# -*- coding: UTF8 -*-

from rest_framework import serializers
from rest_api.rest_api_field import NativeDateTimeField
from .models import ProductOrder, ProductOrderStatus, ProductOrderComment
from product.models import Product
from product.serializers import ProductSerializer
# from .pay.serializers import PayOrderSerializer
from user.address.serializers import AddressSerializer
from user.models import Address, User


class ProductOrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOrderStatus
        fields = ["id", "name"]


class ProductOrderSerializer(serializers.ModelSerializer):
    create_time = NativeDateTimeField()
    product = ProductSerializer()
    # pay_order = PayOrderSerializer()
    status = ProductOrderStatusSerializer()
    address = AddressSerializer()

    class Meta:
        model = ProductOrder
        fields = ["id", "create_time", "product", "status", "address", "create_time", "num", "sf_no"]


class NewProductOrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset=ProductOrderStatus.objects.all())
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    invite_code = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = ProductOrder
        # read_only_fields = ["id", "create_time", "pay_order", "status"]
        fields = ["product", "status", "address", "user", "id", "invite_code"]


class ProductOrderCommnetSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=ProductOrder.objects.all())
    create_time = NativeDateTimeField()

    class Meta:
        model = ProductOrderComment
        list_serializer_class = serializers.ListSerializer
        fields = ["order", "comment", "create_time"]
