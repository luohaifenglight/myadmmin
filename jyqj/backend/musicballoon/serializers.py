
from rest_framework import routers, serializers, viewsets
class EditSublevelSericalizer(serializers.Serializer):
    goodsquality = serializers.CharField(max_length=32)
    originalprice = serializers.CharField()
    title = serializers.CharField(max_length=64)
    freeshipping = serializers.CharField(max_length=32)
    shippingprice = serializers.CharField(max_length=32)
    images = serializers.ListField(child=serializers.CharField())
    mainimage = serializers.CharField(max_length=128, allow_null=True, allow_blank=True, required=False)
    buyprice = serializers.CharField(max_length=32)
    goodstype = serializers.CharField(max_length=32)
    desc = serializers.CharField(max_length=512)
    goodstags = serializers.ListField(child=serializers.CharField())
    city = serializers.CharField(max_length=20)
    area = serializers.CharField(max_length=20)