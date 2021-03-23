from django.contrib.auth import views
from django.urls import path
from .views import ProfileView, RegisterView, SettingsView, DeleteCard, GetApplicationsReport, MessagesView, \
    FeedbackView, ChangePhoneView, PersonalSaleView, ProfileLoginView
from .utils import generate_qr


urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('personal-sale/', PersonalSaleView.as_view(), name='personal_sale'),
    path('change-phone/', ChangePhoneView.as_view(), name='change_phone'),
    path('login/', ProfileLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-change', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('remove_card/<int:pk>/', DeleteCard.as_view(), name='remove_card'),
    path('get_report/', GetApplicationsReport.as_view(), name='get_report'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('generate-qr/', generate_qr, name='generate_qr'),
]
