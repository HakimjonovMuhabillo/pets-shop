from django.contrib.auth.models import User
from django.db import models
from colorfield.fields import ColorField

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class Brand(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    short_description = models.TextField(default='Short description')
    description = models.TextField(default='Main Description')
    information = models.TextField(default='Additional info')
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Всего 6 цифр и 2 из них после запятой
    discount = models.IntegerField(verbose_name='Процент скидки')
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, blank=True, null=True)
    sales = models.IntegerField(default=0)
    in_stock = models.IntegerField(default=10)

    def get_discount_price(self):
        disc_price = float(self.price) - float(self.price) * self.discount / 100
        return disc_price

    def get_first_image(self):
        if len(self.images.all()) > 0:
            return self.images.first().image.url
        else:
            return 'https://pubshamrock.com/wp-content/uploads/2023/04/skoro-zdes-budet-foto.jpg'

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=255)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.title

class Size(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', blank=True, null=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    username = models.CharField(max_length=255)
    email = models.EmailField()
    review = models.TextField()
    rating = models.IntegerField()
    image = models.ImageField(blank=True, null=True, upload_to='reviews')
    date = models.DateField(blank=True, null=True, auto_now_add=True)


# Создать систему избранного
# Модель - должна знать пользователя и товар
# Прописать логику добавления и удаления из избранного
# Прописать логику показа всех избранных на странице wishlist.html
# Прописать логику показа является ли товар в избранном в списке товаров
# Например если товар в избранном сердечко - черное, если нет - Белое
# В избранное может добавлять только вошедший в аккаунт пользователь


class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_cart_total_quantity(self):
        cart_products = self.cartproduct_set.all()
        total_quantity = sum([product.quantity for product in cart_products])
        return total_quantity

    @property
    def get_cart_total_price(self):
        cart_products = self.cartproduct_set.all()
        total_price = sum([product.get_total_price for product in cart_products])
        return total_price

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    color = models.CharField(default='No', max_length=255, null=True, blank=True)
    size = models.CharField(default='No', max_length=255, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)

    @property
    def get_total_price(self):
        total_price = (float(self.product.price) - float(self.product.price) * self.product.discount / 100) * self.quantity
        return total_price


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    country = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

