from .models import Category
def get_all_category(req):
    all_category=Category.objects.all()
    return{"all_category":all_category}