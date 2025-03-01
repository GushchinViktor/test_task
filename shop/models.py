from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return self.name

# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)  # Связь с пользователем
#     items = models.ManyToManyField(Item, through='CartItem')  # Связь с товаром

class CartItem(models.Model):
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)  # Количество товаров