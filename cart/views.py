import json
from django. conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from .cart import Cart
from .forms import CheckoutForm
import razorpay
from order.utilities import checkout, notify_vendor, notify_customer
from order.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

class PaymentStatus:
    SUCCESS = "Success"
    FAILURE = "Failure"
    PENDING = "Pending"

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def order_payment(request):
     # If Checkout
    # print("____FLAG_____0")
    if request.method == 'POST':
        cart = Cart(request)
        form = CheckoutForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            pincode = form.cleaned_data['pincode']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            place = form.cleaned_data['city']
            payment_type = form.cleaned_data['payment_type']

            if payment_type == 'razorpay':
                razorpay_order = razorpay_client.order.create(
                    {
                        "amount" : float(cart.get_total_cost())*100,
                        "currency": settings.CURRENCY,
                        "payment_capture": '1'
                    })

                order = checkout(request, full_name, email, phone, address, pincode, place, cart.get_total_cost(), payment_type, provider_order_id=razorpay_order['id'], latitude=latitude, longitude=longitude)
                cart.clear()
                return render(request, "cart/payment.html", {
                        "id": razorpay_order['id'],
                        "callback_url": r"http://localhost:8080/cart/callback/",
                        "razorpay_key": settings.RAZORPAY_KEY_ID,
                        "currency": settings.CURRENCY,
                        "order": order,
                    })
            else:
                order = checkout(request, full_name, email, phone, address, pincode, place, cart.get_total_cost(), payment_type, latitude=latitude, longitude=longitude)
                cart.clear()
                return render(request, 'cart/success.html', {'order': order})
            # notify_customer(order)
            # notify_vendor(order)
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
    

# Create your views here.
def cart_detail(request):
    cart = Cart(request)
    form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart:cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart:cart')
        
    return render(request, 'cart/cart.html', {'form': form })

@csrf_exempt
def callback(request):
    if request.method == "POST":
        try:
            if "razorpay_signature" in request.POST:
                payment_id = request.POST.get("razorpay_payment_id", "")
                provider_order_id = request.POST.get("razorpay_order_id", "")
                signature_id = request.POST.get("razorpay_signature", "")
                order = Order.objects.get(provider_order_id=provider_order_id)
                order.payment_id = payment_id
                order.signature_id = signature_id
                order.save()
                if not razorpay_client.utility.verify_payment_signature(request.POST):
                    order.status = PaymentStatus.SUCCESS
                    order.save()
                    return render(request, "payment/success.html", context={"order":order})
                else:
                    order.status = PaymentStatus.FAILURE
                    order.save()
                    return render(request, "payment/failure.html", context={"order":order})
            else:
                payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
                provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
                order = Order.objects.get(provider_order_id=provider_order_id)
                order.payment_id = payment_id
                if order.payment_id==None:
                    order.payment_id='NO_ID_AVAIL'
                order.status = PaymentStatus.FAILURE
                order.save()
                return render(request, "payment/failure.html", context={"order":order})
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

def cancelled(request):
    return render(request, "payment/cancelled.html")
