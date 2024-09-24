from .forms import RegisterForm

def get_form(request):
    return {
        'registerform': RegisterForm()
    }