from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import re
from typing import TypedDict
from django.core.validators import RegexValidator
from colorfield.fields import ColorField

# Create your models here.

class Slide(models.Model):

    image = models.ImageField(upload_to='slides/')
    alt_text = models.CharField(max_length=255)

    def __str__(self):
        return self.alt_text
    
class Video(models.Model):
    video_title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.video_title

    def video_url(self):
        if self.video_file:
            return self.video_file.url
        return None


class Category(models.Model):
    category_name = models.CharField(max_length=250)
    category_img = models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pr_name = models.CharField(max_length=255)
    pr_img = models.ImageField(upload_to='product_images/')
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount =  models.IntegerField(default=0)
    new = models.BooleanField(default=False)
    status = models.CharField('Enter new/old ', max_length=50,blank=True)
    num_sales = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.pr_name
    

class Product_detail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size=models.PositiveIntegerField('Product size (GB)')
    color = ColorField('Product color')  
    color_image = models.ImageField(upload_to='color_images/', blank=True, null=True) 

    def __str__(self):
        return f'{self.product}'

class Product_images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pictures=models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f'{self.product}'

class Product_description(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    in_stock = models.BooleanField(default=True)
    description=models.TextField('Product description')

    def __str__(self):
        return self.description


    
class All_products(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
    


class TopSelling(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return  f'{self.product}'


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product}'
    


class HotDeal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    


    

class Store_img(models.Model):
    image_title=models.CharField('title',max_length=250)
    image= models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image_title

class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True)
    description = models.TextField('Description', blank=True)
    img = models.ImageField(upload_to='images/')
    new_price = models.PositiveIntegerField('Enter new price', blank=True, default=0)
    old_price = models.PositiveBigIntegerField('Enter old price', blank=True, default=0)
    discount = models.IntegerField('Enter discount', blank=True, default=0)
    status = models.CharField('Enter new/old ', max_length=50,blank=True)

    def __str__(self):
        return self.name




    


class UserMessage(models.Model):
    
    name = models.CharField('Name', max_length=50)
    phone = models.CharField('Phone number', max_length=60)
    email = models.EmailField('Email')
    address = models.TextField('Address')
    message = models.TextField('Message')

    def __str__(self):
        return self.name
    

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name
    

class Product_page(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pictures=models.ImageField(upload_to='product_images/')


# class Accesorisse(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     img = models.ImageField(upload_to='product_images/')
#     new_price = models.DecimalField(max_digits=10, decimal_places=2)
#     other_price = models.PositiveIntegerField(default=0)
#     discount = models.IntegerField(default=0)
    
#     def __str__(self):
#         return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# class Accesorise_detail(models.Model):
#     product = models.ForeignKey(Accesorise, on_delete=models.CASCADE, default=None)
#     color = models.CharField('Product color', max_length=25)  

#     def __str__(self):
#         return f'{self.product} - {self.color}'


class Pay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    name = models.TextField('Name')
    card_number = models.PositiveIntegerField('Card number')
    hetevi_tver = models.PositiveIntegerField('Hetevi tver')
    phone_number = models.PositiveIntegerField('Phone number')
    email = models.EmailField('Email')

    def __str__(self):
        return self.name

class Accessories(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
   
   




class CookieConsent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accepted_cookies = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cookie consent for {self.user}"
    

COOKIE_NAME_RE = re.compile(r"^[-_a-zA-Z0-9]+$")
validate_cookie_name = RegexValidator(
    COOKIE_NAME_RE,
    _(
        "Enter a valid 'varname' consisting of letters, numbers"
        ", underscores or hyphens."
    ),
    "invalid",
)


def clear_cache_after(func):
    def wrapper(*args, **kwargs):
        from .cache import delete_cache

        return_value = func(*args, **kwargs)
        delete_cache()
        return return_value

    return wrapper


class CookieGroupDict(TypedDict):
    varname: str
    name: str
    description: str
    is_required: bool
    # TODO: should we output this? page cache busting would be
    # required if we do this. Alternatively, set up a JSONView to output these?
    # version: str


class BaseQueryset(models.query.QuerySet):
    @clear_cache_after
    def delete(self):
        return super().delete()

    @clear_cache_after
    def update(self, **kwargs):
        return super().update(**kwargs)


class CookieGroupManager(models.Manager.from_queryset(BaseQueryset)):
    def get_by_natural_key(self, varname):
        return self.get(varname=varname)


class CookieGroup(models.Model):
    varname = models.CharField(
        _("Variable name"),
        max_length=32,
        unique=True,
        validators=[validate_cookie_name],
    )
    name = models.CharField(_("Name"), max_length=100, blank=True)
    description = models.TextField(_("Description"), blank=True)
    is_required = models.BooleanField(
        _("Is required"),
        help_text=_("Are cookies in this group required."),
        default=False,
    )
    is_deletable = models.BooleanField(
        _("Is deletable?"),
        help_text=_("Can cookies in this group be deleted."),
        default=True,
    )
    ordering = models.IntegerField(_("Ordering"), default=0)
    created = models.DateTimeField(_("Created"), auto_now_add=True, blank=True)

    objects = CookieGroupManager()

    class Meta:
        verbose_name = _("Cookie Group")
        verbose_name_plural = _("Cookie Groups")
        ordering = ["ordering"]

    def __str__(self):
        return self.name

    @clear_cache_after
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @clear_cache_after
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def natural_key(self):
        return (self.varname,)

    def get_version(self) -> str:
        try:
            return str(self.cookie_set.all()[0].get_version())
        except IndexError:
            return ""

    def for_json(self) -> CookieGroupDict:
        return {
            "varname": self.varname,
            "name": self.name,
            "description": self.description,
            "is_required": self.is_required,
            # "version": self.get_version(),
        }


class CookieManager(models.Manager.from_queryset(BaseQueryset)):
    def get_by_natural_key(self, name, domain, cookiegroup):
        group = CookieGroup.objects.get_by_natural_key(cookiegroup)
        return self.get(cookiegroup=group, name=name, domain=domain)


class Cookie(models.Model):
    cookiegroup = models.ForeignKey(
        CookieGroup,
        verbose_name=CookieGroup._meta.verbose_name,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Name"), max_length=250)
    description = models.TextField(_("Description"), blank=True)
    path = models.TextField(_("Path"), blank=True, default="/")
    domain = models.CharField(_("Domain"), max_length=250, blank=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True, blank=True)

    objects = CookieManager()

    class Meta:
        verbose_name = _("Cookie")
        verbose_name_plural = _("Cookies")
        constraints = [(
            models.UniqueConstraint(fields=['name', 'description'], name='main_natural_key')

            ),
        ]
        ordering = ["-created"]

    def __str__(self):
        return "%s %s%s" % (self.name, self.domain, self.path)

    @clear_cache_after
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @clear_cache_after
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def natural_key(self):
        return (self.name, self.domain) + self.cookiegroup.natural_key()

    natural_key.dependencies = ["cookie_consent.cookiegroup"]

    @property
    def varname(self):
        return "%s=%s:%s" % (self.cookiegroup.varname, self.name, self.domain)

    def get_version(self):
        return self.created.isoformat()


ACTION_ACCEPTED = 1
ACTION_DECLINED = -1
ACTION_CHOICES = (
    (ACTION_DECLINED, _("Declined")),
    (ACTION_ACCEPTED, _("Accepted")),
)


class LogItem(models.Model):
    action = models.IntegerField(_("Action"), choices=ACTION_CHOICES)
    cookiegroup = models.ForeignKey(
        CookieGroup,
        verbose_name=CookieGroup._meta.verbose_name,
        on_delete=models.CASCADE,
    )
    version = models.CharField(_("Version"), max_length=32)
    created = models.DateTimeField(_("Created"), auto_now_add=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.cookiegroup.name, self.version)

    class Meta:
        verbose_name = _("Log item")
        verbose_name_plural = _("Log items")
        ordering = ["-created"]