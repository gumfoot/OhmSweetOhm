from .models import Product,Category,HotDeal
from modeltranslation.translator import register, TranslationOptions



@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)  



@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('pr_name',)  



@register(HotDeal)
class HotDealTranslationOptions(TranslationOptions):
    fields = ('title','description',)  






