from django.shortcuts import render
from product.models import Product
from core.models import Settings
from django.contrib.auth.decorators import user_passes_test, login_required


# Create your views here.
def frontpage(request):
    core_frontpage = Settings.objects.all()[0:1]
    newest_products = Product.objects.all()[0:8]
    context = {
        'newest_products': newest_products,
        'core_frontpage': core_frontpage,
    }
    return render(request, 'core/frontpage.html', context)


def contactpage(request):
    core_frontpage = Settings.objects.all()[0:1]
    context = {
        'core_frontpage': core_frontpage,
    }
    return render(request, 'core/contact.html', context)