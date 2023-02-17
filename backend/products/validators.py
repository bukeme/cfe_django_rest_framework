from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product

def validate_title(value): #validate_<field_name>
    # qs = Product.objects.filter(title__iexact=value)
    if 'hello' in value:
        raise serializers.ValidationError(f'hello in {value}')
    return value

unique_data = UniqueValidator(queryset=Product.objects.all())