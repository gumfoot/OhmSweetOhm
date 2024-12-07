from django.shortcuts import render, redirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ProductImageForm
from django.contrib.auth import login, authenticate, logout
from .models import Category, Product, Wishlist,HotDeal,Store, Store_img,Pay,Cart,TopSelling,Product_detail,Product_images,Product_description,Accessories,CookieConsent,Slide,Video
from django.http import JsonResponse
from django.contrib import messages
from.forms import PayForm, AddToWishlistForm, UserMessageForm,NewUserForm,AccessoriesFilterForm,AccessoriesImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import jwt
from jwt.exceptions import PyJWTError
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .forms import ContactForm
from django.http import  JsonResponse
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.views import RedirectURLMixin
from django.core.exceptions import SuspiciousOperation
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token as get_csrf_token
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import ListView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import CookieGroup
from .util import (
    accept_cookies,
    decline_cookies,
    get_accepted_cookie_groups,
    get_declined_cookie_groups,
    get_not_accepted_or_declined_cookie_groups,
)
import warnings

from django import template
from django.urls import reverse
from django.utils.html import json_script

from .cache import all_cookie_groups as get_all_cookie_groups
from .conf import settings
from .util import (
    are_all_cookies_accepted,
    get_accepted_cookies,
    get_cookie_dict_from_request,
    get_cookie_string,
    get_cookie_value_from_request,
    get_not_accepted_or_declined_cookie_groups,
    is_cookie_consent_enabled,
)

def is_ajax_like(request: HttpRequest) -> bool:
    # legacy ajax, removed in Django 4.0 (used to be request.is_ajax())
    ajax_header = request.headers.get("X-Requested-With")
    if ajax_header == "XMLHttpRequest":
        return True

    # module-js uses fetch and a custom header
    return bool(request.headers.get("X-Cookie-Consent-Fetch"))


class CookieGroupListView(ListView):
    """
    Display all cookies.
    """

    model = CookieGroup


class CookieGroupBaseProcessView(RedirectURLMixin, View):
    def get_success_url(self):
        """
        If user adds a 'next' as URL parameter or hidden input,
        redirect to the value of 'next'. Otherwise, redirect to
        cookie consent group list
        """
        redirect_to = self.request.POST.get("next", self.request.GET.get("next"))
        if redirect_to and not url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        ):
            raise SuspiciousOperation("Unsafe open redirect suspected.")
        return redirect_to or reverse("cookie_consent_cookie_group_list")

    def process(self, request, response, varname):  # pragma: no cover
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        varname = kwargs.get("varname", None)
        if is_ajax_like(request):
            response = HttpResponse()
        else:
            response = HttpResponseRedirect(self.get_success_url())
        self.process(request, response, varname)
        return response


class CookieGroupAcceptView(CookieGroupBaseProcessView):
    """
    View to accept CookieGroup.
    """

    def process(self, request, response, varname):
        accept_cookies(request, response, varname)


class CookieGroupDeclineView(CookieGroupBaseProcessView):
    """
    View to decline CookieGroup.
    """

    def process(self, request, response, varname):
        decline_cookies(request, response, varname)

    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CookieStatusView(View):
    """
    Check the current accept/decline status for cookies.

    The returned accept and decline URLs are specific to this user and include the
    cookie groups that weren't accepted or declined yet.

    Note that this endpoint also returns a CSRF Token to be used by the frontend,
    as baking a CSRFToken into a cached page will not reliably work.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        accepted = get_accepted_cookie_groups(request)
        declined = get_declined_cookie_groups(request)
        not_accepted_or_declined = get_not_accepted_or_declined_cookie_groups(request)
        # TODO: change this csv URL param into proper POST params
        varnames = ",".join([group.varname for group in not_accepted_or_declined])
        data = {
            "csrftoken": get_csrf_token(request),
            "acceptUrl": reverse("cookie_consent_accept", kwargs={"varname": varnames}),
            "declineUrl": reverse(
                "cookie_consent_decline", kwargs={"varname": varnames}
            ),
            "acceptedCookieGroups": [group.varname for group in accepted],
            "declinedCookieGroups": [group.varname for group in declined],
            "notAcceptedOrDeclinedCookieGroups": [
                group.varname for group in not_accepted_or_declined
            ],
        }
        return JsonResponse(data)


#----------------------------------------------------------------------------------------------------------------------------------
# def product_list(request):
#     products = Product.objects.all()
#     name = request.GET.get('name')
#     gb = request.GET.get('gb')
#     price = request.GET.get('price')

#     if name:
#         products = products.filter(name__icontains=name)
#     if gb:
#         products = products.filter(gb=gb)
#     if price:
#         products = products.filter(price__lte=price)

#     data = []
#     for product in products:
#         data.append({
#             'name': product.name,
#             'gb': product.gb,
#             'price': product.price,
#         })

#     return JsonResponse(data, safe=False)

#----------------------------------------------------------------------------------------------------------------------------------------------

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_sum = sum(item.quantity * (item.product.new_price if item.product else item.accessory.new_price) for item in cart_items)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user_info = form.save()
            return redirect('index')
    else:
        form = ContactForm()
        
    context = {
        'form': form,
        'total_quantity': total_quantity,
        'total_sum': total_sum,
        'items': cart_items,
    }

    return render(request, 'main/checkout.html', context=context)


# def hot_deal(request):
#     return render(request, 'hot_deal.html', context={

#     })
def product(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(pr_name__icontains=search_query)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'main/product.html', context)
def store(request):
    images = Store_img.objects.all()
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')  # Get category from URL params
    product_name = request.GET.get('product_name', '')


    products = Product.objects.all().prefetch_related()

    if search_query:
        products = products.filter(pr_name__icontains=search_query)
    
    if category_id:  # Filter by category if provided
        products = products.filter(category_id=category_id)

    if product_name:  
        products = products.filter(pr_name__icontains=product_name)

    
    # Pagination
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()

    context = {
        'store': Store.objects.all().prefetch_related(),
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_id': category_id,  # Pass category_id to template
        'product_name': product_name,
        'total_products': products.count,
        'images': images,
    }
    return render(request, 'main/store.html', context)


@login_required
def add_to_wishlist(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    
        
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist.")
        return redirect('index')
    if request.user.is_authenticated:
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
        )
        if created:
            messages.success(request, "Product added to wishlist.")
        else:
            messages.info(request, "Product is already in your wishlist.")
    else:
        messages.error(request, "Please log in to add items to your wishlist.")
    return redirect('index')
@login_required
def add_to_cart_from_wishlist(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist.")
        return redirect('wishlist')
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Quantity updated in cart.")
        else:
            cart_item.quantity = 1
            cart_item.save()
            messages.success(request, "Product added to cart.")
        Wishlist.objects.filter(user=request.user, product=product).delete()
    else:
        messages.error(request, "Please log in to add items to cart.")
    return redirect('wishlist')


@login_required
def wishlist(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        wishlist_items = []
    context = {
        'categories': categories,
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count(),
    }
    return render(request, 'main/wishlist.html', context)
@login_required
def delete_from_wishlist(request, product_id):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    if request.method == 'POST':
        wishlist_item.delete()
        messages.success(request, "Item removed from wishlist.")
    return redirect('wishlist')

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_details = Product_detail.objects.filter(product=product)
    top_selling = TopSelling.objects.filter(product=product)
    
    pictures = Product_images.objects.filter(product=product)
    description = Product_description.objects.filter(product=product).first()
    wishlist = None
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(product=product, user=request.user)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.product = product
            new_image.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ProductImageForm()
    context = {
        'product': product,
        'product_details': product_details,
        'pictures': pictures,
        'description':description,
        'top_selling': top_selling,
        'wishlist': wishlist,
        'form': form,
    }
    return render(request, 'main/product.html', context)
def all_products(request):

    try:
        accessory_category = Category.objects.get(category_name='Accessories')  # Adjust based on your actual field name
    except Category.DoesNotExist:
        accessory_category = None
    
    # Filter products excluding those categorized as Accessory
    if accessory_category:
        products = Product.objects.exclude(category=accessory_category)
    else:
        products = Product.objects.all()  # Fallback if 'Accessory' category doesn't exist
    
    context = {
        'products': products
    }
    
    return render(request, 'main/all_products.html', context)

# def index(request):
#     top_selling_products = Product.objects.order_by('-num_sales')[:10]
#     if request.method == 'POST':
#         who = request.POST.get('who')
#         product_name = request.POST.get('product_name')
#         product_price = request.POST.get('product_price')
#         if who and product_name and product_price:
#             try:
#                 current_user = get_user_model().objects.get(username=who)
#                 Product.objects.create(who=current_user, name=product_name, price=product_price)
#             except get_user_model().DoesNotExist:
#                 pass
#         return redirect('index')
#     categories = Category.objects.all()
#     user_products = get_user_model().objects.all()
#     hot_deal = HotDeal.objects.first()
#     stores = Store.objects.all()
#     products = Product.objects.all()
#     pay = Pay.objects.first()
#     wishlist_items = Wishlist.objects.all()
#     if request.user.is_authenticated:
#         cart_items = Wishlist.objects.filter(user=request.user)
#     else:
#         cart_items = []
#     context = {
#         'products': products,
#         'cart': cart_items,
#         'user_products': user_products,
#         'pay': pay,
#         'wishlist_items': wishlist_items,
#         'stores': stores,
#         'categories': categories,
#         'hot_deal': hot_deal,
#         'top_selling_products': top_selling_products,
#     }
#     return render(request, 'main/index.html', context=context)


def index(request):
    videos = Video.objects.all()
    slide = Slide.objects.all()
    top_selling_products = Product.objects.order_by('-num_sales')[:10]
    
    categories = Category.objects.all()
    
    # Include "All Products" category
    all_category = {'id': 'all', 'category_name': 'All Products'}
    categories = [all_category] + list(categories)
    
    user_products = get_user_model().objects.all()
    hot_deal = HotDeal.objects.first()
    stores = Store.objects.all()
    products = Product.objects.all()
    pay = Pay.objects.first()
    wishlist_items = Wishlist.objects.all()
    
    if request.user.is_authenticated:
        cart_items = Wishlist.objects.filter(user=request.user)
    else:
        cart_items = []
    
    context = {
      
        'products': products,
        'cart': cart_items,
        'user_products': user_products,
        'pay': pay,
        'wishlist_items': wishlist_items,
        'stores': stores,
        'categories': categories,
        'hot_deal': hot_deal,
        'top_selling_products': top_selling_products,  
        'slide': slide,
        'videos': videos
    }
    return render(request, 'main/index.html', context=context)
@login_required
def add_to_cart(request, product_id):
    try:
        # Attempt to fetch a Product with the given product_id
        product = Product.objects.get(pk=product_id)
        if product:
            # Add the product to the cart
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, "Product quantity updated in cart.")
            else:
                cart_item.quantity = 1
                cart_item.save()
                messages.success(request, "Product added to cart.")
            return redirect('index')

    except Product.DoesNotExist:
        pass  # Handle if product with given ID doesn't exist

    # If Product does not exist, try handling an Accessory (assuming you have an Accessory model)
    try:
        # Attempt to fetch an Accessory with the given product_id
        accessory = Accessories.objects.get(pk=product_id)  # Assuming Accessory model exists
        if accessory:
            # Add the accessory to the cart
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                accessory=accessory
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, "Accessory quantity updated in cart.")
            else:
                cart_item.quantity = 1
                cart_item.save()
                messages.success(request, "Accessory added to cart.")
            return redirect('index')

    except Accessories.DoesNotExist:
        pass  # Handle if accessory with given ID doesn't exist

    # If neither Product nor Accessory found, display an error message
    messages.error(request, "Item does not exist.")
    return redirect('index')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_amount = 0

    for item in cart_items:
        if item.product:
            item.item_total = item.quantity * item.product.new_price
        elif item.accessory:
            item.item_total = item.quantity * item.accessory.new_price
        total_amount += item.item_total

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    return render(request, 'main/cart.html', context)

def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_amount = sum(item.quantity * (item.product.new_price if item.product else item.accessory.new_price) for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    return render(request, 'main/cart.html', context)

def update_cart(request, product_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        
        if action == 'increment':
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, 'Quantity increased.')
        
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request, 'Quantity decreased.')
            else:
                cart_item.delete()
                messages.success(request, 'Item removed from cart.')
        
        return redirect('cart')
    
    return redirect('cart')
    
@login_required
def delete_from_cart(request, product_id):
    cart_items = Cart.objects.filter(user=request.user, product_id=product_id)
    
    if cart_items.exists():
        for cart_item in cart_items:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request, "Quantity of item reduced.")
            else:
                cart_item.delete()
                messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in cart.")
    
    return redirect('cart')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = backend
            login(request, user, backend=backend)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("index")
    else:
        form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("index")
                    
                    next_url = request.POST.get('next') or request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('index')
                else:
                    messages.error(request, "Invalid username or password.")
            except PyJWTError:
                messages.error(request, "Error processing authentication token.")
                return redirect("login")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    context = {
        "login_form": form,
        "next": request.GET.get('next', '')
    }
    return render(request=request, template_name="main/login.html", context={"login_form": form})
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")
@login_required
def pay(request):
    quantity = 0
    summ = 0
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        print("price:{item.product.new_price}")
        quantity += item.quantity
        summ += item.product.new_price * item.quantity
    if request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            pay = form.save(commit=False)
            pay.user = request.user
            if 'cart_id' in request.session:
                try:
                    pay.cart = Cart.objects.get(id=request.session['cart_id'], user=request.user)
                    pay.save()
                    messages.info(request, "You have successfully paid.")
                    return redirect('index')
                except Cart.DoesNotExist:
                    messages.error(request, "Invalid cart ID.")
                    return redirect('index')
            else:
                messages.error(request, "Cart ID not found in session.")
                return redirect('index')
    else:
        form = PayForm()
    return render(request, 'main/payment.html', context={
        'form': form,
        'summ': summ,
        'quantity': quantity,
        'cart_items': cart_items
    })
def user_details(request):
    if request.method == "POST":
        form = UserMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Details submitted successfully.")
            return redirect('index')
    else:
        form = UserMessageForm()
    return render(request, 'main/address_after_payment.html', context={'form': form})

# def all_accessories(request):
#     try:
#         accessories_category = Category.objects.get(category_name='Accessories')
#         # Fetch products related to the 'Accessories' category
#         accessories = Product.objects.filter(category=accessories_category)
#     except Category.DoesNotExist:
#         accessories = Product.objects.none()
    
#     context = {
#         'accessories': accessories
#     }

#     return render(request, 'main/all_accessories.html', context)

@login_required
def accept_cookies(request):
    if request.method == "POST":
        CookieConsent.objects.update_or_create(user=request.user, defaults={'accepted_cookies': True})
        return redirect("index")  
    return render(request, "cookiegroup_list.html")

def my_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    
    if not CookieConsent.objects.filter(user=request.user, accepted_cookies=True).exists():
        return render(request, "accept_cookies.html")
    
    return render(request, "index.html")
# @login_required
# def add_to_wishlist(request, accessory_id):
#     try:
#         accessory = Accesorise.objects.get(pk=accessory_id)
#     except Accesorise.DoesNotExist:
#         messages.error(request, "Accessory does not exist.")
#         return redirect('index')
    
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             wishlist_item, created = Wishlist.objects.get_or_create(
#                 user=request.user,
#                 accessory=accessory,
#             )
#             if created:
#                 messages.success(request, "Accessory added to wishlist.")
#             else:
#                 messages.info(request, "Accessory is already in your wishlist.")
#         else:
#             messages.error(request, "Please log in to add items to your wishlist.")
#         return redirect('index')
#     else:
#         # Handle GET request, if necessary
#         messages.error(request, "Invalid request method.")
#         return redirect('index')

# @login_required
# def add_to_cart(request, product_id):
#     try:
#         product = Product.objects.get(pk=product_id)
#     except Product.DoesNotExist:
#         messages.error(request, "Product does not exist.")
#         return redirect('index')
    
#     if request.user.is_authenticated:
#         cart_item, created = Cart.objects.get_or_create(
#             user=request.user,
#             product=product,
#         )
#         if not created:
#             cart_item.quantity += 1
#             cart_item.save()
#             messages.success(request, "Quantity updated in cart.")
#         else:
#             cart_item.quantity = 1
#             cart_item.save()
#             messages.success(request, "Product added to cart.")
#     else:
#         messages.error(request, "Please log in to add items to cart.")
    
#     return redirect('index')

# @login_required
# def wishlist(request):
#     categories = Category.objects.all()  # Assuming you need categories for context
#     wishlist_items = Wishlist.objects.filter(user=request.user)
    
#     context = {
#         'categories': categories,
#         'wishlist_items': wishlist_items,
#         'wishlist_count': wishlist_items.count(),
#     }
#     return render(request, 'main/wishlist.html', context)


# @login_required
# def delete_from_wishlist(request, accessory_id):
#     wishlist_item = get_object_or_404(Wishlist, user=request.user, accessory_id=accessory_id)
    
#     if request.method == 'POST':
#         wishlist_item.delete()
#         messages.success(request, "Item removed from wishlist.")

#     return redirect('wishlist')



# def add_to_cart(request, accessory_id):
#     accessory = Accesorise.objects.get(id=accessory_id)
#     # Add accessory to cart logic
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart.items.add(accessory)
#     messages.success(request, 'Accessory added to cart.')
#     return redirect('all_accessories')

# def add_to_wishlist(request, accessory_id):
#     accessory = Accesorise.objects.get(id=accessory_id)
#     # Add accessory to wishlist logic
#     wishlist, created = Wishlist.objects.get_or_create(user=request.user)
#     wishlist.items.add(accessory)
#     messages.success(request, 'Accessory added to wishlist.')
#     return redirect('all_accessories')


register = template.Library()


@register.filter
def cookie_group_accepted(request, arg):
    """
    Filter returns if cookie group is accepted.

    Examples:
    ::

        {{ request|cookie_group_accepted:"analytics" }}
        {{ request|cookie_group_accepted:"analytics=*:.google.com" }}
    """
    value = get_cookie_value_from_request(request, *arg.split("="))
    return value is True


@register.filter
def cookie_group_declined(request, arg):
    """
    Filter returns if cookie group is declined.
    """
    value = get_cookie_value_from_request(request, *arg.split("="))
    return value is False


@register.filter
def all_cookies_accepted(request):
    """
    Filter returns if all cookies are accepted.
    """
    return are_all_cookies_accepted(request)


@register.simple_tag
def not_accepted_or_declined_cookie_groups(request):
    """
    Assignement tag returns cookie groups that does not yet given consent
    or decline.
    """
    return get_not_accepted_or_declined_cookie_groups(request)


@register.filter
def cookie_consent_enabled(request):
    """
    Filter returns if cookie consent enabled for this request.
    """
    return is_cookie_consent_enabled(request)


@register.simple_tag
def cookie_consent_accept_url(cookie_groups):
    """
    Assignement tag returns url for accepting given concept groups.
    """
    varnames = ",".join([g.varname for g in cookie_groups])
    url = reverse("cookie_consent_accept", kwargs={"varname": varnames})
    return url


@register.simple_tag
def cookie_consent_decline_url(cookie_groups):
    """
    Assignement tag returns url for declining given concept groups.
    """
    varnames = ",".join([g.varname for g in cookie_groups])
    url = reverse("cookie_consent_decline", kwargs={"varname": varnames})
    return url


@register.simple_tag
def get_accept_cookie_groups_cookie_string(request, cookie_groups):  # pragma: no cover
    """
    Tag returns accept cookie string suitable to use in javascript.
    """
    warnings.warn(
        "Cookie string template tags for JS are deprecated and will be removed "
        "in django-cookie-consent 1.0",
        DeprecationWarning,
    )
    cookie_dic = get_cookie_dict_from_request(request)
    for cookie_group in cookie_groups:
        cookie_dic[cookie_group.varname] = cookie_group.get_version()
    return get_cookie_string(cookie_dic)


@register.simple_tag
def get_decline_cookie_groups_cookie_string(request, cookie_groups):
    """
    Tag returns decline cookie string suitable to use in javascript.
    """
    warnings.warn(
        "Cookie string template tags for JS are deprecated and will be removed "
        "in django-cookie-consent 1.0",
        DeprecationWarning,
    )
    cookie_dic = get_cookie_dict_from_request(request)
    for cookie_group in cookie_groups:
        cookie_dic[cookie_group.varname] = settings.COOKIE_CONSENT_DECLINE
    return get_cookie_string(cookie_dic)


@register.simple_tag
def js_type_for_cookie_consent(request, varname, cookie=None):
    """
    Tag returns "x/cookie_consent" when processing javascript
    will create an cookie and consent does not exists yet.

    Example::

      <script type="{% js_type_for_cookie_consent request "social" %}"
      data-varname="social">
        alert("Social cookie accepted");
      </script>
    """
    # This approach doesn't work with page caches and/or strict Content-Security-Policies
    # (unless you use nonces, which again doesn't work with aggressive page caching).
    warnings.warn(
        "Template tags for use in/with JS are deprecated and will be removed "
        "in django-cookie-consent 1.0",
        DeprecationWarning,
    )
    enabled = is_cookie_consent_enabled(request)
    if not enabled:
        res = True
    else:
        value = get_cookie_value_from_request(request, varname, cookie)
        if value is None:
            res = settings.COOKIE_CONSENT_OPT_OUT
        else:
            res = value
    return "text/javascript" if res else "x/cookie_consent"


@register.filter
def accepted_cookies(request):
    """
    Filter returns accepted cookies varnames.

    .. code-block:: django

        {{ request|accepted_cookies }}

    """
    return [c.varname for c in get_accepted_cookies(request)]


@register.simple_tag
def all_cookie_groups(element_id: str):
    """
    Serialize all cookie groups to JSON and output them in a script tag.

    :param element_id: The ID for the script tag so you can look it up in JS later.

    This uses Django's core json_script filter under the hood.
    """
    groups = get_all_cookie_groups()
    value = [group.for_json() for group in groups.values()]
    return json_script(value, element_id)