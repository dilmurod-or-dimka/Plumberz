from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("service/", views.service_view, name="service"),
    path("contact/", views.contact_view, name="contact"),
    path("booking/", views.booking_view, name="booking"),
    path("team/", views.team_view, name="team"),
    path("testimonial/", views.testimonial_view, name="testimonial"),
    path("login/", views.LoginView.as_view(),name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("delete_profile_picture/", views.delete_profile_picture, name="delete_profile_picture"),
    path("profile/", views.Profile_view.as_view(), name="profile"),
]