from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, CartItem
import stripe
from django.conf import settings
from .currency_rates import get_exchange_rate
from decimal import *


class ItemDetailView(View):  # Подробная информация о товаре
    def get(self, request, id):
        item = get_object_or_404(Item, id=id)  # Проверка, существует ли товар
        if item is None:
            return HttpResponse("Item not found", status=404)
        currency = request.session.get('currency', 'USD')  # По умолчанию - доллар
        price_item = item.price
        # Рендерим HTML-страницу с формой
        currency_rate = Decimal(str(get_exchange_rate(currency)))
        price_item *= currency_rate

        # Подготовка символа валюты для отображения
        currency_symbol = {
            'EUR': '€',
            'USD': '$',
            'CNY': '¥',
            'RUB': '₽',
            'AED': 'AED',
            'KZT': '₸'
        }.get(currency, '$')  # Получаем символ по текущей валюте

        return render(request, 'shop/item_detail.html',
                      {'item': item, 'currency': currency, 'price_item': round(price_item, 2),
                       'currency_symbol': currency_symbol})

    def post(self, request, id):
        item = get_object_or_404(Item, id=id)
        if 'currency' in request.POST:  # Проверяем, какой параметр мы получили
            new_currency = request.POST.get('currency')
            request.session['currency'] = new_currency
            currency_rate = Decimal(str(get_exchange_rate(new_currency)))
            price_item = item.price

            # Применяем конвертацию к новой валюте
            price_item *= currency_rate

            # Возвращаем обновленную цену и валюту в JSON формате
            return JsonResponse({'price_item': round(price_item, 2), 'currency': new_currency})

        return JsonResponse({'error': 'Invalid request'}, status=400)  # Для некорректных запросов


class SuccessView(View):  # Перенаправление на страницу успешной оплаты через stripe
    def get(self, request):
        return render(request, 'shop/success.html')


class CancelView(View):  # Перенаправление на страницу не успешной оплаты через stripe
    def get(self, request):
        return render(request, 'shop/cancel.html')


class ItemListView(View):  # Получить список всех товаров
    def get(self, request):
        item_list = Item.objects.all()  # Получаем все товары
        paginator = Paginator(item_list, 5)  # Разделяем на страницы по 5 товаров
        page_number = request.GET.get('page', 1)  # Получаем номер страницы из GET-запроса
        page_obj = paginator.get_page(page_number)  # Получаем товары для текущей страницы

        currency = request.session.get('currency', 'USD')  # По умолчанию - доллар
        currency_rate = Decimal(str(get_exchange_rate(currency)))

        line_items = []
        for item in page_obj:
            price_item = item.price
            price_item *= currency_rate
            price_item = round(price_item, 2)
            line_items.append({'price_item': price_item,
                               'name': item.name,
                               'description': item.description,
                               'id': item.id})

        return render(request, 'shop/item_list.html',
                      {'page_obj': page_obj, 'currency': currency, 'line_items': line_items})

    def post(self, request):
        if 'currency' in request.POST:
            # Обработка изменения валюты
            new_currency = request.POST.get('currency')
            request.session['currency'] = new_currency
            return redirect('item_list')  # Перенаправляем обратно на страницу корзины
        return redirect('item_list')


class CartView(View):  # Получить список всех товаров в корзине
    def get(self, request):
        cart_items = CartItem.objects.all()  # Получаем все товары в корзине

        if not cart_items:
            return render(request, 'shop/cart_empty.html')  # Страница "Корзина пуста"
        currency = request.session.get('currency', 'USD')  # По умолчанию - доллар
        currency_rate = Decimal(str(get_exchange_rate(currency)))

        total_price = sum(item.item.price * item.quantity for item in cart_items)
        total_price *= currency_rate
        total_price = round(total_price, 2)  # Округляем после конвертации (ИТОГО:)

        line_items = []
        for item in cart_items:
            line_items.append({'price_item': round((item.item.price * currency_rate), 2),
                               'i': item,
                               'sum_price': round((item.item.price * currency_rate * item.quantity), 2)})

        return render(request, 'shop/cart.html', {
            'line_items': line_items,
            'total_price': total_price,
            'currency': currency,
            'currency_rate': currency_rate,
        })

    def post(self, request):
        if 'currency' in request.POST:
            # Обработка изменения валюты
            new_currency = request.POST.get('currency')
            request.session['currency'] = new_currency
            return redirect('cart')  # Перенаправляем обратно на страницу корзины

        # Обработка обновления количества или удаления товара
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')

        # Проверка нажатия кнопки "Удалить"
        if 'remove' in request.POST:
            # Удаление товара из корзины
            if cart_item_id:
                cart_item = get_object_or_404(CartItem, id=cart_item_id)
                cart_item.delete()  # Удаляем товар из корзины
            return redirect('cart')  # Перенаправляем обратно на страницу корзины

        # Обновление количества товара
        if (str(int(quantity)) == quantity) and cart_item_id and quantity is not None:
            quantity = int(quantity)  # Преобразуем количество в целое число

            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            if quantity <= 0:
                cart_item.delete()  # Удаляем товар из корзины
            else:
                cart_item.quantity = quantity  # Обновляем количество товара
                cart_item.save()  # Сохраняем изменения
            return redirect('cart')  # Перенаправляем обратно на страницу корзины

        return redirect('cart')  # Если ничего не произошло, просто перенаправляем


class AddToCartView(View):  # Возможность добавить товар в корзину
    def post(self, request, id):
        item = get_object_or_404(Item, id=id)
        quantity = int(request.POST.get('quantity', '1'))
        if quantity >= 1:
            # Получаем корзину
            cart_item, created = CartItem.objects.get_or_create(item=item)

            # Обновляем количество в корзине
            cart_item.quantity += quantity
            cart_item.save()
            return JsonResponse({'message': 'Товар успешно добавлен в корзину'}, status=200)
        else:
            return JsonResponse({'message': 'Ошибка добавления товара в корзину.'}, status=400)
        # return render(request,'shop/item_list.html')  # Если передали число меньше 1, просто перенаправляем обратно в список товаров


class CheckoutView(View):  # Логика работы передачи данных в страйп и формирования окна оплаты в stripe для корзины
    def post(self, request):
        items = CartItem.objects.all()
        if not items:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        currency = request.POST.get('currency')  # Получаем валюту из формы или используем USD
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # _USD if currency == 'usd' else settings.STRIPE_SECRET_KEY_EUR

        currency_rate = Decimal(str(get_exchange_rate(currency)))
        line_items = []
        for item in items:
            line_items.append({
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': item.item.name,
                        'description': item.item.description,
                    },
                    'unit_amount': int(item.item.price * currency_rate * 100),
                },
                'quantity': item.quantity,
            })

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri('/shop/success/'),
                cancel_url=request.build_absolute_uri('/shop/cancel/'),
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        return redirect(session.url)  # Перенаправляем пользователя к странице оплаты в Stripe


class SuccessView(View):  # Обработчик успешной оплаты
    def get(self, request):
        # Очищаем корзину после успешной оплаты
        CartItem.objects.all().delete()  # Очищаем все элементы корзины
        return render(request, 'shop/success.html')  # Отображаем страницу успешной оплаты
