import random # To get random products from the database
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Category, Product, Vendor
from django.db.models import Q
from .forms import AddToCartForm
from cart.cart import Cart

# Create your views here.
def product(request, category_slug, product_slug):
    # Create instance of Cart class
    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    # Check whether the AddToCart button is clicked or not
    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product.id, quantity=quantity, update_quantity=True)

            messages.success(request, "The product was added to the cart.")

            return redirect('product:product', category_slug=category_slug, product_slug=product_slug)            
    
    else:
        form = AddToCartForm()

    similar_products = list(product.category.products.exclude(id=product.id))


    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)
    
    context = {
        'product': product,
        'similar_products': similar_products,
        'form': form,
    }

    return render(request, 'product/product.html', context)


# def category(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)

#     # Check whether the AddToCart button is clicked or not
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = AddToCartForm(request.POST)

#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             print(form)
#             pid = form.cleaned_data['pid']
#             cart.add(product_id=pid, quantity=quantity, update_quantity=True)
#             messages.success(request, "The product was added to the cart.")      
#     else:
#         form = AddToCartForm()
#     return render(request,'product/category.html', {'category': category})


def search(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')
    try:
        category_title = get_object_or_404(Category, id=category)
    except:
        category = None
        category_title = "All"
        
    if category:
        products = Product.objects.filter((Q(title__icontains=query) | Q(description__icontains=query)) & Q(category__exact=category) & Q(active=True)).select_related('vendor').filter(Q(vendor__active=True))
    else:
        products = Product.objects.filter((Q(title__icontains=query) | Q(description__icontains=query)) & Q(active=True)).select_related('vendor').filter(Q(vendor__active=True))

    cart = Cart(request)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            pid = form.cleaned_data['pid']
            cart.add(product_id=pid, quantity=quantity, update_quantity=True)
            messages.success(request, "The product was added to the cart.")      
    else:
        form = AddToCartForm()
    return render(request, 'product/search.html', {'products':products, 'query': query, 'category': category_title, 'id': category})