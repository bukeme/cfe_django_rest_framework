from rest_framework import generics, authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from .serializer import ProductSerializer
from .models import Product
from api.permissions import IsStaffEditorPermission
from api.authentication import TokenAuthentication
from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin


class ProductAPIViewMixin(object):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(ProductAPIViewMixin, StaffEditorPermissionMixin, generics.RetrieveAPIView):
    pass

class ProductCreateAPIView(ProductAPIViewMixin, StaffEditorPermissionMixin, generics.CreateAPIView):
    def perform_create(self, serializer):
        print(serializer.validated_data.get('title'))
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)
        return super().perform_create(serializer)

class ProductListAPIView(ProductAPIViewMixin, StaffEditorPermissionMixin, generics.ListAPIView):
    pass

class ProductListCreateAPIView(UserQuerySetMixin, ProductAPIViewMixin, StaffEditorPermissionMixin, generics.ListCreateAPIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
    ]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.DjangoModelPermissions]
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]
    def perform_create(self, serializer):
        email = serializer.validated_data.pop('email')
        print(serializer.validated_data.get('title'))
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)
        return super().perform_create(serializer)


class ProductUpdateAPIView(ProductAPIViewMixin, StaffEditorPermissionMixin, generics.UpdateAPIView):
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDestroyAPIView(ProductAPIViewMixin, StaffEditorPermissionMixin, generics.DestroyAPIView):
    def perform_destroy(self, instance):
        super().perform_destroy(instance)

class ProductMixinView(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs['pk']
        except:
            pk = None
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print(serializer.validated_data.get('title'))
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)
        return super().perform_create(serializer)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def product_alt_view(request, pk=None, *args, **kwargs):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)

    if request.method == 'GET':
        if pk:
            obj = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(obj, many=False).data
            return Response(serializer)
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True).data
        return Response(serializer)

    if request.method == 'PUT':
        obj = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(data=request.data, instance=obj)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    if request.method == 'DELETE':
        obj = get_object_or_404(Product, pk=pk)
        obj.delete()
