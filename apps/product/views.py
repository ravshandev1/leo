from django.shortcuts import render
from .models import Category, Product
from user.models import TelegramUser, Store, StorePhone


def categories_view(req):
    qs = Category.objects.all()
    lang = req.GET.get('lang')
    chat_id = req.GET.get('chat_id')
    ls = list()
    title = None
    if lang == "uz":
        title = "Katolog"
        for i in qs:
            ls.append({'id': i.id, 'name': i.name_uz, 'icon': i.icon})
    elif lang == "ru":
        title = "Каталог"
        for i in qs:
            ls.append({'id': i.id, 'name': i.name_ru, 'icon': i.icon})
    return render(req, 'categories.html', {'qs': ls, 'title': title, 'lang': lang, 'chat_id': chat_id})


def products_view(req, cat_id):
    qs = Product.objects.filter(category_id=cat_id)
    lang = req.GET.get('lang')
    chat_id = req.GET.get('chat_id')
    cat_name = req.GET.get('name')
    ls = list()
    if lang == "uz":
        for i in qs:
            ls.append({'id': i.id, 'name': i.name_uz, 'image': i.images.first(), 'bonus': i.bonus, 'price': i.price})
    elif lang == "ru":
        for i in qs:
            ls.append({'id': i.id, 'name': i.name_ru, 'image': i.images.first(), 'bonus': i.bonus, 'price': i.price})
    return render(req, 'products.html', {'qs': ls, 'cat_name': cat_name, 'lang': lang, 'chat_id': chat_id})


def product_detail_view(req, pk):
    obj = Product.objects.filter(id=pk).first()
    lang = req.GET.get('lang')
    chat_id = req.GET.get('chat_id')
    user = TelegramUser.objects.filter(chat_id=chat_id).first()
    overall = None
    you_got = None
    order_btn = None
    you_cant = None
    data = dict()
    if lang == "uz":
        overall = "Jami: "
        you_got = f"Sizda {user.point} ball mavjud"
        order_btn = "Buyurtma berish"
        you_cant = "Sizda ball yetarli emas"
        data['name'] = obj.name_uz
        data['images'] = obj.images.all()
        data['bonus'] = obj.bonus
        data['price'] = obj.price
        data['description'] = obj.description_uz
    elif lang == "ru":
        overall = "Итого: "
        you_got = f"У вас есть {user.point} баллов"
        order_btn = "Заказать"
        you_cant = "У вас недостаточно баллов"
        data['name'] = obj.name_ru
        data['images'] = obj.images.all()
        data['bonus'] = obj.bonus
        data['price'] = obj.price
        data['description'] = obj.description_ru
    data['id'] = obj.id
    return render(req, 'product-detail.html',
                  {'you_cant': you_cant,'order_btn': order_btn, 'overall': overall, 'you_got': you_got, 'obj': data, 'lang': lang,
                   'chat_id': chat_id, 'point': user.point})


def order_view(req, pk):
    count = req.GET.get('count')
    chat_id = req.GET.get('chat_id')
    lang = req.GET.get('lang')
    user = TelegramUser.objects.filter(chat_id=chat_id).first()
    stores = Store.objects.filter(region_id=user.region)
    return render(req, 'order.html', {'pk': pk, 'stores': stores, 'count': count, 'lang': lang, 'chat_id': chat_id})
