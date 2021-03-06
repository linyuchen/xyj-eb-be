import uuid
from rest_framework.response import Response
from rest_framework.request import Request
from django.http.request import HttpRequest
from rest_api.rest_api_views import LycApiBaseView
from .serializers import ProductOrderSerializer, NewProductOrderSerializer, ProductOrderCommnetSerializer
from .models import ProductOrder, ProductOrderStatus, ProductOrderComment
from user.models import Address, User
from invite_code.models import InviteCode
from wechatpub.pay.api import WechatPay
from wechatpub.pay.models import WechatPayOrder
from wechatpub.api import WECHATPUB_API


class ProductOrdersApi(LycApiBaseView):
    model_class = ProductOrder
    serializer_class = ProductOrderSerializer
    http_method_names = ["get"]
    auth_http_method_names = ["get"]

    def get_queryset(self):
        user = self.request.user
        queryset = self.model_class.objects.filter(user=user)
        return queryset


class ProductOrderDetailApi(LycApiBaseView):
    model_class = ProductOrder
    serializer_class = ProductOrderSerializer
    http_method_names = ["get"]
    auth_http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        user: User = self.request.user
        order = self.model_class.objects.filter(user=user, id=kwargs.get("id")).first()
        if not order:
            return self.err_response("订单id有误")
        return Response(self.serializer_class(order).data)


class NewProductOrderApi(LycApiBaseView):

    model_class = ProductOrder
    serializer_class = NewProductOrderSerializer
    http_method_names = ["post"]
    auth_http_method_names = ["post"]

    def post(self, request: Request, *args, **kwargs):
        request.data["status"] = ProductOrderStatus.objects.get(name=ProductOrderStatus.STATUS_WAIT_PAY).id

        # 检查invite_code
        # invite_code = request.data.get("invite_code")
        # invite_code: InviteCode = InviteCode.objects.filter(code=invite_code).first()
        # if not invite_code:
        #     return self.err_response("邀请码有误")
        # if invite_code.is_used():
        #     return self.err_response("邀请码已失效")

        # 收货地址复制一份出来保存
        address = Address.objects.filter(id=request.data.get("address")).first()
        if not address:
            return self.err_response("收货地址id有误")
        address.id = None
        address.save()
        request.data["address"] = address.id
        request.user.default_address = address
        request.user.save()

        # 订单关联用户
        request.data["user"] = request.user.id

        response = super(NewProductOrderApi, self).post(request, *args, **kwargs)

        order: ProductOrder = None
        try:
            order = self.model_class.objects.filter(id=response.data.get("id")).first()
        except AttributeError:
            pass

        # 创建订单失败时删除地址副本
        if not order:
            address.delete()

        if order:

            # 支付方式
            product = order.product
            pay_way = request.data.get("pay_way")
            out_trade_no = uuid.uuid4().hex
            response.data["jssdk_config"] = WECHATPUB_API.jssdk_config("http://forward2.linyuchen.net/")
            WechatPay().create_order(order_summary=order.product.name, out_trade_no=out_trade_no,
                                     money=product.price, to_user=order.user.wxopenid, response_data=response.data,
                                     product_id=product.id)
            wechat_pay_order = WechatPayOrder(money=product.price)
            wechat_pay_order.save()
            order.wechat_pay_order = wechat_pay_order
            order.save()

        return response


class NewProductOrderCommentApi(LycApiBaseView):
    serializer_class = ProductOrderCommnetSerializer
    http_method_names = ["post"]
    model_class = ProductOrderComment
