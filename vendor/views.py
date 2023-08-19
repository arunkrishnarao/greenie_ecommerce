from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vendor
from order.models import Order, OrderItem
from product.models import Product, Category
from .forms import ProductForm, ProductEditForm, VendorEditForm
from django.db.models import Q
from core.models import Settings

# Converting Title into Slug
from django.utils.text import slugify
from cart.cart import Cart
from product.forms import AddToCartForm
from django.contrib.auth.decorators import user_passes_test
from django import forms
from django.contrib.auth.forms import UserCreationForm
import csv
from datetime import datetime

# Create your views here.
def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('core:home')
    else:
        form = UserCreationForm()

    return render(request, 'vendor/become_vendor.html', {'form': form})

@login_required
@user_passes_test(lambda u: not u.is_superuser)
def vendor_admin(request):

    core_frontpage = Settings.objects.all()[0:1]
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()
    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor/vendor_admin.html',
                  {'vendor': vendor, 'products': products, 'orders': orders, 'active': vendor.active, 'core_frontpage': core_frontpage})

@login_required
def add_product(request):
    vendor = request.user.vendor
    if vendor.active == False:
        return redirect('vendor:vendor-admin')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)  # Because we have not given vendor yet
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()  # finally save

            return redirect('vendor:vendor-admin')

    else:
        form = ProductForm

    return render(request, 'vendor/add_product.html', {'form': form})

@login_required
def edit_vendor(request):
    vendor = request.user.vendor
    if request.method == 'POST':
        form = VendorEditForm(request.POST, request.FILES)
        if form.is_valid():
            post_items = dict(request.POST.items())
            file_items = dict(request.FILES.items())

            vendor_prev_state = Vendor.objects.get(pk=vendor.id)
            vendor_new = form.save(commit=False)
            vendor_new.id = vendor_prev_state.id
            vendor_new.created_at = vendor_prev_state.created_at
            vendor_new.created_by = vendor_prev_state.created_by
            vendor_new.active = vendor_prev_state.active


            if file_items.get('image', '') == '':
                vendor_new.image = vendor_prev_state.image
            if post_items.get('name', '') == '':
                vendor_new.name = vendor_prev_state.name     
            if post_items.get('address', '') == '':
                vendor_new.address = vendor_prev_state.address
            if post_items.get('email', '') == '':
                vendor_new.email = vendor_prev_state.email
            if post_items.get('phone', '') == '':
                vendor_new.phone = vendor_prev_state.phone
            # vendor_new.created_by.save()
            vendor_new.save()
        return redirect('vendor:vendor-admin')
    else:
        form = VendorEditForm
    return render(request, 'vendor/edit_vendor.html', {'form': form})

@login_required
def edit_product(request):
    pid = request.GET.get('pid', '')
    vendor = request.user.vendor

    if vendor.active == False:
        return redirect('vendor:vendor-admin')

    if int(pid) not in [item.id for item in vendor.products.all()]:
        return redirect('vendor:vendor-admin')

    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES)

        if form.is_valid():
            post_items = dict(request.POST.items())
            file_items = dict(request.FILES.items())

            product_prev_state = Product.objects.get(pk=pid)
            product = form.save(commit=False)  # Because we have not given vendor yet
            product.id = pid
            product.category_id = product_prev_state.category_id
            product.title = product_prev_state.title
            product.price = product_prev_state.price
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)

            if file_items.get('image', '') == '':
                product.image = product_prev_state.image
            if post_items.get('description', '') == '':
                product.description = product_prev_state.description    
            product.save()  # finally save
        return redirect('vendor:vendor-admin')
    else:
        form = ProductEditForm
    return render(request, 'vendor/edit_product.html', {'form': form})

@login_required
def delete_product(request):
    pid = request.GET.get('pid', '')
    vendor = request.user.vendor
    if vendor.active == False:
        return redirect('vendor:vendor-admin')

    if int(pid) not in [item.id for item in vendor.products.all()]:
        return redirect('vendor:vendor-admin')
    else:
        product = Product.objects.get(id=int(pid))
        product.active = not product.active
        product.save()
        messages.success(request, "The selected product was disabled.")
    return redirect('vendor:vendor-admin')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def reports(request):
    if request.method == 'GET':
        start_date = request.GET.get('sd', '')
        end_date = request.GET.get('ed', '')
        report_type = request.GET.get('rt', '')
        print(start_date, end_date, report_type)
        if start_date != '' and end_date !='':
            if report_type == 'order':
                now = datetime.now()
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename=orderReport-{start_date}:{end_date}.csv'
                writer = csv.writer(response)
                writer.writerow(['Greenie Report - Auto Generated on' , str(now.strftime("%d/%m/%Y, %H:%M:%S"))])
                writer.writerow(['*', '*', '*', '*'])
                writer.writerow(['Start Date', start_date, 'End Date', end_date])    
                writer.writerow(['*', '*', '*', '*'])
                writer.writerow(['Order ID', 'Date', 'Customer Name', 'Customer Email', 'Customer Phone', 'Customer Address', 'Customer PIN', 'Customer City', 'Payment Type', 'Payment Status', 'Payment ID', 'Rayzorpay Order ID', 'Payment Amount', 'Latitude', 'Longitude'])
                for order in Order.objects.filter(created_at__range=[start_date, end_date]):
                    writer.writerow([str(order.id), str(order.created_at), str(order.full_name), str(order.email), str(order.phone), str(order.address), str(order.pincode), str(order.city), str(order.payment_info), str(order.status), str(order.payment_id), str(order.provider_order_id), str(order.amount), str(order.latitude), str(order.longitude) ])
                return response
            elif report_type == 'delivery':
                now = datetime.now()
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename=deliveryReport-{start_date}:{end_date}.csv'
                writer = csv.writer(response)
                writer.writerow(['Greenie Report - Auto Generated on' , str(now.strftime("%d/%m/%Y, %H:%M:%S"))])
                writer.writerow(['*', '*', '*', '*'])
                writer.writerow(['Start Date', start_date, 'End Date', end_date])    
                writer.writerow(['*', '*', '*', '*'])
                for order in Order.objects.filter(created_at__range=[start_date, end_date]):
                    writer.writerow(['Order ID', 'Date', 'Customer Name', 'Customer Email', 'Customer Phone', 'Customer Address', 'Customer PIN', 'Customer City', 'Payment Type', 'Payment Status', 'Payment ID', 'Rayzorpay Order ID', 'Payment Amount', 'Latitude', 'Longitude'])
                    writer.writerow([str(order.id), str(order.created_at), str(order.full_name), str(order.email), str(order.phone), str(order.address), str(order.pincode), str(order.city), str(order.payment_info), str(order.status), str(order.payment_id), str(order.provider_order_id), str(order.amount), str(order.latitude), str(order.longitude) ])
                    for item in order.items.all():
                        writer.writerow(['Order Item ID', 'Item ID', 'Item Name', 'Item Description', 'Item Quantity', 'Item Price', 'Vendor ID', 'Vendor Name', 'Vendor Address', 'Vendor Phone'])
                        writer.writerow([str(item.id), str(item.product.id), str(item.product.title), str(item.product.description), str(item.quantity), str(item.get_total_price()), str(item.vendor.id), str(item.vendor.name), str(item.vendor.address), str(item.vendor.phone)])
                    writer.writerow(['*', '*', '*', '*'])
                return response
        else:
            return render(request, 'vendor/reports.html', {})
    else:
        return render(request, 'vendor/reports.html', {})

def vendors(request):
    category = request.GET.get('category', None)
    if category:
        vendors = Vendor.objects.filter(Q(active=True)).filter(Q(products__category__exact=category))
    else:
        vendors = Vendor.objects.filter(Q(active=True))
    return render(request, 'vendor/vendors.html', {'vendors': vendors, 'category_id': category})

def vendor(request, vendor_id):
    # Create instance of Cart class
    cart = Cart(request)
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    category = request.GET.get('category', '')
    try:
        category_title = get_object_or_404(Category, id=category)
    except:
        category = None
        category_title = "All"

    # Check whether the AddToCart button is clicked or not
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            pid = form.cleaned_data['pid']
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=pid, quantity=quantity, update_quantity=True)
            messages.success(request, "Product was added to the cart.")
    if category:
        products = Product.objects.filter(Q(active=True)).select_related('vendor').filter(Q(vendor__active=True) and Q(vendor__id=vendor_id) & Q(category__exact=category))
    else:
        products = Product.objects.filter(Q(active=True)).select_related('vendor').filter(Q(vendor__active=True) and Q(vendor__id=vendor_id))
    return render(request, 'vendor/vendor.html', {'vendor': vendor, 'products': products, 'category': category_title, 'category_id': category})