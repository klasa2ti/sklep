from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
from .forms import ProfileForm, UserForm, AddItem
from django.contrib.auth import authenticate, login as login_auth, logout as logout_user
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Order, Profile, Merchant
from django.utils import timezone
import random

# Create your views here.


def index(request):
    products = Product.objects.filter(active=True).order_by('rating')[:5]
    return render(request, 'shop/home.html', {
        'ismerchant': request.user.groups.filter(name='merchant').exists(),
        'title': 'Giercownia',
        'barIco': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/WPVG_icon_2016.svg/1024px-WPVG_icon_2016.svg.png',
        'products': products
    })

def product(request, product_id):
    game = get_object_or_404(Product,pk=product_id)
    if request.user.is_authenticated:
        if Order.objects.filter(user=request.user.profile, product=game).exists():
            return render(request, 'shop/gameinfo.html', {
                'ismerchant': request.user.groups.filter(name='merchant').exists(),
                'title': game.name,
                'barIco': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/WPVG_icon_2016.svg/1024px-WPVG_icon_2016.svg.png',
                'game': game,
                'hasgame': True
            })
    return render(request, 'shop/gameinfo.html',{
        'ismerchant': request.user.groups.filter(name='merchant').exists(),
        'title': game.name,
        'barIco': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/WPVG_icon_2016.svg/1024px-WPVG_icon_2016.svg.png',
        'game': game
    })

def merchants(request):
    merchant_list = Merchant.objects.all()
    return render(request,'shop/merchantlist.html',{
            'ismerchant': request.user.groups.filter(name='merchant').exists(),
            'title': 'Wydawcy',
            'barIco': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/WPVG_icon_2016.svg/1024px-WPVG_icon_2016.svg.png',
            'list': merchant_list})

@user_passes_test(lambda u: u.is_anonymous)
def register(request):
    if request.method == 'POST':
        userFormTemplate = UserForm(request.POST)
        if userFormTemplate.is_valid():
            userFormTemplate.save()
            return redirect('index')
    else:
        userFormTemplate = UserForm()
    return render(request, 'shop/register.html', {
        'ismerchant': request.user.groups.filter(name='merchant').exists(),
        'userForm': userFormTemplate,
        'title': 'Załóż konto - Giercownia',
        'barIco': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/WPVG_icon_2016.svg/1024px-WPVG_icon_2016.svg.png',
    })

@user_passes_test(lambda u: u.is_anonymous)
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return redirect('index')
        else:
            return redirect('index')
    elif request.method == 'GET':
        return render(request,'shop/login.html',{
        'ismerchant': request.user.groups.filter(name='merchant').exists(),
        'title': 'Zaloguj się - Giercownia',
        'barIco': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/WPVG_icon_2016.svg/1024px-WPVG_icon_2016.svg.png',
    })

@login_required
def logout(request):
    logout_user(request)
    return redirect('index')

@user_passes_test(lambda u: u.groups.filter(name='merchant').exists())
@login_required
def product_add(request):
    if request.method == 'GET':
        addItemForm = AddItem()
        return render(request, 'shop/additem.html', {
                'ismerchant': request.user.groups.filter(name='merchant').exists(),
                'form': addItemForm,
                'title': 'Dodaj Produkt',
                'barIco': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/WPVG_icon_2016.svg/1024px-WPVG_icon_2016.svg.png',
            })
    if request.method == 'POST':
        merchant = get_object_or_404(Merchant, user=request.user.profile)
        updated_request = request.POST.copy()
        updated_request.update({'merchant_id': merchant.pk})
        form = AddItem(updated_request, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            addItemForm = AddItem(request.POST)
            return render(request, 'shop/additem.html', {
                'ismerchant': request.user.groups.filter(name='merchant').exists(),
                'form': addItemForm,
                'title': 'Dodaj Produkt',
                'barIco': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/WPVG_icon_2016.svg/1024px-WPVG_icon_2016.svg.png',
            })

@login_required
def product_buy(request, product_id):
    if request.method == 'GET':
        profile = get_object_or_404(Profile,user=request.user)
        game = get_object_or_404(Product,pk=product_id)
        if profile.funds >= game.price:
            profile.funds -= game.price
            order = Order(user=profile,product=game,created_at=timezone.now(),code=str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9)))
            profile.save()
            order.save()
            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')

@login_required
def mygames(request):
    if request.method == 'GET':
        gamelist = get_list_or_404(Order,user=request.user.profile)
        return render(request,'shop/gamelist.html', {
            'ismerchant': request.user.groups.filter(name='merchant').exists(),
            'title': 'Moje gry',
            'barIco': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/WPVG_icon_2016.svg/1024px-WPVG_icon_2016.svg.png',
            'games': gamelist})