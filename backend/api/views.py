from email import header
import json
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from products.models import Product
from products.serializer import ProductSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response


# ---------------------- GET ----------------

# @api_view(['GET', 'POST'])
# def api_home(request, *args, **kwargs):

#     # body = request.body
#     # print(request.GET)
#     # data = {}
#     # try:
#     #     data = json.loads(body)
#     # except:
#     #     pass
#     # data['headers'] = dict(request.headers)

#     instance = Product.objects.order_by('?').first()
#     data = {}
#     if instance:
#         # data['id'] = model_data.id
#         # data['title'] = model_data.title
#         # data['content'] = model_data.content 
#         # data['price'] = model_data.price
#         # data = model_to_dict(model_data)

#         # data = model_to_dict(model_data, fields=['id', 'title', 'price'])
#         data = ProductSerializer(instance).data


#         # json_data_str = json.dumps(data) # converts json to stringprint(json_data_str)
#     # return HttpResponse(json_data_str, headers={'content-type': 'application/json'}) # send httpRequest as json
#     # return JsonResponse(data)
#     return Response(data)


# ----------------------- POST -----------------------------


@api_view(['POST'])
def api_home(request, *args, **kwargs):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        print(instance)
        return Response(serializer.data)
