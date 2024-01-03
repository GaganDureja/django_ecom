# myproject/context_processors.py

from products.models import category, sub_category  # Adjust this import based on your app's structure

def global_categories(request):
    all_categories = category.objects.all()
    
    categories_with_subcategories = []
    for cat in all_categories:
        subcategories = sub_category.objects.filter(category=cat)
        categories_with_subcategories.append({'category': cat, 'subcategories': subcategories})

    return {
        'categories_with_subcategories': categories_with_subcategories,
    }
