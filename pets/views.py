from django.contrib.auth import logout, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

from .models import *
from django.db.models import ExpressionWrapper, F, FloatField
from django.core.paginator import Paginator
from .forms import AddToCartForm, LoginForm, RegisterForm, ReviewFormAuthenticated, ReviewFormAnonymous, ContactUsForm, ShippingAddressForm
from django.contrib import messages
from .utils import CartForAnonymous, CartForAuthenticatedUser
# Create your views here.

def index(request):
    tags = Tag.objects.all()
    products = Product.objects.order_by('-sales')[:6]
    context = {
        'tags': tags,
        'products': products,
        'title': 'Главная страница'
    }
    return render(request, 'pets/index.html', context)


class ProductFilter:
    def __init__(self, request, queryset):
        self.request = request
        self.queryset = queryset

    def filter_by_category(self):
        category = self.request.GET.get('category')
        if category:
            self.queryset = self.queryset.filter(category__id=category)
        return self

    def filter_by_brand(self):
        brand = self.request.GET.get('brand')
        if brand:
            self.queryset = self.queryset.filter(brand__id=brand)
        return self

    def filter_by_tag(self):
        tag = self.request.GET.get('tag')
        if tag:
            self.queryset = self.queryset.filter(tags__id=tag)
        return self

    def sort_by(self):
        sort = self.request.GET.get('sort')
        if sort:
            self.queryset = self.queryset.order_by(sort)
        return self

    def paginate(self):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(self.queryset, 9)
        return paginator.get_page(page)

    def filter_by_price(self):
        price = self.request.GET.get('price')

        self.queryset = self.queryset.annotate(
            discount_price=ExpressionWrapper(
                F('price') - F('price') * F('discount') / 100.0,
                output_field=FloatField()
            )
        )
        if price:
            if price == '0_10':
                self.queryset = self.queryset.filter(discount_price__lt=10)
            elif price == '10_20':
                self.queryset = self.queryset.filter(discount_price__gte=10, discount_price__lt=20)
            elif price == '20_30':
                self.queryset = self.queryset.filter(discount_price__gte=20, discount_price__lt=30)
            elif price == '30_40':
                self.queryset = self.queryset.filter(discount_price__gte=30, discount_price__lt=40)
            elif price == '40_50':
                self.queryset = self.queryset.filter(discount_price__gte=40, discount_price__lt=50)
            elif price == 'more_50':
                self.queryset = self.queryset.filter(discount_price__gt=50)
            elif price == 'skidka_bor':
                self.queryset = self.queryset.filter(discount__gt=0)
        return self

    def get_queryset(self):
        return self.queryset

def shop_view(request):
    products = Product.objects.all()
    product_filter = ProductFilter(request, products)
    products = (product_filter
                .filter_by_category()
                .filter_by_brand()
                .filter_by_tag()
                .filter_by_price()
                .sort_by()
                .get_queryset())
    products_count = len(products)

    paginated_products = product_filter.paginate()

    context = {
        'products': paginated_products,
        'title': 'Все товары',
        'products_count': products_count
    }
    return render(request, 'pets/shop.html', context)


def single_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        form = AddToCartForm(product)
        if request.user.is_authenticated:
            review_form = ReviewFormAuthenticated()
        else:
            review_form = ReviewFormAnonymous()
        reviews = Review.objects.filter(product=product)
        rating_list = [i.rating for i in reviews]
        rating = round(sum(rating_list) / len(rating_list), 1) if len(rating_list) > 0 else 0
        count_reviews = len(reviews)
        context = {
            'count_reviews': count_reviews,
            'product': product,
            'form': form,
            'review_form': review_form,
            'reviews': reviews,
            'title': f'{product.title}',
            'rating': rating,

        }
        return render(request, 'pets/single-product.html', context)
    except Exception as e:
        print(e)
        return render(request, 'pets/error.html')




# Сделать логику входа в аккаунт и регистрации
# В качестве страницы использовать готовый account.html
# Сделать context_processor для вывода формы регистрации
# На любую страницу

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():  # Если все данные в форме адекватные
            user = form.get_user()  # Получаем пользователя по данным из базы
            if user:
                login(request, user)

                return redirect('index')
            else:
                messages.error(request, 'Не верные имя пользователя или пароль')
                return redirect('account')
        else:
            messages.error(request, 'Не верные имя пользователя или пароль')
            return redirect('account')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('index')
        else:
            # Произошла ошибка
            return redirect('account')

def logout_view(request):
    logout(request)
    return redirect('index')


def account(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    context = {
        'login_form': login_form,
        'register_form': register_form,
        'title': 'Вход в аккаунт и регистрация'
    }
    return render(request, 'pets/account.html', context)


# Реализовать отзывы к товарам, которые может оставить любой пользователь
# Если не авторизован - просить имя и email
# Если авторизован - не просить


def save_review(request, pk):
    if request.user.is_authenticated:
        form = ReviewFormAuthenticated(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            product = Product.objects.get(pk=pk)
            review.product = product
            review.username = request.user.username
            review.email = request.user.email
            review.save()
            return redirect('product', product.slug)
    else:
        form = ReviewFormAnonymous(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            product = Product.objects.get(pk=pk)
            review.product = product
            review.save()
            return redirect('product', product.slug)


def wishlist_action(request, pk):
    product = Product.objects.get(pk=pk)
    user = request.user
    if WishList.objects.filter(product=product, user=user).exists():
        wish = WishList.objects.get(product=product, user=user)
        wish.delete()
    else:
        WishList.objects.create(product=product, user=user)
    return redirect(request.META.get('HTTP_REFERER'))


def wishlist(request):
    user = request.user
    wishs = WishList.objects.filter(user=user)
    products = [i.product for i in wishs]
    context = {
        'products': products,
        'title': "Избранное"
    }
    return render(request, 'pets/wishlist.html', context)




class SearchView(ListView):
    model = Product
    template_name = 'pets/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(title__icontains=word)
        return products


def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(data=request.POST)
        if form.is_valid():
            contactus = form.save()
            return redirect('contact')
    else:
        form = ContactUsForm()
    context = {
        'form': form
    }

    return render(request, 'pets/contact.html', context)


def to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':

        form = AddToCartForm(data=request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity', 1)
            color = form.cleaned_data.get('color', None)
            if color:
                color = color.color.title
            else:
                color = 'No'
            size = form.cleaned_data.get('size', None)
            if size:
                size = size.size.title
            else:
                size = 'No'
            if request.user.is_authenticated:
                CartForAuthenticatedUser(request, product_id, 'add', color, size, quantity)
            else:
                CartForAnonymous(request, product_id, 'add', color, size, quantity)
        else:
            print(form.errors)
    return redirect('product', product.slug)


def plus_minus(request, pk, action, color, size, quantity):
    if request.user.is_authenticated:
        CartForAuthenticatedUser(request, pk, action, color, size, quantity)
    else:
        CartForAnonymous(request, pk, action, color, size, quantity)
    return redirect('cart')


def cart(request):
    if request.user.is_authenticated:
        cart = CartForAuthenticatedUser(request)
    else:
        cart = CartForAnonymous(request)
    cart_info = cart.get_cart_info()
    return render(request, 'pets/cart.html', cart_info)

def clear(request):
    if request.user.is_authenticated:
        cart = CartForAuthenticatedUser(request)
    else:
        cart = CartForAnonymous(request)
    cart.clear()
    return redirect('cart')



def checkout(request):
    if request.user.is_authenticated:
        cart = CartForAuthenticatedUser(request)
    else:
        cart = CartForAnonymous(request)
    cart_info = cart.get_cart_info()
    context = {
        'shipping_form': ShippingAddressForm(),
        'title': 'Оформление заказа',
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'cart_total_price': cart_info['cart_total_price'],
        'order': cart_info['cart'],
        'products': cart_info['products']
    }
    if not request.user.is_authenticated:
        context['register_form'] = RegisterForm()
    return render(request, 'pets/checkout.html', context)


def process_checkout(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            user_cart = CartForAnonymous(request)
            register_form = RegisterForm(data=request.POST)
            if register_form.is_valid():
                user = register_form.save()
                user.save()
                login(request, user)
                # Логику как перекачать данные из неавтор корзины в авторизов
        else:
            user_cart = CartForAuthenticatedUser(request)
            user = request.user

        shipping_form = ShippingAddressForm(data=request.POST)
        if shipping_form.is_valid():
            shippingaddress = shipping_form.save(commit=False)
            shippingaddress.user = user
            shippingaddress.save()
        cart_info = user_cart.get_cart_info()
        cart_products = cart_info['products']

        line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': cart_product.product.title,
                    'description': cart_product.product.description
                },
                'unit_amount': int(cart_product.product.get_discount_price() * 100)
            },
            'quantity': cart_product.quantity
        } for cart_product in cart_products]
        import stripe
        STRIPE_PUBLISH_KEY = 'pk_test_51PYQY1RvY4iGghS1CIV3oPNQREkgds1Dvj3V2FqhbxKngM5noswtzuRRLKciQS6ZFK1HYFrSDNMhiqESaNahPERU005tT3bvin'
        STRIPE_SECRET_KEY = 'sk_test_51PYQY1RvY4iGghS1nWKS9mUUlKB2h5mRrdFjR1jjG78qxPIRRNKEBP4pubbcMpUMyEMIu7tBBpgWQ2lSAD9dr6si00Jl4JTo3G'
        stripe.api_key = STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url = request.build_absolute_uri(reverse('success')),
            cancel_url = request.build_absolute_uri(reverse('checkout'))
        )
        return redirect(session.url, 303)


def success_payment(request):
    cart = CartForAuthenticatedUser(request)
    cart.clear()
    return render(request, 'pets/thank-you.html')
