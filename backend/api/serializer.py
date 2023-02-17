from rest_framework import serializers

from products.models import Product



class UserPublicInlineSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk', read_only=True)

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    other_products = serializers.SerializerMethodField(read_only=True)

    def get_other_products(self, obj):
        user = obj
        qs = user.product_set.all()[:5]
        return UserPublicInlineSerializer(qs, many=True, context=self.context).data