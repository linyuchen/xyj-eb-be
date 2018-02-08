# -*- coding: UTF8 -*-
from django.conf.urls import url
from .views import ProductOrdersApi, NewProductOrderApi, ProductOrderDetailApi

urlpatterns = [
    url("^product/all$", ProductOrdersApi.as_view()),
    url("^product/(?P<id>\d+)$", ProductOrderDetailApi.as_view()),
    url("^product/new$", NewProductOrderApi.as_view())
]
