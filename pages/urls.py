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
]