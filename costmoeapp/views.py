from django.shortcuts import render
from .models import ProductPriceBySource
from collections import defaultdict
import json
from bs4 import BeautifulSoup
from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from django.contrib import messages  # Optional for error messages
from django.contrib.auth.hashers import check_password  # Use if password is hashed
from django.db.models import Q

@csrf_exempt
def login_a(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(username=username)

            # If passwords are hashed, use check_password:
            if user.password_hash == password:  # Replace this line if hashed
                # Successful login
                request.session['user_id'] = user.user_id
                request.session['username'] = user.username
                request.session['role'] = user.role
                return redirect('/home/')
            else:
                messages.error(request, 'Invalid password.')
        except Users.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'admin_p/signin.html')

def login_c(request):

    logout = "na"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(Q(username=username) | Q(email=username), role="costumer")

            # If passwords are hashed, use check_password:
            if user.password_hash == password:  # Replace this line if hashed
                # Successful login
                request.session['user_id'] = user.user_id
                request.session['username'] = user.username
                request.session['role'] = user.role
                return redirect('home3')
            else:
                messages.error(request, 'Invalid password.')
        except Users.DoesNotExist:
            messages.error(request, 'User not found.')
    context = {
        'logout' : logout
    }

    return render(request, 'admin_p/signin.html', context)

def logout_view(request):
    # Clear the session
    request.session.flush()
    
    # Optional: add a message
    messages.success(request, "You have been logged out.")
    
    # Redirect to login page (or wherever you want)
    return redirect('login_c')

# Create your views here.
def home(request):
    username = request.session.get('username', 'na') 
    context = { 
        'username' : username
    }
    return render(request, 'client/index.html', context)

# Create your views here.
def ecom(request):
    username = request.session.get('username', 'na') 
    context = { 
        'username' : username
    }
    return render(request, 'client/ecom.html', context)

# Create your views here.

def admin(request):
    products = ProductPriceBySource.objects.values('source_website', 'last_updated', 'min_price').order_by('last_updated')

    grouped_prices = defaultdict(list)
    last_updated_labels = []

    for product in products:
        grouped_prices[product['source_website']].append(float(product['min_price']))  # Convert Decimal to float
        if str(product['last_updated']) not in last_updated_labels:
            last_updated_labels.append(str(product['last_updated']))  # Ensure unique timestamps
    
    context = {
        "grouped_prices": json.dumps(dict(grouped_prices)),
        "last_updated_labels": json.dumps(last_updated_labels)
    }
    return render(request, 'admin_p/index.html', context)


import requests
from django.http import JsonResponse

def scrape_url(request):
    url = request.GET.get('url')  # Get the URL from the query parameters
    if not url:
        return JsonResponse({'status': 'error', 'message': 'URL is required.'})

    try:
        # Browserless API endpoint
        browserless_url = "https://chrome.browserless.io/scrape"
        
        # Send request to Browserless with the URL
        response = requests.post(browserless_url, json={"url": url, "headless": True})

        # Check if the response is successful
        if response.status_code == 200:
            html_content = response.text
            return JsonResponse({'status': 'success', 'html': html_content})
        else:
            return JsonResponse({'status': 'error', 'message': 'Error fetching page from Browserless.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
