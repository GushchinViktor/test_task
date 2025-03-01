from django.urls import path
from .views import ItemDetailView, SuccessView, CancelView, ItemListView, CartView, AddToCartView, CheckoutView

urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),  # Устанавливаем список товаров на главной странице
    path('item/<int:id>/', ItemDetailView.as_view(), name='item_detail'),
    path('shop/success/', SuccessView.as_view(), name='payment_success'),
    path('shop/cancel/', CancelView.as_view(), name='payment_cancel'),
    path('cart/', CartView.as_view(), name='cart'),  # Маршрут для отображения корзины
    path('add_to_cart/<int:id>/', AddToCartView.as_view(), name='add_to_cart'),  # Маршрут для добавления товара в корзину
    path('checkout/', CheckoutView.as_view(), name='checkout'),  # Маршрут для оформления заказа
]