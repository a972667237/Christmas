from rest_framework import serializers
from .models import GiftSystem_user, GivenGift, Gift, ExchangeGift, ChangeResult

class Wechat_userSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftSystem_user
        exclude = ["id"]

class GiftAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        exclude = ["id"]

class GivenGiftSerializer(serializers.ModelDurationField):
    class Meta:
        model = GivenGift
        exclude = ["id"]

class ExchangeGiftSerializer(serializers.ModelDurationField):
    class Meta:
        model = ExchangeGift
        exclude = ["id"]

class ChangeResultSerializer(serializers.ModelDurationField):
    class Meta:
        model = ChangeResult
        exclude = ["id"]