# -*- coding:UTF-8 -*-
from rest_framework import serializers

from product.serializers import ProductSerializer

__author__ = u"linyuchen"
__doc__ = u""


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    product = ProductSerializer()