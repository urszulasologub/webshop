from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Complainment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	order_id = models.IntegerField(default=0, validators=[MinValueValidator(0)], null=True)
	email = models.EmailField(max_length=254)
	body = models.TextField(max_length=1000)
	is_active = models.BooleanField(default=False)


