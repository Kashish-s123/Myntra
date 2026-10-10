from django.urls import path
from . import views


urlpatterns = [

    # ================= HOME =================

    path(
        '',
        views.home,
        name='home'
    ),


    # ================= PRODUCTS =================

    path(
        'products/',
        views.product_list,
        name='product_list'
    ),

    path(
        'product/<int:id>/',
        views.product_detail,
        name='product_detail'
    ),


    # ================= CATEGORY =================

    path(
        'category/<int:id>/',
        views.category_products,
        name='category_products'
    ),


    # ================= AUTHENTICATION =================

    path(
        'signup/',
        views.signup_view,
        name='signup'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),


    # ================= WISHLIST =================

    path(
        'wishlist/',
        views.wishlist_view,
        name='wishlist'
    ),

    path(
        'wishlist/add/<int:product_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),

    path(
        'wishlist/remove/<int:product_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),


    # ================= BAG =================

    path(
        'bag/',
        views.bag_view,
        name='bag'
    ),

    path(
        'bag/add/<int:product_id>/',
        views.add_to_bag,
        name='add_to_bag'
    ),

    path(
        'bag/increase/<int:item_id>/',
        views.increase_bag_quantity,
        name='increase_bag_quantity'
    ),

    path(
        'bag/decrease/<int:item_id>/',
        views.decrease_bag_quantity,
        name='decrease_bag_quantity'
    ),

    path(
        'bag/remove/<int:item_id>/',
        views.remove_from_bag,
        name='remove_from_bag'
    ),


    # ================= CHECKOUT / ORDERS =================

    path(
        'checkout/',
        views.checkout_view,
        name='checkout'
    ),

    path(
        'order-success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'orders/',
        views.my_orders,
        name='my_orders'
    ),

]