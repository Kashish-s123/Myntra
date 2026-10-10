from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import SignupForm
from .models import Product, Category, Wishlist, BagItem, Order, OrderItem


# ================= HOME =================

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
    })


# ================= PRODUCT LIST =================

from django.db.models import Q


def product_list(request):

    products = Product.objects.all()

    query = request.GET.get('q', '').strip()
    brand = request.GET.get('brand', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    sort = request.GET.get('sort', '').strip()

    # Search
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )

    # Brand Filter
    if brand:
        products = products.filter(
            brand__iexact=brand
        )

    # Minimum Price
    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    # Maximum Price
    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    # SORTING - ADD HERE
    if sort == 'low':
        products = products.order_by('price')

    elif sort == 'high':
        products = products.order_by('-price')

    # Brands for dropdown
    brands = Product.objects.values_list(
        'brand',
        flat=True
    ).distinct().order_by('brand')

    return render(request, 'product_list.html', {
        'products': products,
        'brands': brands,
        'query': query,
        'selected_brand': brand,
        'min_price': min_price,
        'max_price': max_price,
        'selected_sort': sort,
    })

# ================= PRODUCT DETAIL =================

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'product_detail.html', {
        'product': product,
    })


# ================= CATEGORY PRODUCTS =================

def category_products(request, id):
    category = get_object_or_404(Category, id=id)

    products = Product.objects.filter(category=category)

    return render(request, 'product_list.html', {
        'category': category,
        'products': products,
    })


# ================= SIGNUP =================

def signup_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Your account was created successfully.'
            )

            return redirect('profile')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form,
    })


# ================= LOGIN =================

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'You have logged in successfully.'
            )

            next_url = request.POST.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('home')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(request, 'login.html', {
        'next': request.GET.get('next', '')
    })


# ================= LOGOUT =================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        'You have logged out successfully.'
    )

    return redirect('home')


# ================= PROFILE =================

@login_required
def profile_view(request):
    return render(request, 'profile.html')


# ================= WISHLIST =================

@login_required
def wishlist_view(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('product')

    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items
    })


# ================= ADD TO WISHLIST =================

@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        if created:
            messages.success(
                request,
                "Product added to wishlist."
            )

        else:
            messages.info(
                request,
                "Product is already in your wishlist."
            )

    return redirect(
        request.POST.get('next', 'wishlist')
    )


# ================= REMOVE FROM WISHLIST =================

@login_required
def remove_from_wishlist(request, product_id):

    if request.method == "POST":

        Wishlist.objects.filter(
            user=request.user,
            product_id=product_id
        ).delete()

        messages.success(
            request,
            "Product removed from wishlist."
        )

    return redirect('wishlist')


# ================= bag PAGE =================

@login_required
def bag_view(request):

    bag_items = BagItem.objects.filter(
        user=request.user
    ).select_related('product')

    total_amount = sum(
        item.subtotal for item in bag_items
    )

    return render(request, 'bag.html', {
        'bag_items': bag_items,
        'total_amount': total_amount,
    })


# ================= ADD TO BAG =================

@login_required
def add_to_bag(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        if product.stock <= 0:

            messages.error(
                request,
                'This product is out of stock.'
            )

            return redirect(
                'product_detail',
                id=product.id
            )

        bag_item, created = BagItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:

            if bag_item.quantity < product.stock:

                bag_item.quantity += 1
                bag_item.save()

            else:

                messages.warning(
                    request,
                    'Maximum available stock reached.'
                )

                return redirect('bag')

        messages.success(
            request,
            'Product added to bag.'
        )

    return redirect('bag')


# ================= INCREASE BAG QUANTITY =================

@login_required
def increase_bag_quantity(request, item_id):

    if request.method == 'POST':

        bag_item = get_object_or_404(
            BagItem,
            id=item_id,
            user=request.user
        )

        if bag_item.quantity < bag_item.product.stock:

            bag_item.quantity += 1
            bag_item.save()

        else:

            messages.warning(
                request,
                'Maximum available stock reached.'
            )

    return redirect('bag')


# ================= DECREASE BAG QUANTITY =================

@login_required
def decrease_bag_quantity(request, item_id):

    if request.method == 'POST':

        bag_item = get_object_or_404(
            BagItem,
            id=item_id,
            user=request.user
        )

        if bag_item.quantity > 1:

            bag_item.quantity -= 1
            bag_item.save()

        else:

            bag_item.delete()

    return redirect('bag')


# ================= REMOVE FROM BAG =================

@login_required
def remove_from_bag(request, item_id):

    if request.method == 'POST':

        bag_item = get_object_or_404(
            BagItem,
            id=item_id,
            user=request.user
        )

        bag_item.delete()

        messages.success(
            request,
            'Product removed from bag.'
        )

    return redirect('bag')


# CHECKOUT AND ORDER 

@login_required
def checkout_view(request):

    bag_items = BagItem.objects.filter(
        user=request.user
    )

    if not bag_items.exists():
        messages.warning(
            request,
            'Your bag is empty.'
        )
        return redirect('bag')

    total_amount = sum(
        item.subtotal for item in bag_items
    )

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            total_amount=total_amount
        )

        for item in bag_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save()

        bag_items.delete()

        messages.success(
            request,
            'Order placed successfully.'
        )

        return redirect(
            'order_success',
            order_id=order.id
        )

    return render(request, 'checkout.html', {
        'bag_items': bag_items,
        'total_amount': total_amount
    })

# ORDER SUCCESS 

@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'order_success.html',
        {
            'order': order
        }
    )

# MY ORDER VIEW

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders.html',
        {
            'orders': orders
        }
    )