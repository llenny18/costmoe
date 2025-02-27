from django.shortcuts import render
from .models import ProductPriceBySource
from collections import defaultdict
import json


# Create your views here.
def home(request):
    return render(request, 'client/index.html')

# Create your views here.
def ecom(request):
    return render(request, 'client/ecom.html')

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
    return render(request, 'admin/index.html', context)