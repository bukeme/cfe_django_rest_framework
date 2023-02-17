from django.urls import path
from .views import ProductDetailAPIView, ProductCreateAPIView, ProductListAPIView, ProductListCreateAPIView, ProductUpdateAPIView, ProductDestroyAPIView, ProductMixinView, product_alt_view
from . import viewsets


urlpatterns = [
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('create/', ProductCreateAPIView.as_view()),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('<int:pk>/update/', ProductUpdateAPIView.as_view(), name='product-edit'),
    # path('<int:pk>/update/', product_alt_view),
    path('<int:pk>/delete/', ProductDestroyAPIView.as_view()),
    # path('<int:pk>/delete/', product_alt_view),
    # path('list/', product_alt_view),
    # path('create/', product_alt_view),
    # path('<int:pk>/', product_alt_view),

    path('list-create/', ProductListCreateAPIView.as_view()),
    # path('list/', ProductMixinView.as_view()),
    # path('<int:pk>/', ProductMixinView.as_view()),
    # path('create/', ProductMixinView.as_view()),
    # path('<int:pk>/update/', ProductMixinView.as_view()),
    # path('<int:pk>/delete/', ProductMixinView.as_view()),
    path('list/v2/', viewsets.product_list_view),
]
