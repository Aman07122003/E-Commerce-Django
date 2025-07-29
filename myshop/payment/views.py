import razorpay
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from orders.models import Order

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        amount = int(order.get_total_cost() * 100)  # Convert to paise

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1  # Auto capture
        })

        # Save order_id for later verification
        request.session['razorpay_order_id'] = razorpay_order['id']

        # Redirect to Razorpay checkout page
        return redirect(reverse('payment:razorpay_checkout'))

    return render(request, 'payment/process.html', {'order': order})


def razorpay_checkout(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    razorpay_order_id = request.session.get('razorpay_order_id')

    amount = int(order.get_total_cost())

    return render(request, 'payment/razorpay_checkout.html', {
        'order': order,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_key': settings.RAZORPAY_API_KEY,
        'amount': amount,
        'currency': 'INR',
        'callback_url': reverse('payment:verify')  # Verification endpoint
    })


@csrf_exempt
def verify_payment(request):
    """Verify Razorpay payment signature after successful payment"""
    if request.method == 'POST':
        data = json.loads(request.body)
        params_dict = {
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            # ✅ Payment verified successfully
            return JsonResponse({'message': 'Payment successful!'})
        except:
            return JsonResponse({'message': 'Payment verification failed'}, status=400)


# ✅ New Views for Completed & Canceled Pages
def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
