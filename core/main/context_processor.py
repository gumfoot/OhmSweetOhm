from .models import Category

def categories_processor(request):
    """Global context processor to make categories available in all templates"""
    return {
        'categories': Category.objects.all()
    }