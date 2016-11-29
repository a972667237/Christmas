from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import ExchangeGift, Gift, GiftSystem_user, GivenGift, ChangeResult
from django.views.generic import View
from .forms import ExchangeForm, GiftForm, UserForm, GivenForm
import json

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
            data = {'status': 'success', 'message':"您的礼物ID是:%s" % t.giftId}
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


def resultList(request):
    mygifts = Gift.objects.filter(own__stu_no="2015150003")
    return render(request, "resultList.html", locals())

def postWantType(request):
    if request.method == "POST":
        wantType = request.POST.getlist("wanttype[]")
        giftId = request.POST["giftId"]
        wanttypestring = ''
        for i in wantType:
            wanttypestring = wanttypestring + i + " "
        stu_no = "2015150003"
        gift = Gift.objects.get(giftId=giftId)
        if gift.own.stu_no == stu_no and gift.isExchange:
            try:
                a = gift.exchangegift.changeresult
                data = {"status": "resubmit", "message": "已绑定过想要的礼物类型"}
                return HttpResponse(json.dumps(data), content_type="application/json")
            except:
                if not wanttypestring:
                    data = {"status": "error", "message": "提交的类型为空"}
                    return HttpResponse(json.dumps(data), content_type="application/json")
                print (wanttypestring)
                ChangeResult.objects.create(exchangegift=gift.exchangegift, wangGiftType=wanttypestring)
                data = {"status": "success", "message": "成功添加想要的礼物类型"}
                return HttpResponse(json.dumps(data), content_type="application/json")
    data = {"status": "error", "message": "出了点不知道什么原因的错误呢= =、"}
    return HttpResponse(json.dumps(data), content_type="application/json")

# def postWantType(request):
#     if request.method == "POST":
#         wantType = request.POST["wanttype[]"]
#         giftId = request.POST["giftId"]
#         if not wantType or not giftId:
#             data = {"status": "resubmit", "message": "重复提交了"}
#             return HttpResponse(json.dumps(data), content_type="application/json")
#         stu_no = "2015150003"
#         gift = Gift.objects.get(giftId=giftId)
#         if gift.own.stu_no == stu_no and gift.isExchange:
#             thisTypeGifts = Gift.objects.filter(type=wantType, isUsed=False)
#             if thisTypeGifts:
#                 getGift = random.choice(thisTypeGifts)
#                 if gift.exchangegift.changeresult.wangGiftType or gift.exchangegift.changeresult.getGiftId:
#                     data = {"status": "error", "message": "你已经有礼物了"}
#                     return HttpResponse(json.dumps(data), content_type="application/json")
#                 gift.exchangegift.changeresult.wangGiftType = wantType
#                 getId = getGift.giftId
#                 gift.exchangegift.changeresult.getGiftId = getId
#                 gift.exchangegift.changeresult.save()
#                 data = {"status": "success", "message": "获取的礼物ID是" + getId}
#                 return HttpResponse(json.dumps(data), content_type="application/json")
#             data = {"status": "nogift", "message":"没有这种类别的礼物了"}
#             return HttpResponse(json.dumps(data), content_type="application/json")
#     data = {"status": "error", "message": "提交有误"}
#     return HttpResponse(json.dumps(data), content_type="application/json")
