import json
from django.shortcuts import get_object_or_404, redirect, render

from django.utils import timezone
from django.contrib.auth.models import User
from Chat.views import get_online_users
from datetime import timedelta
from Carts.models import Cart, CartItem
from Chat.models import Room, Message, Section
from Orders.models import Order, OrderItem
from PrivateSessions.forms import PrivateSessionForm
from Products.models import Product
from django.urls import reverse
import requests
from Users.forms import TransactionForm
from Users.models import Badge, Transaction
from .forms import LogInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from Courses.models import Course, CourseProgression, Level, LevelProgression, Module, Video
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import Dashboard
from django.core.serializers import serialize
from Users.models import CustomUser
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

def homeView(request, *args, **kwargs):
    courses = Course.objects.all()
    next_points_goal = 500
    return render(request, 'home.html', {"courses": courses, "next_points_goal": next_points_goal})

def shopView(request, *args, **kwargs):
    products = Product.objects.all()
    return render(request, 'shop.html', {"products": products})

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
    first_module = level.modules.first()  # Get the first module in the level
    if first_module:
        first_video = first_module.videos.first()  # Get the first video in the first module
    else:
        first_video = None
    return render(request, 'video-course.html', {"modules": level.modules.all(), "level": level, "video": first_video})

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
    return redirect('')

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
        


""" def privateSessionView(request, *args, **kwargs):
    form = PrivateSessionRequestForm()

    # Accessing the choices from the form field
    professor_choices = form.fields['selected_professor'].choices

    # Convert the choices to a list for easier manipulation
    professor_choices_list = list(professor_choices)

    # Exclude the first element in the list
    professor_choices_list = professor_choices_list[1:]

    # Accessing the choices for duration_hours
    session_time_choices = form.fields['duration_hours'].choices

    # Convert the choices to a list for easier manipulation
    session_time_choices_list = list(session_time_choices)

    # Exclude the first element in the list
    session_time_choices_list = session_time_choices_list[1:]

    # Now you can manipulate the choices
    separated_duration_choices = [session_time_choices_list[i:i+2] for i in range(0, len(session_time_choices_list), 2)]

    return render(request, 'privateSession.html', {'form': form, "professor_choices_list": professor_choices_list, "separated_duration_choices": separated_duration_choices})

def schedulePrivateSessionView(request):
    if request.method == 'POST':
        form = PrivateSessionRequestForm(request.POST)
        print("testing form validation", request.POST)
        if form.is_valid():
            form.save()
            print("wooooooooooooooooooo")
            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        else:
            # Return a JSON response with form errors
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # Handle GET requests, assuming there's some logic for GET requests
        # You can return an HttpResponse or render a template here
        return HttpResponse("GET request handled") """

def privateSessionView(request, *args, **kwargs):
    if request.method == 'POST':
        return privateSessionSubmitView(request)
    else:
        form = PrivateSessionForm()
        return render(request, 'privateSession.html', {'form': form})

def privateSessionSubmitView(request):
    form = PrivateSessionForm(request.POST)
    if form.is_valid():
        form.save()
        # Redirect to a success page or do something else
        return JsonResponse({"success": True, "message": "form submitted successfully"})
    else:
        return JsonResponse({"success": False, "errors": form.errors})

def privateSessionScheduleDoneView(request, *args, **kwargs):

    return render(request, 'privateSessionScheduleDone.html', {})

def settingsView(request, *args, **kwargs):

    return render(request, 'settings.html', {})

def settingsResetPasswordView(request, *args, **kwargs):

    return render(request, 'settingsResetPassword.html', {})

def paymentView(request, *args, **kwargs):

    return render(request, 'payment.html', {})

def personalInfoView(request, *args, **kwargs):

    return render(request, 'personalInfo.html', {})

def checkoutView(request, *args, **kwargs):
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=CustomUser.objects.get(user=request.user))
    # Check if the cart is empty
    if cart.cart_items.exists():
        print(cart)
        return render(request, 'checkout.html', {"cartID": cart.id, "cart": cart})
    else:
        # If the cart is empty, redirect the user to some page indicating that the cart is empty
         return redirect(reverse('shop'))

def orderCompleteView(request, *args, **kwargs):

    return render(request, 'orderComplete.html', {})

def cartView(request, *args, **kwargs):
    cart=Cart.objects.get(user=request.user.customuser)
    cart.price = cart.calculate_total_price()
    return render(request, 'cart.html', {"cart": cart})

def delete_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('itemId')
        try:
            # Retrieve the cart item
            cart_item = CartItem.objects.get(pk=item_id)
            # Delete the cart item
            cart_item.delete()

            user_cart = None
            try:
                user_cart = Cart.objects.filter(user=CustomUser.objects.get(user=request.user))[0]
            except:
                print ("Cart does not exist")
            if user_cart:
                # Access the items related to the cart using the related name 'cart_items'
                items = user_cart.cart_items.all()
                total_price = user_cart.calculate_total_price()
                ultimate_total = total_price
                total_items = user_cart.cart_items.count()
                print(total_price)
                print("items exists")
            else:
                print("items doesn't exist")
                items = []

            return JsonResponse({'success': True, 'message': 'Item deleted successfully', "total_price": total_price, "ultimate_total":ultimate_total, "total_items": total_items})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'})
    else:
        return JsonResponse({'error': 'bad request'})
  

def createOrderView(request):
    if request.method == 'POST':
        # Retrieve data from request.POST
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        payment_method = request.POST.get('payment_method')
        print("payment_method", payment_method, "credit-card")
        
        cart_id = request.POST.get('cartId')

        # Retrieve the cart
        cart = Cart.objects.get(id=cart_id)

        # Create the order
        order = Order.objects.create(
            user=request.user.customuser,  # Assuming the user is authenticated
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            shipping_method=1,  # You may adjust this as needed
            payment_method=1,
            price=cart.price,  # Ensure you have the correct price for the order
        )

        # Move items from cart to order
        for item in cart.cart_items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                color=item.color,
                size=item.size,
            )

        # Clear the cart after order creation
        cart.cart_items.all().delete()
        cart.price = 0
        cart.save()
        print(payment_method, "credit-card")
        # Redirect to payment page or confirmation page based on payment method
        if payment_method == "credit-card":
            print("eeeeeeeeeeeeeeeeeeeeeee")
            payment = initiate_payment(request, orderId=order.id, amount=order.price)
            url = payment["payUrl"]
        else:
            url = "/shop"  # Redirect to shop or confirmation page if payment method is not credit card

        return JsonResponse({'success': True, 'order_id': order.id, "url": url})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    

def initiate_payment(request, orderId, amount):
    # Make sure to replace these values with your actual credentials and data
    api_key = '665ddd89ecb4e3b38d776b78a:5usETKkdz0MZwYpgWLMIQXg2gtyNgGp'
    konnect_wallet_id = '65ddd89ecb4e3b38d776b78e'

    url = "https://api.preprod.konnect.network/api/v2/payments/init-payment"
    headers = {
        "x-api-key": '65f0e6d5f85f11d7b8c06004:x3QEEv76q8kvnSxAXTqjMljIeYLz',
        "Content-Type": "application/json"
    }
    print(amount*100)
    print(amount*1000)
    payload = {
      "receiverWalletId": '65f0e6d5f85f11d7b8c06008',
      "token": "TND",
      "amount": amount * 1000,
      "type": "immediate",
      "description": "payment description",
      "acceptedPaymentMethods": [
        "bank_card",
      ],
      "lifespan": 10,
      "checkoutForm": True,
      "addPaymentFeesToAmount": True,
      "firstName": request.user.first_name,
      "lastName": request.user.last_name,
      "phoneNumber": request.user.customuser.tel,
      "email": request.user.customuser.email,
      "orderId": orderId,
      "webhook": "http://127.0.0.1:8000/webhook",
      "silentWebhook": True,
      "successUrl": "http://127.0.0.1:8000/order_complete",
      "failUrl": "http://127.0.0.1:8000/payment-error",
      "theme": "dark"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        error_message = "Failed to initiate payment"
        if response.status_code == 401:
            error_message = "Unauthorized: API key is invalid or missing"
        elif response.status_code == 403:
            error_message = "Forbidden: You do not have permission to access this resource"
        elif response.status_code == 404:
            error_message = "Not Found: The requested resource was not found"
        elif response.status_code == 422:
            error_message = "Unprocessable Entity: The request was well-formed but failed validation"
        
        return JsonResponse({"error": error_message}, status=response.status_code)

def webhook(request):
    payment_ref = request.GET.get("payment_ref")
    if payment_ref:
        # Query Konnect API to get payment details
        payment_status = get_payment_status(payment_ref)
        print(payment_status)
        # Process payment status and update database or trigger actions
        # Example: Update database with payment status
        # payment.update(status=payment_status)
        return JsonResponse({"message": "Webhook received", "payment status": payment_status})
    else:
        return JsonResponse({"error": "Payment reference ID not provided"})

def get_payment_status(payment_ref):
    # Make a request to Konnect API to get payment details
    # Replace 'YOUR_KONNECT_API_KEY' with your actual API key
    api_key = '665ddd89ecb4e3b38d776b78a:5usETKkdz0MZwYpgWLMIQXg2gtyNgGp'
    url = f"https://api.preprod.konnect.network/api/v2/payments/{payment_ref}"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        payment_data = response.json()
        payment_status = payment_data.get("payment", {}).get("status")
        return payment_status
    else:
        error_message = "Failed to get payment status"
        if response.status_code == 401:
            error_message = "Unauthorized: API key is invalid or missing"
        elif response.status_code == 403:
            error_message = "Forbidden: You do not have permission to access this resource"
        elif response.status_code == 404:
            error_message = "Not Found: The requested resource was not found"
        elif response.status_code == 422:
            error_message = "Unprocessable Entity: The request was well-formed but failed validation"
        elif response.status_code == 502:
            error_message = "Bad Gateway: The server was acting as a gateway or proxy and received an invalid response from the upstream server"
        
        return error_message



def finalCartCheckoutView(request):
    cartId = request.POST.get('cartId')
    price = request.POST.get('price')
    shippingMethod = request.POST.get('shippingMethod')
    shippingCost = request.POST.get('shippingCost')

    cart = Cart.objects.get(id=cartId)
    cart.price = price
    cart.shippingMethod = shippingMethod
    cart.shippingCost = shippingCost
    cart.save()
    return JsonResponse({'success': True})


def notificationView(request, *args, **kwargs):

    return render(request, 'settingsNotification.html', {})

from django.core.serializers.json import DjangoJSONEncoder


def serverChatView(request, room_name, *args, **kwargs):
    customuser_id = request.user.customuser.id
    room = get_object_or_404(Room, name=room_name)
    messages = Message.objects.filter(room=room).order_by('timestamp').values('user__user__username', 'content', 'user__pfp', 'timestamp')
    messages_list = list(messages)
    
    # Convert QuerySet to list of dictionaries
    messages_list = [dict(message) for message in messages_list]

    # Serialize the messages list to JSON
    messages_json = json.dumps(messages_list, cls=DjangoJSONEncoder)
    online_user_ids = get_online_users()
    online_users = CustomUser.objects.filter(user_id__in=online_user_ids)
    all_badges = Badge.objects.filter(customusers__in=online_users).order_by('-index')
    sections = Section.objects.all().order_by('-index')

    print(messages_json)  # Add this line for debugging
    return render(request, 'serverChat.html', {"room_name": room_name, "customuser_id": customuser_id, "messages_json": messages_json, "online_members": online_users, "all_badges": all_badges, "sections": sections})

def privateChatView(request, *args, **kwargs):

    return render(request, 'privateChat.html', {})


    

def getVideoView(request, *args, **kwargs):
    if request.method == 'POST':
        videoId = request.POST.get("videoId")
        print(videoId) # Debugging purpose
        try:
            video = Video.objects.get(id=videoId)
            serialized_video = {
                "title": video.title,
                "video_file": video.video_file.url,
                "notes": video.notes,
                "summary": video.summary,
                'finished': video.finished,
                'quiz_id': video.quiz.id,
                'quiz_question': video.quiz.id,
                'quiz_options': video.quiz.options,
                'answer': video.quiz.answer,
            }
            return JsonResponse({'success': True, "video": serialized_video})
        except Video.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Video not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    
def videoFinishedView(request, *args, **kwargs):
    videoId = request.POST.get("videoId")
    print(videoId) # Debugging purpose
    video = Video.objects.get(id=videoId)
    user = request.user.customuser
    user.finished_videos.add(video)
    user.save()
    return JsonResponse({'success': True, 'message':"video finished successfully"})


def ProductView (request, product_id, *args, **kwargs):
    product = Product.objects.get(id=product_id)
    return render(request, 'product.html', {"product": product})

def logout_view(request):
    logout(request)
    next_page = request.GET.get('next', '/')  # Redirige vers  par défaut
    return redirect(next_page)




def add_to_cart(request):
    if request.method == 'POST':
        # Get the product ID and types from the POST data
        product_id = request.POST.get('product_id')
        color = request.POST.get('color')
        size = request.POST.get('size')
        print('aaaaaaa',request.user)
        if product_id:
            # Get the product object
            product = get_object_or_404(Product, id=product_id)

            # Get the user's cart or create one if it doesn't exist
            user_cart, created = Cart.objects.get_or_create(user=CustomUser.objects.get(user=request.user))

            # Check if the product is already in the cart
            # Parse the 'types' JSON string into a Python dictionary

            # Check if the item already exists in the cart with the same product and types
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=product,
                color=color,
                size=size,
            )

            if not item_created:
                # If the item already exists in the cart, increment its quantity
                cart_item.quantity += 1
                cart_item.save()

            # Set the created_at timestamp for the cart if it's newly created
            if created:
                user_cart.created_at = timezone.now()
                user_cart.save()

            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        else:
            # Return a JSON response indicating failure
            return JsonResponse({'success': False, 'message': 'Product ID not provided'})
    else:
        # Return a JSON response indicating failure for non-POST requests
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def add_video_to_finished(request, video_id):
    if request.method == 'POST':
        user = request.user.customuser
        video = get_object_or_404(Video, id=video_id)
        
        # Add the video to the finished videos of the user
        user.finished_videos.add(video)
        user.save()
        
        return JsonResponse({'message': f'Video "{video.title}" added to finished videos for user {user.user.username}'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)



def profileView(request, username, *args, **kwargs):
    profile_user = get_object_or_404(User, username=username)
    custom_profile_user = CustomUser.objects.get(user=profile_user)
    return render(request, 'profile.html', {"custom_profile_user": custom_profile_user})