from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    gender = models.ForeignKey('Gender',on_delete=models.DO_NOTHING, null=True, verbose_name='Płeć')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True, verbose_name='Kraj')
    phone_number = models.CharField(max_length=9, null=True, verbose_name='Numer telefony')
    funds = models.FloatField(default=5000.0, null=True, verbose_name='Środki')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Lokalizacja')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Data urodzenia')

    def __str__(self):
        return self.user.email

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Country(models.Model):
    name = models.CharField(max_length=255)
    area_code = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Merchant(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('Profile',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Produkt')
    merchant_id = models.ForeignKey('Merchant', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='Cena')
    thumbnail = models.FileField(upload_to='media/items/thumbnail', verbose_name='Okładka')
    bgc = models.FileField(upload_to='media/items/bgc', verbose_name='Tło')
    description = models.TextField(verbose_name='Opis')
    size = models.FloatField(verbose_name='Rozmiar')
    rating = models.IntegerField()
    rating_count = models.IntegerField()
    active = models.BooleanField(verbose_name='Aktywny')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_rating(self):
        if self.rating_count == 0:
            return 'Brak ocen'
        else:
            return round(self.rating / self.rating_count, 2)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.product.name

class Status(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
