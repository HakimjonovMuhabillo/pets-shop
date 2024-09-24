from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class AddToCartForm(forms.Form):
    size = forms.ModelChoiceField(
        required=False,
        queryset=ProductSize.objects.none(),
        widget=forms.HiddenInput(),  # Скрываем стандартный выпадающий список
    )
    color = forms.ModelChoiceField(
        required=False,
        queryset=ProductColor.objects.none(),
        widget=forms.HiddenInput(),  # Скрываем стандартный выпадающий список
    )
    quantity = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'quantity',
                'name': 'quantity',
                'class': 'form-control input-number text-center p-2 mx-1',
                'value': '1'

            }
        )
    )
    def __init__(self, product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].queryset = ProductSize.objects.filter(product=product)
        self.fields['color'].queryset = ProductColor.objects.filter(product=product)
        self.fields['quantity'].widget.attrs['data-stock'] = product.in_stock



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Пароль'
    }))


class RegisterForm(UserCreationForm):
    username = forms.CharField( widget=forms.TextInput(attrs={
        'autofocus': False,
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Имя пользователя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Пароль'
    }), help_text="")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Подтвердите пароль'
    }), help_text="")

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Почта'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ReviewFormAuthenticated(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))
    rating = forms.ChoiceField(
        choices=[(1, ''), (2, ''), (3, ''), (4, ''), (5, '')],
        widget=forms.RadioSelect(attrs={
            'class': 'star-rating'
        })
    )
    review = forms.Field(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Review
        fields = ['image', 'rating', 'review']


class ReviewFormAnonymous(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))
    rating = forms.ChoiceField(
        choices=[(1, ''), (2, ''), (3, ''), (4, ''), (5, '')],
        widget=forms.RadioSelect(attrs={
            'class': 'star-rating'
        })
    )
    review = forms.Field(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Review
        fields = ['image', 'rating', 'review', 'username', 'email']

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control ps-3 me-3',
                'placeholder': 'Write Your Name Here'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control ps-3',
                'placeholder': 'Write Your Email Here'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control ps-3 me-3',
                'placeholder': 'Phone Number'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control ps-3 me-3',
                'placeholder': 'Write Your Subject Here'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control ps-3 me-3',
                'placeholder': 'Write Your Message Here',
                'style' : "height:150px;"
            }),
        }


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['country', 'address', 'city', 'state', 'zipcode', 'phone']
        widgets = {
            'country': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4',
                'placeholder': 'Country / Region *'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4',
                'placeholder': 'Street Address *'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4',
                'placeholder': 'Town / City *'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4',
                'placeholder': 'State *'
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4',
                'placeholder': 'Zip Code *'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4',
                'placeholder': 'Phone *'
            }),
        }
