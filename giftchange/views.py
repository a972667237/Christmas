from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import Wechat_userSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from .serializers import ExchangeGiftSerializer
from .models import ExchangeGift, Gift, GiftSystem_user, GivenGift
from django.views.generic import View
from .forms import ExchangeForm, GiftForm, UserForm, GivenForm
import json
# Create your views here.
''' get account api here  '''
# class Wechat_View(APIView):
#     def get(self, request, format=None):
#         wechat_user = GiftSystem_user.objects.filter(stu_no="2015150006")
#         serialzer = Wechat_userSerializer(wechat_user, many=True)
#         return Response({"user_list": JSONRenderer().render(serialzer.data)})
#     def post(self, request, format=None):
#         serilizer = Wechat_userSerializer(data=request.data, many=True)
#         if serilizer.is_valid():
#             serilizer.save()
#             return Response(serilizer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serilizer.data, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ExchangeGift_View(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'addExchange.html'
#     def get(self, request):
#         serialzer = ExchangeGiftSerializer(ExchangeGift)
#         return Response({'serializer': serialzer})

class ExchangeView(View):
    def get(self, request):
        exchange = ExchangeForm()
        gift = GiftForm()
        current_user = GiftSystem_user.objects.get(stu_no="2015150003")
        user = UserForm()
        return render(request, 'addExchange.html', locals())
    def post(self, request):
        currentUser = get_object_or_404(GiftSystem_user, stu_no="2015150003")
        gifts = Gift.objects.filter(own__stu_no="2015150003")
        if len(gifts) > 2:
            data = {"status": "full", "message": u"您的礼物数目满了噢"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        exchange = ExchangeForm(request.POST)
        gift = GiftForm(request.POST)
        user = UserForm(request.POST)
        if not currentUser.phone or not currentUser.area:
            if user.is_valid():
                phone = user.cleaned_data['phone']
                area = user.cleaned_data['area']
            else:
                data = {"status": "error", "message": user.errors.values()}
                return HttpResponse(json.dumps(data), content_type="application/json")
            currentUser.area = area
            currentUser.phone = phone
            currentUser.save()
        if exchange.is_valid() and gift.is_valid():
            t = Gift.objects.create(
                name = gift.cleaned_data["name"],
                type = gift.cleaned_data["type"],
                description = gift.cleaned_data["description"],
                isAnonymous = gift.cleaned_data["isAnonymous"],
                giftId= currentUser.area + gift.cleaned_data["type"] + "{:0>5}".format(
                    len(Gift.objects.filter(own__area=currentUser.area)) + 1)
            )
            try:
                ExchangeGift.objects.create(
                    aimGroup = exchange.cleaned_data["aimGroup"],
                    gift = t
                )
            except:
                t.delete()
            t.own = currentUser
            t.save()
            data = {'status': 'success', 'message': "您的礼物ID是:%s" % t.giftId}
            return HttpResponse(json.dumps(data), content_type='application/json')
        exchange_message = [i for i in exchange.errors.values()]
        gift_message = [i for i in gift.errors.values()]
        data = {"status": "error", "message": exchange_message + gift_message}
        return HttpResponse(json.dumps(data), content_type="application/json")

class GivenView(View):
    def get(self, request):
        given = GivenForm()
        gift = GiftForm()
        current_user = GiftSystem_user.objects.get(stu_no="2015150003")
        user = UserForm()
        return render(request, "addGiven.html", locals())
    def post(self, request):
        currentUser = get_object_or_404(GiftSystem_user, stu_no="2015150003")
        gifts = Gift.objects.filter(own__stu_no="2015150003")
        if len(gifts) > 2:
            data = {"status": "full", "message": u"您的礼物数目满了噢"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        given = GivenForm(request.POST)
        gift = GiftForm(request.POST)
        user = UserForm(request.POST)
        if not currentUser.phone or not currentUser.area:
            if user.is_valid():
                phone = user.cleaned_data['phone']
                area = user.cleaned_data['area']
            else:
                data = {"status": "error","message": user.errors.values()}
                return HttpResponse(json.dumps(data), content_type="application/json")
            currentUser.area = area
            currentUser.phone = phone
            currentUser.save()
        if given.is_valid() and gift.is_valid():
            t = Gift.objects.create(
                name=gift.cleaned_data["name"],
                type=gift.cleaned_data["type"],
                description=gift.cleaned_data["description"],
                isAnonymous=gift.cleaned_data["isAnonymous"],
                giftId=currentUser.area + gift.cleaned_data["type"] + "{:0>5}".format(
                    len(Gift.objects.filter(own__area=currentUser.area)) + 1)
            )
            try:
                GivenGift.objects.create(
                    givenPerson=given.cleaned_data["givenPerson"],
                    givenAdress=given.cleaned_data["givenAdress"],
                    givenPhone=given.cleaned_data["givenPhone"],
                    gift=t
                )
            except:
                t.delete()
            t.own = currentUser
            t.isExchange = False
            t.save()
            data = {'status': 'success', 'message':"您的礼物ID是:%s" % t.giftId }
            return HttpResponse(json.dumps(data), content_type= 'application/json')
        given_message = [i for i in given.errors.values()]
        gift_message = [i for i in gift.errors.values()]
        data = {"status": "error", "message":  given_message + gift_message}
        return HttpResponse(json.dumps(data), content_type="application/json")

def giftList(request):
    gifts = Gift.objects.filter(own__stu_no="2015150003")
    gifts_count = 3 - len(gifts)
    return render(request, "giftList.html", locals())

def index(request):
    return render(request, 'index.html', locals())
