from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer

from api.mixins import StaffEditorPermissionMixin


# class ProductMixinView(
#         mixins.CreateModelMixin,
#         mixins.ListModelMixin,
#         mixins.RetrieveModelMixin,
#         generics.GenericAPIView):

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'pk'

#     def get(self, request, pk=None, *args, **kwargs):
#         if pk is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def perform_create(self, serializer):
#         content = serializer.validated_data.get('content')

#         if content is None:
#             content = 'This is auto generated content'
#         serializer.save(content=content)


class ProductListCreateAPIView(
        StaffEditorPermissionMixin,
        generics.ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None

        if content is None:
            content = title

        serializer.save(user=self.request.user, content=content)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        print(request.user)
        return qs.filter(user=request.user)


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(
        StaffEditorPermissionMixin,
        generics.RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
        StaffEditorPermissionMixin,
        generics.RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(
        StaffEditorPermissionMixin,
        generics.RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


product_destroy_view = ProductDestroyAPIView.as_view()


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == 'GET':
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)

        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data

        return Response(data)

    if method == 'POST':
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')

            if content is None:
                content = title

            serializer.save(content=content)

            return Response(serializer.data)
        return Response({'error': 'Invalid data'}, status=400)
