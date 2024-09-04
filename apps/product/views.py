from itertools import product

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
                  {'you_cant': you_cant, 'order_btn': order_btn, 'overall': overall, 'you_got': you_got, 'obj': data,
                   'lang': lang,
                   'chat_id': chat_id, 'point': user.point})


def order_view(req, pk):
    count = req.GET.get('count')
    chat_id = req.GET.get('chat_id')
    lang = req.GET.get('lang')
    total = req.GET.get('total')
    user = TelegramUser.objects.filter(chat_id=chat_id).first()
    qs = Store.objects.filter(region_id=user.region)
    stores = list()
    region = None
    conf_btn = None
    back_btn = None
    if lang == "uz":
        for i in qs:
            stores.append({'id': i.id, 'name': i.name_uz, 'longitude': i.longitude, 'latitude': i.latitude})
        region = user.region.name_uz
        back_btn = "Orqaga"
        conf_btn = "Tasdiqlash"
    elif lang == "ru":
        for i in qs:
            stores.append({'id': i.id, 'name': i.name_ru, 'longitude': i.longitude, 'latitude': i.latitude})
        region = user.region.name_ru
        back_btn = "Назад"
        conf_btn = "Подтверждение"
    return render(req, 'order.html',
                  {'region': region, 'pk': pk, 'stores': stores, 'count': count, 'lang': lang, 'chat_id': chat_id,
                   'total': total, 'back_btn': back_btn, 'conf_btn': conf_btn})


def order_confirm_view(req, pk):
    count = req.GET.get('count')
    chat_id = req.GET.get('chat_id')
    lang = req.GET.get('lang')
    p_id = req.GET.get('p_id')
    total = req.GET.get('total')
    user = TelegramUser.objects.filter(chat_id=chat_id).first()
    store = Store.objects.filter(id=pk).first()
    product = Product.objects.filter(id=p_id).first()
    store_dict = dict()
    product_dict = dict()
    warning_text = None
    if lang == "uz":
        store_dict['name'] = f"Dukon nomi: {store.name_uz}"
        store_dict['region'] = f"Viloyat: {store.region.name_uz}"
        product_dict['name'] = f"Mahsulot: {product.name_uz}"
        product_dict['count'] = f"Soni: {count}"
        warning_text = "5 kundan so'ng olishingiz mumkin"
        product_dict['price'] = f"Narxi: {product.price}"
        product_dict['total'] = f"Jami: {total}"
    elif lang == "ru":
        store_dict['name'] = f"Название магазина: {store.name_ru}"
        store_dict['region'] = f"Региональный: {store.region.name_ru}"
        product_dict['name'] = f"Продукт: {product.name_ru}"
        product_dict['count'] = f"Количество: {count}"
        warning_text = "Вы можете получить его через 5 дней"
        product_dict['price'] = f"Стоимость: {product.price}"
        product_dict['total'] = f"Итого: {total}"
    store_dict['phones'] = store.phones.all()
    return render(req, 'confirm-order.html',
                  {'warning_text': warning_text, 'store': store_dict, 'product': product_dict, 'chat_id': chat_id})
