from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("shop:product_list_by_category", args=[self.slug])


class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	producer = models.CharField(max_length=100, blank=True)

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)

	@property
	def average_rating(self):
		return Review.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("shop:product_detail", args=[self.id, self.slug])


class Review(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
	RATING_CHOICES = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),
	)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.IntegerField(choices=RATING_CHOICES, default=3)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	#rating = models.IntegerField(choices=RATING_CHOICES)

	class Meta:
		ordering = ('created', 'rating',)

	def __str__(self):
		return 'Recenzja użytkownika {} produktu {}'.format(self.user, self.product)


class Parameter(models.Model):
	category = models.ForeignKey(Category, related_name='parameters', on_delete=models.CASCADE)
	name = models.CharField(max_length=100, db_index=True)

	def __str__(self):
		return self.name


class Description(models.Model):
	parameter = models.ForeignKey(Parameter, related_name='description', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='descript') #dorobić moliwość wybrania tylko produktu z kategorii określonego parametru
	description = models.CharField(max_length=200)

	# może walidacja cleanem, jeśli product i parameter nie mają tego samego category
	def clean(self):
		if not self.parameter.category == self.product.category:
			raise ValidationError('Kategorie produktu i parametru różnią się.')

	def __str__(self):
		return 'Parametr {} produktu {} o opisie {}'.format(self.parameter, self.product, self.description)


class ExtraPhoto(models.Model):
	product = models.ForeignKey(Product, related_name='extra_photo', on_delete=models.CASCADE)
	image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

	def __str__(self):
		return str(self.id) + ": " + self.product.name