"""
URL configuration for TTG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static

from Pages import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', views.shopView, name="shop"),
    path('', views.homeView, name="home"),
    path('courses/', views.coursesView, name="courses"),
    path('<int:course_id>/levels/', views.levelsView, name="levels"),
    path('<int:level_id>/video-course/', views.videoCourseView, name="video-course"),
    path('<int:level_id>/notes-course/', views.notesCourseView, name="notes-course"),
    path('<int:level_id>/imgQuizz-course/', views.imgQuizzCourseView, name="imgQuizz-course"),
    path('<int:level_id>/textQuizz-course/', views.textQuizzCourseView, name="textQuizz-course"),
    path('<int:level_id>/lesson-completed/', views.lessonCompletedView, name="lesson-completed"),

    path('register/', views.registerView, name="register"),
    path('registerf/', views.registerf, name="registerf"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="forgetPassword.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="verification.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class = SetPasswordForm, template_name="newPassword.html", success_url=reverse_lazy('password_reset_complete')), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="resetDone.html"), name="password_reset_complete"),

    path('login/', views.loginView, name="login"),
    path('loginf/', views.loginf, name="loginf"),

    path('logoutf/', views.logoutf, name="logout"),

    path('404/', views.pageNotFoundView, name="404"),
    
    path('verification/', views.verificationView, name="verification"),

    path('dashboard/', views.dashboardView, name="dashboard"),
    path('getDashboard/', views.getDashboard, name="getDashboard"),
    path('getTransactions/', views.getTransactions, name="getTransaction"),
    path('getRanking/', views.getRanking, name="getRanking"),
    path('getTopUser/', views.getTopUser, name="getTopUser"),

    path('landing/', views.landingView, name="landing"),

    path('course_progress/', views.course_progress, name="course_progress"),
    path('level_progress/', views.level_progress, name="level_progress"),

    path('add_points/', views.addPoints, name="add_points"),
    path('add_transaction/', views.addTransaction, name="add_transaction"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
