from django.shortcuts import redirect, render

from django.utils import timezone
from datetime import timedelta
from PrivateSessions.forms import PrivateSessionForm
from Users.forms import TransactionForm
from Users.models import Transaction
from .forms import LogInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from Courses.models import Course, CourseProgression, Level, LevelProgression
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import Dashboard
from django.core.serializers import serialize
from Users.models import CustomUser

def homeView(request, *args, **kwargs):
    courses = Course.objects.all()
    next_points_goal = 500
    return render(request, 'home.html', {"courses": courses, "next_points_goal": next_points_goal})

def shopView(request, *args, **kwargs):
    return render(request, 'shop.html', {})

def coursesView(request, *args, **kwargs):
    courses = Course.objects.all()


    return render(request, 'courses.html', {"courses": courses})

def levelsView(request, *args, **kwargs):
    course_id = kwargs.get('course_id')
    course = Course.objects.get(id=course_id)
    levels = Level.objects.filter(course=course)  # Filter levels by the course
    return render(request, 'levels.html', {"levels": levels})

def videoCourseView(request, level_id):
    level = Level.objects.get(id=level_id)
    return render(request, 'video-course.html', {"modules": level.module_set.all()})

def notesCourseView(request, level_id):
    level = Level.objects.get(id=level_id)
    return render(request, 'notes-course.html', {"modules": level.module_set.all()})

def imgQuizzCourseView(request, level_id):
    level = Level.objects.get(id=level_id)
    return render(request, 'imgQuizz-course.html', {"modules": level.module_set.all()})

def textQuizzCourseView(request, level_id):
    level = Level.objects.get(id=level_id)
    return render(request, 'textQuizz-course.html', {"modules": level.module_set.all()})

def lessonCompletedView(request, level_id):
    level = Level.objects.get(id=level_id)
    return render(request, 'lessonComplete.html', {"modules": level.module_set.all()})


def registerView(request, *args, **kwargs):
    SignupForm = SignUpForm()
    return render(request, 'register.html', {"SignupForm": SignupForm})

def registerf(request, *args, **kwargs):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            """ login """
            user = authenticate(firstName=first_name, lastName=last_name, username=username, email=email, password1=password1, password2=password2)
            login(request, user)
            messages.success(request, "registred and logged in successfully.")
            return JsonResponse({'success': True})  # Return success response
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})  # Return error response
    else:
        return redirect('register')

def loginView(request, *args, **kwargs):
    LoginForm = LogInForm()

    return render(request, 'login.html', {"LoginForm": LoginForm})

def loginf(request, *args, **kwargs):
    print("1")
    if request.method == 'POST':
        print("2")
        form = LogInForm(data=request.POST)
        if form.is_valid():
            print("3")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                print("4")
                messages.success(request, 'Logged In succesfully')
                login(request, user)

                return  JsonResponse({'success': True, 'error': "User logged in"})
            else:
                print("5")
                return  JsonResponse({'success': False, 'error': "User not found"})
        else:
            print("6")
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'error': errors})


def logoutf(request):
    logout(request)
    # Redirect to a specific page after logout
    return redirect('home')

def pageNotFoundView(request, *args, **kwargs):
    return render(request, '404.html', {})

def forgetPasswordView(request, *args, **kwargs):

    return render(request, 'forgetPassword.html', {})


def resetDoneView(request, *args, **kwargs):
    return render(request, 'resetDone.html', {})

def newPasswordView(request, *args, **kwargs):
    
    return render(request, 'newPassword.html', {})

def verificationView(request, *args, **kwargs):
    return render(request, 'verification.html', {})




def dashboardView(request, *args, **kwargs):
    dashboard = Dashboard.objects.get(id=1)
    transactionForm = TransactionForm
    transactions = Transaction.objects.all().order_by('-date')  # Assuming 'date' is the field you want to order by
    reversed_transactions = reversed(transactions)

    top_users = CustomUser.objects.all()
    top_users = sorted(top_users, key=lambda user: user.calculate_balance(), reverse=True)[:5]

    top_user = sorted(top_users, key=lambda user: user.calculate_balance(), reverse=True)[:1][0]
    print(top_user)
    return render(request, 'dashboard.html', {"dashboard": dashboard, "top_user_pfp": top_user.pfp, "transactions": reversed_transactions, "top_users": top_users, "top_user": top_user, "transactionForm": transactionForm})

def getDashboard(request, *args, **kwargs):
    if request.method == "GET":
        dashboard = Dashboard.objects.get(id=1)
        dashboard_data = {
            'objectif': dashboard.objectif,
            'profits': dashboard.calculate_profits(),
            'losses': dashboard.calculate_losses(),
            'balance': dashboard.total_balance(),
        }

        # Return the dictionary as JSON response
        return JsonResponse({"success": True, "dashboard": dashboard_data})
    else:
        return JsonResponse({"success": False, "error": "Bad request"})

def getTransactions(request, *args, **kwargs):
    if request.method == "GET":
        transactions = Transaction.objects.all()
    
        # Prepare transaction data
        transactions_data = []
        for transaction in reversed(transactions):
            badges_list = []

            # Iterate through user's badges and create dictionaries
            for badge in transaction.user.badges.all():
                badge_dict = {
                    'title': badge.title,
                    'icon': badge.icon.url  # Assuming badge.icon is a FileField
                }
                badges_list.append(badge_dict)


            transaction_data = {
                'user': transaction.user.user.username,  # Assuming user has a related User model
                'pfp': transaction.user.pfp.url,
                'badges': badges_list,
                'type': transaction.type,
                'pair': transaction.pair,
                'amount': transaction.amount,
                'date': transaction.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format the date as string
                # Add other fields as needed
            }
            transactions_data.append(transaction_data)

        # Return the transactions data as JSON response
        return JsonResponse({"success": True, "transactions": transactions_data})
    else:
        return JsonResponse({"success": False, "error": "Bad request"})

def getRanking(request, *args, **kwargs):
    if request.method == "GET":
        # Query all users and order them by calculated balance in descending order
        top_users = CustomUser.objects.all()
        top_users = sorted(top_users, key=lambda user: user.calculate_balance(), reverse=True)[:5]

        # Serialize user data into JSON serializable format
        serialized_users = []
        rankIco = 1
        for user in top_users:
            serialized_user = {
                'username': user.user.username,
                'pfp': user.pfp.url,
                'balance': user.calculate_balance(),
                'rankIco': rankIco,
                # Add other fields if necessary
            }
            rankIco += 1
            serialized_users.append(serialized_user)


        # Pass the serialized top 5 users to the JsonResponse
        return JsonResponse({"success": True, "top_users": serialized_users})
    else:
        return JsonResponse({"success": False, "error": "Bad request"})

def getTopUser(request, *args, **kwargs):
    if request.method == "GET":
        # Query all users and order them by calculated balance in descending order
        top_users = CustomUser.objects.all()
        top_user = sorted(top_users, key=lambda user: user.calculate_balance(), reverse=True)[:1][0]
        badges_list = []

        for badge in top_user.badges.all():
            badge_dict = {
                'title': badge.title,
                'icon': badge.icon.url  # Assuming badge.icon is a FileField
            }
            badges_list.append(badge_dict)

        # Extract the username from the top user
        top_user_username = top_user.user.username
        
        # Serialize the top user
        top_user_serialized = serialize('json', [top_user])
        
        # Pass the serialized top user to the JsonResponse along with the username
        return JsonResponse({"success": True, "top_user": top_user_serialized, "top_user_badgesList": badges_list, "top_user_username": top_user_username, 'top_user_pfp': top_user.pfp.url})
    else:
        return JsonResponse({"success": False, "error": "Bad request"})
    


def landingView (request, *args, **kwargs):
    return render(request, 'landing.html', {})



def course_progress(request, *args, **kwargs):
    if request.method == 'POST':
        user = request.user.customuser
        # Assuming you have the user instance

        # Assuming you have the level instance, or you can pass the level_id through the URL
        level_id = 1
        level = Level.objects.get(id=level_id)

        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)

        # Get or create the LevelProgression instance for the user and level
        course_progression, created = CourseProgression.objects.get_or_create(user=user, course=course)
        level_progression, created = LevelProgression.objects.get_or_create(user=user, level=level)


        total_progress = course_progression.calculate_progression()
        return JsonResponse({"success": True, "course_progression": course_progression.calculate_progression()})
    else:
        return JsonResponse({"success": False})


def level_progress(request, *args, **kwargs):
    if request.method == 'POST':
        user = request.user.customuser
        # Assuming you have the user instance

        # Assuming you have the level instance, or you can pass the level_id through the URL
        level_id = request.POST.get('level_id')
        level = Level.objects.get(id=level_id)

        # Get or create the LevelProgression instance for the user and level
        level_progression, created = LevelProgression.objects.get_or_create(user=user, level=level)

        return JsonResponse({"success": True, "level_progression": level_progression.progress})
    else:
        return JsonResponse({"success": False})

def addPoints(request, *args, **kwargs):
    if request.method == 'POST':
        user = request.user.customuser
        
        # Check if the user has added points in the last 24 hours
        last_added_points_time = user.last_added_points_time
        if last_added_points_time is not None and timezone.now() - last_added_points_time < timedelta(hours=24):
            return JsonResponse({"success": False, "message": "Points can only be added once every 24 hours."})
        
        # Add points to the user
        points_to_add = 10
        user.points += points_to_add
        user.last_added_points_time = timezone.now()
        user.save()

        return JsonResponse({"success": True, "message": f"Points successfully added: {points_to_add}"})
    
    return JsonResponse({"success": False, "message": "Invalid request method."})


def addTransaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the transaction
            transaction = form.save(commit=False)
            transaction.user = request.user.customuser
            transaction.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
        


def privateSessionView(request, *args, **kwargs):
    
    form = PrivateSessionForm()

    session_time_choices = form.fields['session_time'].choices
    separated_choices = [session_time_choices[i:i+2] for i in range(0, len(session_time_choices), 2)]
    print(separated_choices)

    return render(request, 'privateSession.html', {'form': form, "separated_choices": separated_choices})

def privateSessionScheduleDoneView(request, *args, **kwargs):

    return render(request, 'privateSessionScheduleDone.html', {})