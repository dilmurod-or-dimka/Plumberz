from django.shortcuts import render, HttpResponse

# Create your views here.




def home_view(request):
    return render(request, "pages/index.html")

def about_view(request):
    return render(request, "pages/about.html")

def service_view(request):
    return render(request, "pages/service.html")

def contact_view(request):
    return render(request, "pages/contact.html")

def booking_view(request):
    return render(request, "pages/booking.html")

def team_view(request):
    return render(request, "pages/team.html")

def testimonial_view(request):
    return render(request, "pages/testimonial.html")