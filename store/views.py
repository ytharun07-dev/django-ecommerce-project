from django.shortcuts import render,redirect, get_object_or_404
from .models import Product,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

# cart = {}


def add_to_cart(request, product_id):

        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        request.session['cart'] = cart

        return redirect('cart')




def cart_view(request):

    cart = request.session.get('cart', {})

    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []

    for product in products:
        quantity = cart[str(product.id)]
        total = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    return render(request, 'store/cart.html', {'cart_items': cart_items})



def checkout(request):

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('product_list')

    order = Order.objects.create(user=request.user)
    products = Product.objects.filter(id__in=cart.keys())

    for product in products:
        quantity = cart[str(product.id)]

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

    request.session['cart'] = {}

    return render(request, 'store/checkout_success.html', {'order': order})



def register(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username, password=password)

        return redirect('login')

    return render(request, 'store/register.html')


def login_view(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('product_list')

    return render(request, 'store/login.html')


def logout_view(request):

    logout(request)

    return redirect('product_list')


@login_required
def order_history(request):

    orders = Order.objects.filter(user=request.user)

    return render(request, 'store/order_history.html', {'orders': orders})