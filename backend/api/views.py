from django.http import JsonResponse
from products.models import Product
from rest_framework.decorators import api_view


@api_view(["GET"])
def api_home(request, *args, **kwargs):
    random_product = Product.objects.all().order_by("?").first()
    data = {}

    if random_product:
        data['id'] = random_product.id
        data['title'] = random_product.title
        data['content'] = random_product.content
        data['price'] = random_product.price

    return JsonResponse(data)
