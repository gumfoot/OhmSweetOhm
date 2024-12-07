from django.urls import path
from . import views
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views



from .views import (
    CookieGroupAcceptView,
    CookieGroupDeclineView,
    CookieGroupListView,
    CookieStatusView,
)





urlpatterns=[
    path('',views.index,name='index'),
    path('product/',views.product,name='product'),
    path('products/', views.all_products, name='all_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('checkout/',views.checkout,name='checkout'),
    path('store/',views.store,name='store'),
    path('login/', views.login_request, name='login'),
    path('register/',views.register_request, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add_to_cart_from_wishlist/<int:product_id>/', views.add_to_cart_from_wishlist, name='add_to_cart_from_wishlist'),
    path('delete_from_wishlist/<int:product_id>/', views.delete_from_wishlist, name='delete_from_wishlist'),
    path('pay/', views.pay, name='pay'),
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('delete_from_cart/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), #instead of registration/password_reset and so on should be accounts/password_reset and so on to open a real password reset page written in html not just as django project 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
    path(
        "accept/",
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name="cookie_consent_accept_all",
    ),
    # TODO
    re_path(
        r"^accept/(?P<varname>.*)/$",
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name="cookie_consent_accept",
    ),
    # TODO: 
    re_path(
        r"^decline/(?P<varname>.*)/$",
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name="cookie_consent_decline",
    ),
    path(
        "decline/",
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name="cookie_consent_decline_all",
    ),
    path("status/", CookieStatusView.as_view(), name="cookie_consent_status"),
    path("", CookieGroupListView.as_view(), name="cookie_consent_cookie_group_list"),



]



