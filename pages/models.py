from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser


class Service(models.Model):
    title = models.CharField(verbose_name="Название категории", max_length=150, unique=True)
    description = models.TextField(verbose_name="Описание услуги")
    slug = models.SlugField(blank=True, null=True, unique=True)
    quality = models.BooleanField(default=False)
    customer = models.BooleanField(default=False)
    supports = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_photo_service(self):
        photo = self.servicesimage_set.all().first()
        if photo is not None:
            return photo.photo.url
        return "https://images.satu.kz/126101312_w640_h640_razdel-v-razrabotketovary.jpg"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"


class ServicesImage(models.Model):
    photo = models.ImageField(verbose_name="Foto", upload_to="services/", blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)



class Staff(models.Model):
    full_name = models.CharField(verbose_name="Full Name", max_length=150)
    designation = models.CharField(verbose_name="Designation", max_length=150)
    facebook = models.URLField(verbose_name="Facebook", blank=True, null=True)
    twitter = models.URLField(verbose_name="Twitter", blank=True, null=True)
    instagram = models.URLField(verbose_name="Instagram", blank=True, null=True)


    def __str__(self):
        return self.full_name

    def get_photo_staff(self):
        photo = self.staffimage_set.all().first()
        if photo is not None:
            return photo.photo.url
        return "https://images.satu.kz/126101312_w640_h640_razdel-v-razrabotketovary.jpg"

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"

class StaffImage(models.Model):
    photo = models.ImageField(verbose_name="Foto", upload_to="staff/", blank=True, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)


class User(AbstractUser):
    avatar = models.ImageField(verbose_name="Foto", upload_to="avatar/", blank=True, null=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name="Comment")


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"