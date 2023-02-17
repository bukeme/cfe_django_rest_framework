from rest_framework import generics
from rest_framework.response import Response
from products.models import Product
from products.serializer import ProductSerializer
from . import client

# Create your views here.

class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        tag = request.GET.get('tag')
        public = str(request.GET.get('public')) != '0'
        user = None 
        if request.user.is_authenticated:
            user = request.user.username
        print(user, query, public, tag)
        if not query:
            return Response('', status=404)
        result = client.perform_search(query, tags=tag, user=user, public=public)
        return Response(result)

class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        result = Product.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            result = qs.search(query=q, user=user)
        return result