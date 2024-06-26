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
from django_ckeditor_5 import views as ckeditor_views

from Pages import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
urlpatterns = [
    path('admin/', admin.site.urls),
    path("chat/", include("Chat.urls")),
    path('shop/', views.shopView, name="shop"),
    path('product/<int:product_id>/', views.ProductView, name="product"),
    path('home/', views.homeView, name="home"),
    path('courses/', views.coursesView, name="courses"),
    path('<int:course_id>/levels/', views.levelsView, name="levels"),
    path('<int:level_id>/video-course/', views.videoCourseView, name="video-course"),
    path('<int:level_id>/notes-course/', views.notesCourseView, name="notes-course"),

    path('<int:level_id>/imgQuizz-course/', views.imgQuizzCourseView, name="imgQuizz-course"),

    path('<int:level_id>/textQuizz-course/', views.textQuizzCourseView, name="textQuizz-course"),
    path('<int:level_id>/lesson-completed/', views.lessonCompletedView, name="lesson-completed"),

    path('get-video/', views.getVideoView, name="get-video"),
    path('videoFinished/', views.videoFinishedView, name="videoFinished"),


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
    path('getPoints/', views.getPoints, name="getPoints"),
    path('logout/', views.logout_view, name='logout'),
    path('', views.landingView, name="landing"),

    path('course-progress/', views.course_progress, name="course-progress"),
    path('level_progress/', views.level_progress, name="level_progress"),

    path('add_points/', views.addPoints, name="add_points"),
    path('add_transaction/', views.addTransaction, name="add_transaction"),

    path('private-session/', views.privateSessionView, name="private_session"),
    path('private-session-done/', views.privateSessionScheduleDoneView, name="private_session_done"),

    path('schedulePrivateSession/', views.privateSessionSubmitView, name="schedule_private_session"),


    path('settings/', views.settingsView, name="settings"),
    path('settings_reset_password/', views.settingsResetPasswordView, name="settingd_reset_password"),
    path('payment/', views.paymentView, name="payment"),
    path('personal_info/', views.personalInfoView, name="personal_info"),
    path('settings_notification/', views.notificationView, name="settings_notification"),


    path('checkout/', views.checkoutView, name="checkout"),
    path('order_complete/', views.orderCompleteView, name="order_complete"),
    path('cart/', views.cartView, name="cart"),


    path('server-chat/<str:room_name>/', views.serverChatView, name="server_chat"),
    path('private-chat/', views.privateChatView, name="private_chat"),
    
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('delete-cart-item/', views.delete_cart_item, name='delete_cart_item'),
    path('create-order/', views.createOrderView, name='create_order'),
    path('final-cart-checkout/', views.finalCartCheckoutView, name='final-cart-checkout'),


    path('add_video_to_finished/<int:video_id>', views.add_video_to_finished, name='add-video-to-finished'),


    path('profile/<str:username>', views.profileView, name='profile'),

    path('submit-feedback/', views.submitFeedbackView, name='submit_feedback'),

    path('getbtc/', views.get_btc_price, name='btc'),
    path('geteth/', views.get_eth_price, name='eth'),
    path('getsol/', views.get_sol_price, name='sol'),


    path('getCryptoDetails/', views.getCryptoDetails, name='get_crypto_details'),


    path('buy-course/', views.buyCourseView, name='buy-course'),

    path('start-quest/', views.start_quest, name='start-quest'),
    path('complete-step/', views.complete_step, name='complete-step'),
    
    path('quest-detail/', views.quest_detail, name='quest-detail'),
    path('user-quest-progression/', views.user_quest_progression, name='user-quest-progression'),


    path('next-video/', views.getNextVideo, name='next-video'),

    path('add_liked_video/', views.add_liked_video, name='add_liked_video'),
    path('remove_liked_video/', views.remove_liked_video, name='remove_liked_video'),
    path('is_video_liked/', views.is_video_liked, name='is_video_liked'),

    path("ckeditor5/", include('django_ckeditor_5.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
