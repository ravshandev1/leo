from django.shortcuts import render
from .models import Category, Product
from user.models import TelegramUser


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
        title = "Russia"
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
    data = dict()
    if lang == "uz":
        data['name'] = obj.name_uz
        data['images'] = obj.images.all()
        data['bonus'] = obj.bonus
        data['price'] = obj.price
        data['description'] = obj.description_uz
    elif lang == "ru":
        data['name'] = obj.name_ru
        data['images'] = obj.images.all()
        data['bonus'] = obj.bonus
        data['price'] = obj.price
        data['description'] = obj.description_ru
    return render(req, 'product-detail.html', {'obj': data, 'lang': lang, 'chat_id': chat_id, 'point': user.point})


def order_view(req, pk):
    return render(req, 'order.html', {'pk': pk})
