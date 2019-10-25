from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


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
	price = models.DecimalField(max_digits=10, decimal_places=2)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'), )
	
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
	rating = models.IntegerField(choices=RATING_CHOICES, default=1)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	rating = models.IntegerField(choices=RATING_CHOICES)

	class Meta:
		ordering = ('created', )
	
	def __str__(self):
		return 'Recenzja użytkownika {} produktu {}'.format(self.user, self.product)

