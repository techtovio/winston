from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.http import HttpResponseRedirect
from datetime import datetime
from django.conf import settings
from .models import Plan, Payment, EbookFlash
import requests
import string
import random, os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class PlanListView(ListView):
    model = Plan
    template_name = 'payments/plans.html'
    context_object_name = 'plans'

@require_POST
def initiate_payment(request):
    plan_id = request.POST.get('plan_id')
    payment_method = request.POST.get('payment_method')
    phone_number = request.POST.get('phone_number')
    country_code = request.POST.get('country_code')
    
    try:
        plan = Plan.objects.get(id=plan_id)
    except Plan.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid plan'}, status=400)

    # Create payment record
    payment = Payment.objects.create(
        user=request.user if request.user.is_authenticated else None,
        plan=plan,
        amount=plan.usd_price,
        currency='USD',
        phone_number=phone_number,
        country_code=country_code,
        payment_method=payment_method,
        guest_email=request.POST.get('email', ''),
        guest_name=request.POST.get('name', '')
    )

    # Process payment based on method
    if payment_method == 'MPESA':
        response = process_mpesa_payment(payment)
    elif payment_method == 'AIRTEL':
        response = None #process_airtel_payment(payment)
    else:
        response = None #process_card_payment(payment)

    if response.get('success'):
        payment.status = 'COMPLETED'
        payment.transaction_id = response.get('transaction_id')
        payment.save()
        return JsonResponse({'status': 'success', 'redirect_url': '/payment/success/'})
    else:
        payment.status = 'FAILED'
        payment.save()
        return JsonResponse({'status': 'error', 'message': response.get('message')}, status=400)

def process_mpesa_payment(payment):
    # Implement M-Pesa API integration
    # This is a mock implementation - replace with actual API calls
    try:
        # Example: Using Django MPesa library or direct API calls
        return {
            'success': True,
            'transaction_id': f'MPE{payment.id}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }

def payment_success(request):
    return render(request, 'payments/success.html')

def payment_failure(request):
    return render(request, 'payments/failure.html')


def ebookflash(request):
    user = request.user
    if user.is_authenticated:
        name = request.user.full_name()
        email = user.email
        amount = 300.00
        if request.method == 'POST':
            phone = request.POST['phone']
            country_code = request.POST['country_code']
            phone_no = f'{country_code}{phone}'
            print(phone_no)
            EbookFlash.objects.create(name=name, email=email, phone=phone_no, amount=amount, ref_id='hjjdsj')

@login_required(login_url="login")
def pay_mpesa(request):
    user = request.user
    if request.method == "POST":
        tel = request.POST['tel']
        amount = request.POST['amount']
        if tel and amount:
            reference = id_generator()
            ua = {
                    'Content-Type': 'application/json',
                    'Authorization':f'{os.getenv("HEDERA_AUTH")}',
                }
            url = 'https://backend.payhero.co.ke/api/v2/payments'
            
            data = {
                "amount": int(amount),
                "phone_number": f"{tel}",
                "channel_id": 947, 
                "provider": "m-pesa",
                "external_reference": f"{reference}",
                "callback_url": "https://quepter.co.ke/payment/mpesa/success/"
            }
            res = requests.post(url=url, json=data, headers=ua)
            js = res.json()
            print(js)
            if js['success'] == True:
                # Add EXception to handle Already Exists subscription
                #Transaction.objects.create(user=user, amount=amount, reference=reference)
                #Notification.objects.create(user=user, title="Payment Initiated", message=f"New payment of Kes {amount} has been initiated successfully, complete by entering your pin.")
                #messages.success(request, "Payment initialized successfuly, please complete it by entering your pin")
                messages.success(request, f"STK push initiated successfully")
            else:
                messages.warning(request, "An error occured while trying to process your payment, please try again later")
        else:
            messages.warning(request, "All Fields are requeired!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def mpesaSuccess(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            response_data = data.get('response', {})
            reference = response_data.get("ExternalReference")
            status = response_data.get("Status")
            payment = None#Transaction.objects.get(reference=reference)
            if status == "Success":
                payment.status = "Completed"
                user = payment.user
                #Notification.objects.create(user=user, title="Funds Have been Received Successfully", message=f"New fund deposit of Kes {payment.amount} has been received successfully")
                profile = None#Profile.objects.get(user=user)
                profile.funds += payment.amount
                payment.save()
                profile.save()
            else:
                #Notification.objects.create(user=user, title="Payment Cancelled", message=f"New payment of Kes {payment.amount} was not successful!")
                payment.status = "Cancelled"
                payment.save()
        except Exception as e:
            print(e)