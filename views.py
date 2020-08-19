from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

# Create your views here.
from . import Checksum
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from payments.utils import VerifyPaytmResponse
import requests


def home(request):
	return HttpResponse("<html><a href='http://127.0.0.1:8000/payment'>PayNow</html>")
# AUTHENTICATION
@csrf_exempt
def payment(request):
	order_id = Checksum.__id_generator__()
	bill_amount = "60"
	data_dict = {
		'MID': settings.PAYTM_MERCHANT_ID,
		'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
		'WEBSITE': settings.PAYTM_WEBSITE,
		'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
		'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
		'MOBILE_NO': 'xxxxxxxxxxxxx',
		'EMAIL': 'xxxxxxxxxxxxxx@gmail.com',
		'CUST_ID': 'xxxxxxx',
		'ORDER_ID':order_id,
		'TXN_AMOUNT': bill_amount,
	} # This data should ideally come from database
	
	data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
	context = {
		'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
		'comany_name': settings.PAYTM_COMPANY_NAME,
		'data_dict': data_dict
	}

	return render(request, 'payments/payment.html', context)
	
#RESPONSE FROM THE PAYTM

@csrf_exempt
def response(request):

	resp = VerifyPaytmResponse(request)
	# 

	if resp['verified']:
		# save success details to db; details in resp['paytm']

		# return HttpResponse("<center><h1>Transaction Successful</h1><center>", status=200)
		return TemplateResponse(request, 'payments/success.html')
		
	else:
		# check what happened; details in resp['paytm']

		# return HttpResponse("<center><h1>Transaction Failed</h1><center>", status=400)

		

		# return HttpResponse("http://127.0.0.1:8000/payment/", status=400)

		return TemplateResponse(request, 'payments/failure.html')
		 # 
#TRANSACTION STATUS	
def success(request):
	return render(request, 'payments/success.html')

def failure(request):

	return render(request, 'payments/failure.html')
	
      
      
   
   
      
   

	# return render(request, 'payments/redirect.html', {})

# HttpResponse("<center><h1><html><a href='http://127.0.0.1:8000/payment'>PayNow</html></h1><center>", status=400)	# return redirect('http://127.0.0.1:8000/payment')





