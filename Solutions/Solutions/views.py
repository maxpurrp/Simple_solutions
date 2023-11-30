from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpRequest
import stripe
import random
import string
import os

from .models import Item, Order

ORDER_DATA = {}


def add_in_order(request: HttpRequest, id):
    item = get_object_or_404(Item, id=id)
    user = request.COOKIES.get("order", None)
    if not user:
        user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(14))
        order = Order.objects.create(user=user,
                                     total_price=item.price)
        order.items.add(item.id)
    else:
        order = get_object_or_404(Order, user=user)
        order.total_price += item.price
        order.items.add(item.id)
        order.save()
    order_items = [elem.name for elem in order.items.all()]
    order_data = {"items": order_items,
                  "total_price": order.total_price}
    response = render(request, 'main/index.html', {'item': item,
                                                    "order": order_data})
    response.set_cookie("order", user)
    if user in ORDER_DATA.keys():
        if item.name in ORDER_DATA[user]:
            ORDER_DATA[user][item.name] += 1
        else:
            ORDER_DATA[user][item.name] = 1
    else:
        ORDER_DATA[user] = {item.name: 1}
    return response


def _buy_item(items):
    stripe.api_key = os.getenv('secret_key')
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        automatic_tax={'enabled': True},
        customer='cus_P6O9fkgtrE965W',
        customer_update={'shipping': 'auto', 'name': 'auto'},
        shipping_address_collection={'allowed_countries': ['RU']},
        mode='payment',
        discounts=[],
        success_url='https://yourwebsite.com/success',
        cancel_url='https://yourwebsite.com/cancel',
        )
    response = JsonResponse({"session_id": session.id})
    return response


def _buy_order(items, order: Order, user):
    stripe.api_key = os.getenv('secret_key')
    if order.discount:
        coupon = stripe.Coupon.create(
            percent_off=order.discount.amount,
            duration='repeating',
            duration_in_months=1,
        )
        discount = [{
            'coupon': coupon.id
        }]
    else:
        discount = []
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        automatic_tax={'enabled': True},
        tax_id_collection={"enabled": True},
        customer='cus_P6O9fkgtrE965W',
        customer_update={'shipping': 'auto', 'name': 'auto'},
        shipping_address_collection={'allowed_countries': ['RU']},
        mode='payment',
        discounts=discount,
        success_url='https://yourwebsite.com/success',
        cancel_url='https://yourwebsite.com/cancel',
        )
    response = JsonResponse({"session_id": session.id})
    response.delete_cookie('order')
    if order.discount:
        coupon.delete()
    ORDER_DATA.pop(user)
    return response


def get_session(request: HttpRequest, id):
    user = request.COOKIES.get('order', None)
    if user:
        items = []
        order = get_object_or_404(Order, user=user)
        for elem in order.items.all():
            count = ORDER_DATA[user][elem.name]
            items.append({
                'price_data': {
                    'currency': "usd",
                    'product_data': {
                        'name': elem.name,
                        'description': elem.description,
                    },
                    'unit_amount': int(elem.price * 100),
                },
                'quantity': count,
            })
    else:
        item = get_object_or_404(Item, id=id)
        items = [{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
            }]
        return _buy_item(items)
    return _buy_order(items, order, user)


def get_item(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'main/index.html', {'item': item})
