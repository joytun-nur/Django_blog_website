from .models import Category

def get_all_categories(rewuest):
    Categories = Category.objects.all()
    context = {
        "categories" : Categories
    }
    return context