from django.db import models
from django.forms import ModelForm, Form, ModelChoiceField, IntegerField, BooleanField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core import validators

class Pizza(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    toppings = models.CharField(max_length=100)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({}) - {}€'.format(self.name, self.toppings, self.price, self.created_at)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Illuminato(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField()
    video = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    balance = models.IntegerField(default=100)
    role = models.TextField(choices=(('user', 'user'), ('dev', 'dev')), default='user')
    is_illuminati = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()   

class PizzaForm(ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'toppings', 'price']

class OrderForm(Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(OrderForm, self).__init__(*args, **kwargs)
        admin = User.objects.get(username='admin')
        flag_pizza = 'Pizza itanimullI'
        pizzas = Pizza.objects.filter(user__in=[admin,user]).exclude(name=flag_pizza).order_by('created_at')
        self.fields['pizza'] = ModelChoiceField(queryset=pizzas, to_field_name='name')

