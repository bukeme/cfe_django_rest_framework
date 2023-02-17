from wsgiref.validate import validator
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validators import validate_title, unique_data
from api.serializer import UserPublicSerializer


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source= 'user',read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(write_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk')
    title = serializers.CharField(validators=[validate_title, unique_data])
    name = serializers.CharField(source='title', read_only=True)
    body = serializers.CharField(source='title')
    class Meta:
        model = Product
        fields = ['pk', 'owner','url', 'edit_url', 'title', 'name', 'email', 'body', 'price', 'sale_price', 'my_discount']

    # def create(self, validated_data):
    #     email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     return obj

    # def validate_title(self, value): #validate_<field_name>
    #     request = self.context.get('request')
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f'{value} is already a product title')
    #     return value

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.context.get('request')
    #     user = request.user
    #     if user.is_authenticated():
    #         return Product.objects.none()
    #     return qs.filter(user=user)

    def get_edit_url(self, obj):
        # return f'/api/products/{obj.pk}/'
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('product-detail', kwargs={'pk': obj.pk}, request=request)

    def get_my_discount(self, obj):
        try:
            return obj.get_discount()
        except:
            return None