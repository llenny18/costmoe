from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'client/index.html')

# Create your views here.
def ecom(request):
    return render(request, 'client/ecom.html')