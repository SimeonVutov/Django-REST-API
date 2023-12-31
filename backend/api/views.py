from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def api_home(request, *args, **kwargs):

    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        print(serializer.data)

        return Response(serializer.data)
