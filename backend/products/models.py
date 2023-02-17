from django.db.models import Q
from django.db import models
from django.conf import settings
import random

# Create your models here.

TAGS_MODEL_VALUE = ['electronics', 'cars', 'furnitures', 'food', 'phones']

class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(Q(public=True))

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if qs.exists():
            if user is not None:
                qs = qs.filter(user=user)
        else:
            return qs
        return qs

class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)
    
    def search(self, query, user=None):
        return self.get_queryset().search(query=query, user=user)

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=1, null=True)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)

    objects = ProductManager()

    def is_public(self) -> bool:
        return self.public

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUE)]

    @property
    def sale_price(self):
        return '%.2f' %(float(self.price) * 0.8)

    @property 
    def body(self):
        return self.content

    def get_discount(self):
        return 55

