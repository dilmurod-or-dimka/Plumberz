from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError
from django.http import HttpResponseRedirect
from django.core.exceptions import BadRequest
from .models import User, Staff, Service, Comment
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import CommentForm
from django.contrib.auth import authenticate, login, logout
from .utils import send_mail_for_contact_us, send_to_telegram
from django.urls import reverse
from django.contrib import messages as django_messages


# Create your views here.


def home_view(request):
    users = User.objects.all()
    comments = Comment.objects.all().order_by('-created_at')
    staffs = Staff.objects.all()[:4]
    services = Service.objects.all()
    staffs_for_fact = Staff.objects.all()
    context = {
        'active_page': 'home',
        'users': users,
        'staffs': staffs,
        'services': services,
        'comments': comments,
        'staffs_for_fact': staffs_for_fact,
    }
    return render(request, "pages/index.html", context)


def about_view(request):
    staffs = Staff.objects.all()[:4]
    comments = Comment.objects.all().order_by('-created_at')
    users = User.objects.all()
    services = Service.objects.all()
    context = {
        'active_page': 'about',
        'users': users,
        'services': services,
        'staffs': staffs,
        'comments': comments,
    }
    return render(request, "pages/about.html", context)


def service_view(request):
    services = Service.objects.all()
    comments = Comment.objects.all().order_by('-created_at')

    context = {
        'active_page': 'service',
        'services': services,
        'comments': comments,
    }
    return render(request, "pages/service.html", context)


def contact_view(request):
    services = Service.objects.all()
    context = {
        "active_page": "contact",
        "services": services,
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            user_name = f"{request.user.first_name} {request.user.last_name}"
            email = request.user.email
        else:
            user_name = request.POST.get("name")
            email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        send_mail_for_contact_us(email, subject, message, user_name)

        # Redirect to contact page after form submission
        return HttpResponseRedirect(reverse('contact'))

    return render(request, "pages/contact.html", context)


def booking_view(request):
    services = Service.objects.all()
    if request.method == "POST":
        user_name = request.POST.get("name")
        email = request.POST.get("email")
        service_id = request.POST.get("service")
        date = request.POST.get("date")
        message = request.POST.get("messages")

        # Basic validation
        if not user_name or not email or not service_id or not date:
            return HttpResponseRedirect("Please fill out all required fields.")

        # Получаем название сервиса по его id
        try:
            service = Service.objects.get(id=service_id).title
        except Service.DoesNotExist:
            return HttpResponseRedirect("Selected service does not exist.")

        body = {
            "user_name": user_name,
            "email": email,
            "service": service,
            "date": date,
            "message": message,
        }
        messages = "\n".join(body.values())

        try:
            send_to_telegram(messages)
            django_messages.success(request, "Your booking request has been sent successfully.")
        except BadRequest as e:
            print(f"Error sending to Telegram: {str(e)}")
            return HttpResponseRedirect("There was an error sending your request.")
        return redirect("home")

    context = {
        'active_page': 'pages',
        'services': services,
    }
    return render(request, "pages/booking.html", context)


def team_view(request):
    services = Service.objects.all()
    staffs = Staff.objects.all()
    context = {
        'active_page': 'pages',
        'services': services,
        'staffs': staffs,
    }
    return render(request, "pages/team.html", context)


def testimonial_view(request):
    services = Service.objects.all()
    comments = Comment.objects.all().order_by('-created_at')
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect("testimonial")
    else:
        form = CommentForm()

    context = {
        'active_page': 'pages',
        "services": services,
        "form": form,
        "comments": comments
    }
    return render(request, "pages/testimonial.html", context)


class Profile_view(LoginRequiredMixin, View):
    template_name = "pages/profil.html"

    def get(self, request):
        user = request.user
        services = Service.objects.all()
        context = {
            'active_page': 'profile',
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "avatar": user.avatar,
            'services': services,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        avatar = request.FILES.get('avatar')
        print("dsladsss", avatar)

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            if not User.objects.filter(email=email).exclude(pk=user.pk).exists():
                user.email = email
            else:
                messages.error(request, "Email email already registered.")
                return redirect("profile")

        if avatar:
            user.avatar = avatar

        user.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("profile")


class LoginView(View):
    template_name = "pages/login.html"

    def get(self, request):
        services = Service.objects.all()
        context = {
            'active_page': 'login',
            "services": services,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name)


def logout_view(request):
    logout(request)
    return redirect('home')


class RegisterView(View):
    template_name = 'pages/register.html'

    def get(self, request):
        services = Service.objects.all()
        context = {
            "services": services,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        if not first_name:
            messages.error(request, "First name is required.")
            return redirect('/register')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('/register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email already exists")
            return redirect('/register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists")
            return redirect('/register')

        is_first_user = not User.objects.exists()

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password1),
            is_superuser=is_first_user,
            is_staff=is_first_user,
            username=username
        )
        user.save()
        login(request, user)

        return redirect('/')


@login_required
def delete_profile_picture(request):
    user = request.user  # This fetches the current logged-in user
    try:
        if user.avatar:
            # Delete the profile picture
            user.avatar.delete(save=False)
            user.avatar = None
            user.save()

            messages.error(request, "Profile picture deleted successfully.")
        else:
            messages.info(request, "No profile picture to delete.")
    except User.DoesNotExist:
        messages.warning(request, "Profile does not exist.")

    return redirect('profile')
