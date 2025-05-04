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
from .models import Users, Products, SystemLogs, BestProductsPerGroup, ProductGroups, ProductChoose,Quotations
from django.contrib import messages  # Optional for error messages
from django.contrib.auth.hashers import check_password  # Use if password is hashed
from django.db.models import Q
from django.utils import timezone
import pymysql
import requests
import re
import json
import http.client
from bs4 import BeautifulSoup
from pprint import pprint
import hashlib
import random
import string
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import csv
from django.db.models import Avg, Count
from django.core.mail import send_mail
import random



def send_otp_email(request, email):
    request.session['otpnow'] = random.randint(100000, 999999)
    request.session['email'] = email
    otp = request.session.get('otpnow', 'na')
    send_mail(
        subject='Welcome to COSTMOE!',
        message=f'Registration Successful! Verify your account now! This is uour One Time Password is {otp}',
        from_email='your_email@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )


def everif(request):
    otp = str(request.session.get('otpnow', 'na'))
    email = request.session.get('email', 'na')

    if email == 'na':
        return redirect('logic_c')
    if request.method == 'POST':
        otp_inputted = str(request.POST.get('otp'))
        print(otp)
        print(otp_inputted)
        if otp == otp_inputted:
            user_v = Users.objects.get(email=email)
            user_v.is_verified = 1
            user_v.save()
            messages.success(request, 'Email verified Successfully! You can login now!')
            return redirect('login_c')
        else:
            messages.success(request, 'Wrong OTP')


    return render(request, 'e-verif.html')

def quotations(request):
        # Retrieve user_id from session (or set default if missing)
    user_id = request.session.get('user_id', 'na')
    username = request.session.get('username', 'na')
    if username == 'na':
        return redirect('login_c')
    quotations = Quotations.objects.filter(user_id=user_id)
    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']

        # Save the uploaded CSV file to the 'quotations' folder inside staticfiles
        fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'costmoeapp/static', 'quotations'))
        filename = fs.save(csv_file.name, csv_file)

        # Generate the file path
        file_path = fs.url(filename)

        # Read the CSV file using pandas
        try:
            # Insert data into Quotations model
            new_quotation = Quotations(
                user_id=user_id,  # Assign user ID if logged in
                file_name=filename,
                file_path=file_path,
                uploaded_at=pd.Timestamp.now()
            )
            new_quotation.save()  # Save the file metadata to the database

            # Process the CSV data (here you can include your ML model and data transformation)
            # products = df.to_dict(orient='records')  # Convert CSV to list of dictionaries
            # enriched_products = enrich_with_ml_insights(products)

            # Render the table in HTML with the enriched products
            return redirect('quotations')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'client/quotations.html', {'quotations' : quotations})

from decimal import Decimal


def analyze_csv(request, c_id):
    # Fetch the quotation object by ID
    try:
        quotations = Quotations.objects.get(quotation_id=c_id)
    except Quotations.DoesNotExist:
        return HttpResponse("Quotation not found.", status=404)
    
    # Construct the full local file path
    file_name = quotations.file_name
    file_path = os.path.join(settings.BASE_DIR, 'costmoeapp/static', 'quotations', file_name)
    
    try:
        # Ensure the file exists
        if not os.path.exists(file_path):
            return HttpResponse("CSV file not found.", status=404)

        # Read the CSV file
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header
            rows = [row for row in reader]  # Read the rest of the rows
        
        # Convert CSV rows to list of dictionaries
        products_data = []
        for row in rows:
            # Skip empty rows
            if not row or all(cell.strip() == '' for cell in row):
                continue
                
            # Create a dictionary mapping header names to row values
            product_dict = {}
            for i, field_name in enumerate(header):
                if i < len(row):
                    # Convert price and rating to numbers if possible
                    if field_name.lower() == 'price':
                        try:
                            product_dict[field_name] = float(row[i].replace(',', '').strip())
                        except (ValueError, TypeError):
                            product_dict[field_name] = 0.0
                    elif field_name.lower() == 'rating':
                        try:
                            product_dict[field_name] = float(row[i].strip())
                        except (ValueError, TypeError):
                            product_dict[field_name] = 0.0
                    else:
                        product_dict[field_name] = row[i]
                else:
                    product_dict[field_name] = ''
            
            # Map CSV headers to expected field names if needed
            field_mapping = {
                'Product Name': 'product_name',
                'Description': 'description',
                'Category': 'category',
                'Brand': 'brand',
                'Price': 'price',
                'Currency': 'currency',
                'Rating': 'rating',
                'Availability': 'availability',
                'Website': 'source_website',
                'URL': 'source_url',
                'Image URL': 'image_url'
            }
            
            # Create a new dictionary with standardized field names
            standardized_dict = {}
            for key, value in product_dict.items():
                # Standardize the field name if a mapping exists
                standard_key = field_mapping.get(key, key)
                # Also try to match by lowercase field name
                if standard_key not in field_mapping.values():
                    for original, standard in field_mapping.items():
                        if key.lower() == original.lower():
                            standard_key = standard
                            break
                
                standardized_dict[standard_key] = value
            
            # Add any missing required fields with default values
            for standard_field in ['product_name', 'price', 'rating', 'source_website', 'availability']:
                if standard_field not in standardized_dict:
                    if standard_field in ['price', 'rating']:
                        standardized_dict[standard_field] = 0.0
                    else:
                        standardized_dict[standard_field] = ''
            
            products_data.append(standardized_dict)
        
        # Now analyze the products with our function
        analyzed_products = analyze_products(products_data)

        # Print the analyzed_products to HTML
        print("Analyzed Products:")
        print(analyzed_products)  # Print to console for debugging
        
        # Pass the header, original rows, and analyzed products to the template
        return render(request, 'client/analyze_csv.html', {
            'header': header, 
            'rows': rows,
            'products': analyzed_products,  # Send analyzed products to template
            'quotation': quotations
        })

    except Exception as e:
        # Handle any unexpected errors
        import traceback
        error_details = traceback.format_exc()
        return HttpResponse(f"Error: {str(e)}<br><pre>{error_details}</pre>", status=500)



def analyze_products(products):
    """
    Analyzes product data and returns ONLY Top 3 products based on market demand score:
    - Rank 1, 2, 3 (highest to lowest)
    - Provides reasons to choose, site trust score, market demand score, price trend, and final conclusion.
    """

    # Site trust/weight score
    site_score_map = {
        'Amazon': 1.00, 'Shopee': 0.95, 'Lazada': 0.93, 'TikTok Shop': 0.88,
        'eBay': 0.85, 'AliExpress': 0.82, 'Rakuten': 0.80, 'Zalora': 0.78,
        'Carousell': 0.70, 'PhilGEPS': 0.65, 'BeautyMNL': 0.63, 'Citimart': 0.55,
        'Temu': 0.50, 'Galleon': 0.45
    }

    # Convert products to DataFrame
    df = pd.DataFrame(list(products))

    if df.empty:
        return []

    # Ensure numeric columns
    df['price'] = df.get('price', 0).apply(lambda x: float(x) if isinstance(x, Decimal) else float(x or 0))
    df['rating'] = df.get('rating', 0).apply(lambda x: float(x) if isinstance(x, Decimal) else float(x or 0))

    # Fill missing values
    df['price'] = df['price'].fillna(df['price'].mean())
    df['rating'] = df['rating'].fillna(3.0)
    df['source_website'] = df['source_website'].fillna('Unknown')
    df['availability'] = df['availability'].fillna('unknown')

    # Add site score
    df['site_score'] = df['source_website'].map(site_score_map).fillna(0.5)

    # Handle division by zero safely
    epsilon = 0.001
    max_price = df['price'].max() + epsilon
    max_rating = df['rating'].max() + epsilon

    # Normalized scores
    df['price_factor'] = 1 - (df['price'] / max_price)
    df['price_factor'] = df['price_factor'].clip(0.1, 1)

    df['rating_factor'] = df['rating'] / 5.0  # Scale rating to 0–1

    # Final Market Demand Score (Weighted)
    df['market_demand_score'] = (
        (df['rating_factor'] * 0.4) +
        (df['price_factor'] * 0.3) +
        (df['site_score'] * 0.3)
    ) * 100  # Scale to 0–100

    # Simulate price trend
    df['price_trend'] = np.random.choice(['increasing', 'stable', 'decreasing'], size=len(df))

    # Generate "Why Choose" text
    df['why_choose'] = df.apply(
        lambda row: f"This product has a high user rating of {row['rating']:.1f}, "
                    f"offered at an affordable ₱{row['price']:.2f}, and is listed on {row['source_website']} "
                    f"(trust score: {row['site_score']:.2f}). "
                    f"{'Currently available in stock.' if row['availability'] == 'in_stock' else 'Currently out of stock.'}",
        axis=1
    )

    # Generate Conclusion
    def generate_conclusion(row):
        if row['market_demand_score'] >= 80:
            return "Top Pick"
        elif row['market_demand_score'] >= 60:
            return "Recommended"
        elif row['market_demand_score'] >= 45:
            return "Consider with Caution"
        else:
            return "Low Priority"

    df['conclusion'] = df.apply(generate_conclusion, axis=1)

    # Sort by market demand score descending
    df = df.sort_values('market_demand_score', ascending=False)

    # Keep only Top 3
    df = df.head(3).copy()

    # Add explicit rank
    df['rank'] = range(1, len(df) + 1)

    # Return results
    return df.to_dict(orient='records')

# Site trust/weight score
site_score_map = {
    'Amazon': 1.00, 'Shopee': 0.95, 'Lazada': 0.93, 'TikTok Shop': 0.88,
    'eBay': 0.85, 'AliExpress': 0.82, 'Rakuten': 0.80, 'Zalora': 0.78,
    'Carousell': 0.70, 'PhilGEPS': 0.65, 'BeautyMNL': 0.63, 'Citimart': 0.55,
    'Temu': 0.50, 'Galleon': 0.45
}

# Dummy model training
def train_dummy_model():
    X = pd.DataFrame({
        'price': np.random.uniform(10, 500, 100),
        'rating': np.random.uniform(1, 5, 100),
        'site_score': np.random.uniform(0.4, 1.0, 100)
    })
    y = (X['price'] < 300) & (X['rating'] > 3.5) & (X['site_score'] > 0.7)
    model = LogisticRegression()
    model.fit(X, y.astype(int))
    return model

ml_model = train_dummy_model()

def enrich_with_ml_insights(products):
    df = pd.DataFrame(list(products))

    # Convert Decimals to floats
    df['price'] = df['price'].astype(float)
    df['rating'] = df['rating'].astype(float)

    # Fill missing
    df['price'] = df['price'].fillna(df['price'].mean())
    df['rating'] = df['rating'].fillna(3.0)
    df['source_website'] = df['source_website'].fillna('Unknown')

    # Add site score
    df['site_score'] = df['source_website'].map(site_score_map).fillna(0.5)

    # Market demand score
    df['market_demand_score'] = ((df['rating'] / df['price']) * 100) * df['site_score']

    # Simulate price trend
    df['price_trend'] = np.random.choice(['increasing', 'stable', 'decreasing'], size=len(df))

    # Predict success
    X_test = df[['price', 'rating', 'site_score']]
    df['predicted_success'] = ml_model.predict(X_test)

    # Final conclusion
    def generate_final_conclusion(row):
        demand = row['market_demand_score']
        trend = row['price_trend']
        site_score = row['site_score']

        if demand > 75 and site_score > 0.90 and trend == 'stable':
            return "Top Pick"
        elif demand > 50 and site_score > 0.80 and trend in ['stable', 'decreasing']:
            return "Recommended"
        elif demand > 40 and site_score > 0.60:
            return "Consider with Caution"
        else:
            return "Low Priority"

    df['final_conclusion'] = df.apply(generate_final_conclusion, axis=1)

    return df.to_dict(orient='records')



# View function to display best products and enrich them with ML insights
def best_products_view(request):
    # Retrieve user_id from session (or set default if missing)
    user_id = request.session.get('user_id', 'na')
    username = request.session.get('username', 'na')

    if username == 'na':
        return redirect('login_c')
    groups = ProductGroups.objects.filter(user_id=user_id)
    
    # Get products filtered by user_id
    products = BestProductsPerGroup.objects.filter(user_id=user_id).values('product_id', 'group_id', 'product_name', 'price', 'rating', 'availability', 'why_scored', 'last_updated', 'source_website', 'rank', 'source_url', 'status')

    # Enrich products with machine learning insights
    enriched_products = enrich_with_ml_insights(products)

    if request.method == 'POST':
        product_id = request.POST.get('p_id')
        new_choose = ProductChoose(
            user_id=user_id,
            product_id=product_id
        )
        new_choose.save()

            # Update the chosen product's status to "yes"
        try:
            chosen_product = Products.objects.get(product_id=product_id, user_id=user_id)
            chosen_product.status = 'yes'
            chosen_product.save()
        except Products.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found.'}, status=404)

            # Update all other products' status to "no"
        other_products = Products.objects.filter(user_id=user_id).exclude(product_id=product_id)
        other_products.update(status='no')        

        return redirect('analyze')
    
    # Render the analysis template with the enriched product data
    return render(request, 'client/analysis.html', {'products': enriched_products, 'groups' :groups, 'username' : username})


def generate_hashed_string():
    # Generate a random string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    # Hash the string using SHA-256 and return first 10 characters of the hex digest
    hash_object = hashlib.sha256(random_string.encode())
    hashed_string = hash_object.hexdigest()[:10]
    
    return hashed_string

@csrf_exempt
def login_a(request):
    logout = "na"
    is_admin = "yes"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(Q(username=username) | Q(email=username), role="admin")

            # If passwords are hashed, use check_password:
            if user.password_hash == password:  # Replace this line if hashed
                # Successful login
                request.session['user_id'] = user.user_id
                request.session['username'] = user.username
                request.session['role'] = user.role
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password.')
        except Users.DoesNotExist:
            messages.error(request, 'User not found.')
    context = {
            'logout' : logout,
            'is_admin': is_admin
        }
    return render(request, 'index_a.html', context)

def login_c(request):

    logout = "na"
    is_admin = "no"
    if request.method == 'POST':

        if "login" in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = Users.objects.get(Q(username=username) | Q(email=username), role="costumer", is_verified=1)

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
                messages.error(request, 'User not found or not verified.')

        elif "register" in request.POST:
            username = request.POST.get('username')
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Basic validation
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('register')  # Replace with your actual URL name

            # Check if user already exists
            if Users.objects.filter(Q(username=username) | Q(email=email)).exists():
                messages.error(request, 'Username or Email already taken.')
                return redirect('register')

            # Create new user
            new_user = Users(
                username=username,
                full_name=full_name,
                email=email,
                password_hash=password,  # Replace with make_password(password) if hashing
                role='costumer',
                created_at=timezone.now()
            )
            new_user.save()
            send_otp_email(request, email)

            messages.success(request, 'Registration successful. Please verify your account. If email not found, check in spam')
            return redirect('everif')  # Replace with your login URL name

    context = {
        'logout' : logout,
        'is_admin': is_admin
    }

    return render(request, 'index.html', context)


    


def register(request):
    logout = "na"
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')  # Replace with your actual URL name

        # Check if user already exists
        if Users.objects.filter(Q(username=username) | Q(email=email)).exists():
            messages.error(request, 'Username or Email already taken.')
            return redirect('register')

        # Create new user
        new_user = Users(
            username=username,
            full_name=full_name,
            email=email,
            password_hash=password,  # Replace with make_password(password) if hashing
            role='costumer',
            created_at=timezone.now()
        )
        new_user.save()

        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login_c')  # Replace with your login URL name
    context = {
            'logout' : logout
        }
    return render(request, 'admin_p/register.html', context)

def logout_view(request):
    role = request.session.get('role', 'na') 
    # Clear the session
    request.session.flush()
    
    # Optional: add a message
    messages.success(request, "You have been logged out.")
    if role == 'costumer':
        return redirect('login_c')      
    elif role == 'admin':
        return redirect('login_a')      

def market_differentiation_view(request):
    user_id = request.session.get('user_id', 'na')
    username = request.session.get('username', 'na')
    
    if username == 'na':
        return redirect('login_c')
    
        # Fetch all products
    products = BestProductsPerGroup.objects.all()

    # Grouping structure: { search_name: { website: score } }
    table_data = {}

    # Track for differentiations
    differentiations = {
        'single_most_expensive': [],
        'single_cheapest': [],
        'most_expensive_multiple': [],
        'cheapest_multiple': [],
        'zero_price_urls': [],
        'repricing_opportunities': []
    }

    # Collect websites
    all_websites = set()

    # Build the table
    for product in products:
        search = product.search_name
        website = product.source_website
        score = product.final_score
        price = product.price

        if search not in table_data:
            table_data[search] = {}

        table_data[search][website] = {
            'score': score,
            'price': price,
            'product_name': product.product_name,
            'source_url': product.source_url
        }

        all_websites.add(website)

        # Zero price
        if price == 0:
            differentiations['zero_price_urls'].append({
                'search_name': search,
                'website': website,
                'product_name': product.product_name,
                'source_url': product.source_url
            })

    all_websites = sorted(list(all_websites))

    # Find best product per search (highest score)
    best_products = {}

    for search, website_scores in table_data.items():
        best = max(website_scores.items(), key=lambda x: x[1]['score'])
        best_products[search] = {
            'product_name': best[1]['product_name'],
            'source_url': best[1]['source_url']
        }

        # Handle differentiations per search
        prices = [data['price'] for data in website_scores.values() if data['price'] is not None]
        if prices:
            min_price = min(prices)
            max_price = max(prices)

            cheapest = [w for w, d in website_scores.items() if d['price'] == min_price]
            most_expensive = [w for w, d in website_scores.items() if d['price'] == max_price]

            if len(cheapest) == 1:
                differentiations['single_cheapest'].append({'search_name': search, 'website': cheapest[0]})
            else:
                for w in cheapest:
                    differentiations['cheapest_multiple'].append({'search_name': search, 'website': w})

            if len(most_expensive) == 1:
                differentiations['single_most_expensive'].append({'search_name': search, 'website': most_expensive[0]})
            else:
                for w in most_expensive:
                    differentiations['most_expensive_multiple'].append({'search_name': search, 'website': w})

            # Repricing (same product across websites different prices)
            product_price_map = {}
            for website, data in website_scores.items():
                pname = data['product_name']
                if pname not in product_price_map:
                    product_price_map[pname] = []
                product_price_map[pname].append(data['price'])

            for pname, prices in product_price_map.items():
                if len(set(prices)) > 1:
                    differentiations['repricing_opportunities'].append({'search_name': search, 'product_name': pname})

    context = {
        'table_data': table_data,
        'all_websites': all_websites,
        'best_products': best_products,
        'differentiations': differentiations
    }
    return render(request, 'client/market_differentiation.html', context)



# Create your views here.
def home(request):
    group_id = generate_hashed_string()

    user_id = request.session.get('user_id', 'na') 
    username = request.session.get('username', 'na') 

    if request.method == 'POST':
        product_name1 = request.POST.get('product_name')
        product_name = product_name1.replace(" ", "%20")
        
        search_name = product_name1
        log_time = timezone.now() 

        # Insert the log into the database
        SystemLogs.objects.create(
            user_id=user_id,
            action=f"Searched for products of {product_name}",
            log_time=log_time 
        )
   

        value_query=product_name
        print(value_query)

        # DB config
        db_config = {
            "host": "mysql-costmoe.alwaysdata.net", 
            "user": "costmoe_user",
            "password": "hqaDY7FA",
            "database": "costmoe_db",
            "port": 3306
        }

        def is_duplicate(cursor, name):
            cursor.execute("SELECT 1 FROM products WHERE product_name = %s LIMIT 1", (name,))
            return cursor.fetchone() is not None

        connection = None
        cursor = None

        try:
            # Connect to DB
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()

            # 1. CAROUSELL
            payload_carousell = {
                'api_key': 'e3ebed373fb3872d8e955acec5e2fa23',
                'url': f'https://www.carousell.ph/search/{value_query}'
            }

            r = requests.get('https://api.scraperapi.com/', params=payload_carousell)
            match = re.search(r'"itemListElement":\s*(\[[\s\S]*?\])', r.text)

            if match:
                try:
                    item_list = json.loads(match.group(1))
                    print(f"Extracted {len(item_list)} Carousell products...")
                    # continue with inserting...
                except json.JSONDecodeError as e:
                    print("Failed to parse itemListElement:", e)
                    print("Sample problematic text:", match.group(1)[:500])
            else:
                print("Carousell itemListElement not found.")


            if match:
                item_list = json.loads(match.group(1))
                print(f"Extracted {len(item_list)} Carousell products...")

                for item in item_list:
                    name = item.get("name", "NA")
                    if is_duplicate(cursor, name):
                        print(f"Duplicate (Carousell): {name}")
                        continue

                    description = "NA"
                    category = "NA"
                    brand = "NA"
                    price = item.get("offers", {}).get("price", "NA").replace("PHP", "").strip()
                    currency = item.get("offers", {}).get("priceCurrency", "NA")
                    rating = "NA"
                    availability = "in_stock"
                    source_website = "Carousell"
                    source_url = item.get("url", "NA")
                    

                    insert_query = """
                    INSERT INTO products (
                        product_name, description, category, brand, price, currency,
                        rating, availability, source_website, source_url, user_id, group_id, search_name
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        name, description, category, brand, price, currency,
                        rating, availability, source_website, source_url, user_id, group_id, search_name
                    ))

                print("Carousell products inserted.")
            else:
                print("Carousell itemListElement not found.")

            # 2. EBAY
            search_url = f'https://www.ebay.ph/sch/i.html?_nkw={value_query}'

            payload_ebay = {
                'source': 'universal',
                'url': search_url,
                'render': 'html',
                'parse': 'false'
            }

            response = requests.post(
                'https://realtime.oxylabs.io/v1/queries',
                auth=('raigye0118_BlrZS', 'LoveGod0118+'),
                json=payload_ebay,
            )

            data = response.json()
            html_content = data.get('results', [{}])[0].get('content', '')

            if not html_content:
                print("No HTML content found in eBay response.")
            else:
                soup = BeautifulSoup(html_content, 'html.parser')
                items = soup.find_all("li", class_="s-item")

                ebay_count = 0
                for item in items:
                    title_tag = item.find("div", class_="s-item__title")
                    link_tag = item.find("a", class_="s-item__link")
                    image_tag = item.find("img", class_="s-item__image-img")
                    price_tag = item.find("span", class_="s-item__price")

                    title = title_tag.text.strip() if title_tag else None
                    link = link_tag['href'] if link_tag else None
                    price = price_tag.text.strip().replace("PHP", "").replace("₱", "").replace(",", "").strip() if price_tag else None
                    

                    if title and link:
                        if is_duplicate(cursor, title):
                            print(f"Duplicate (eBay): {title}")
                            continue

                        cursor.execute("""
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency,
                                rating, availability, source_website, source_url, user_id, group_id, search_name
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            title, 'NA', 'NA', 'NA', price or 'NA', 'PHP', 'NA',
                            'in_stock', 'eBay', link, user_id, group_id, search_name
                        ))
                        ebay_count += 1

                print(f"{ebay_count} eBay products inserted.")
                
            # 3. GALLEON.PH
            payload_galleon = {
                'api_key': 'e3ebed373fb3872d8e955acec5e2fa23',
                'url': f'https://www.galleon.ph/search?category-id=+&keyword={value_query}'
            }
            
            r_galleon = requests.get('https://api.scraperapi.com/', params=payload_galleon)
            
            # Extract the gph_products array
            galleon_match = re.search(r'"gph_products"\s*:\s*(\[\s*\{.*?\}\s*\])', r_galleon.text, re.DOTALL)
            
            if galleon_match:
                # Fix common JSON issues if needed
                array_str = galleon_match.group(1).replace('\\"', '"')
                
                try:
                    galleon_products = json.loads(array_str)
                    print(f"Extracted {len(galleon_products)} Galleon.ph products...")
                    
                    galleon_count = 0
                    for product in galleon_products:
                        name = product.get("name", "NA")
                        
                        if is_duplicate(cursor, name):
                            print(f"Duplicate (Galleon.ph): {name}")
                            continue
                        
                        # Extract relevant fields
                        description = product.get("description", "NA")
                        category = product.get("category", "NA")
                        brand = product.get("brand", "NA")
                        price = str(product.get("price", "NA")).replace("₱", "").replace(",", "").strip()
                        currency = "PHP"  # Assuming PHP as default for Galleon
                        rating = product.get("rating", "NA")
                        availability = "in_stock"
                        source_website = "Galleon.ph"
                        source_url = product.get("url", "NA")
                        
                        
                        # Insert into database
                        cursor.execute("""
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency,
                                rating, availability, source_website, source_url, user_id, group_id, search_name
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            name, description, category, brand, price, currency,
                            rating, availability, source_website, source_url, user_id, group_id, search_name
                        ))
                        galleon_count += 1
                        
                    print(f"{galleon_count} Galleon.ph products inserted.")
                except json.JSONDecodeError as e:
                    print("JSON decoding error for Galleon.ph products:", e)
            else:
                print("Galleon.ph products array not found.")

            # 4. BEAUTYMNL
            payload_beautymnl = {
                'api_key': 'e3ebed373fb3872d8e955acec5e2fa23',
                'url': f'https://beautymanilashop.com/search?q={value_query}'
            }
            
            r_beautymnl = requests.get('https://api.scraperapi.com/', params=payload_beautymnl)
            
            # Extract product variants
            beauty_match = re.search(r'"productVariants"\s*:\s*(\[\s*\{.*?\}\s*\])', r_beautymnl.text, re.DOTALL)
            
            if beauty_match:
                try:
                    variants = json.loads(beauty_match.group(1))
                    print(f"Extracted {len(variants)} BeautyMNL products...")
                    
                    beauty_count = 0
                    for variant in variants:
                        product = variant.get("product", {})
                        price = variant.get("price", {})
                        
                        name = product.get("title", "NA")
                        if is_duplicate(cursor, name):
                            print(f"Duplicate (BeautyMNL): {name}")
                            continue
                        
                        # Extract relevant fields
                        description = "NA"  # Not available in the variant data
                        category = "NA"     # Not available in the variant data
                        brand = product.get("vendor", "NA")
                        price_amount = price.get("amount", "NA")
                        currency = price.get("currencyCode", "PHP")
                        rating = "NA"       # Not available in the variant data
                        availability = "in_stock"
                        source_website = "BeautyMNL"
                        source_url = f"https://beautymanilashop.com{product.get('url', '')}"
                        
                        
                        # Insert into database
                        cursor.execute("""
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency,
                                rating, availability, source_website, source_url, user_id, group_id, search_name
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            name, description, category, brand, price_amount, currency,
                            rating, availability, source_website, source_url, user_id, group_id, search_name
                        ))
                        beauty_count += 1
                        
                    print(f"{beauty_count} BeautyMNL products inserted.")
                except json.JSONDecodeError as e:
                    print("JSON decoding error for BeautyMNL products:", e)
            else:
                print("BeautyMNL productVariants array not found.")
                
            # 5. RAKUTEN
            payload_rakuten = {
                'api_key': 'e3ebed373fb3872d8e955acec5e2fa23',
                'url': f'https://www.rakuten.com/search?term={value_query}'
            }
            
            r_rakuten = requests.get('https://api.scraperapi.com/', params=payload_rakuten)
            soup_rakuten = BeautifulSoup(r_rakuten.text, 'html.parser')
            
            # Find all product titles
            titles = soup_rakuten.find_all('span', class_='css-1qsz6u0')
            
            if titles:
                print(f"Found {len(titles)} Rakuten products...")
                
                rakuten_count = 0
                for title_tag in titles:
                    try:
                        # Get the product title
                        title = title_tag.text.strip()
                        
                        if is_duplicate(cursor, title):
                            print(f"Duplicate (Rakuten): {title}")
                            continue
                        
                        # Navigate upward to get the full product container
                        product_container = title_tag.find_parent('a')
                        
                        # Find price near this container
                        price_tag = product_container.find('span', class_='css-35g9f0')
                        price = price_tag.text.strip().replace('$', '').replace(',', '') if price_tag else "NA"
                        
                        # Find seller
                        seller_tag = product_container.find('span', class_='css-7077jz')
                        seller = seller_tag.text.strip() if seller_tag else "NA"
                        
                        # Get product URL
                        product_url = product_container['href'] if product_container else "NA"
                        
                        
                        # Insert into database
                        cursor.execute("""
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency,
                                rating, availability, source_website, source_url, user_id, group_id, search_name
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            title, 'NA', 'NA', seller, price, 'USD',
                            'NA', 'in_stock', 'Rakuten', product_url, user_id, group_id, search_name
                        ))
                        rakuten_count += 1
                        
                    except Exception as e:
                        print(f"Error parsing Rakuten product: {e}")
                        
                print(f"{rakuten_count} Rakuten products inserted.")
            else:
                print("No Rakuten products found.")
                
            # 6. SHOPEE
            # Using a different API (RapidAPI)
            try:
                # Set up connection to RapidAPI
                conn = http.client.HTTPSConnection("shopee-scraper1.p.rapidapi.com")
                
                payload = json.dumps({
                    "url": f"https://shopee.ph/search?keyword={value_query}"
                })
                
                headers = {
                    'x-rapidapi-key': "1b9956b92fmsh6a189d0e32e8631p131a58jsnbae6ad5adfa8",
                    'x-rapidapi-host': "shopee-scraper1.p.rapidapi.com",
                    'Content-Type': "application/json"
                }
                
                conn.request("POST", "/", body=payload, headers=headers)
                
                res = conn.getresponse()
                data = res.read()
                
                # Decode and parse JSON
                parsed_data = json.loads(data.decode("utf-8"))
                
                # Extract 'items' array
                items = parsed_data.get("items", [])
                
                print(f"Extracted {len(items)} Shopee products...")
                
                shopee_count = 0
                for item in items:
                    basic_info = item.get('item_basic', {})
                    if basic_info:
                        # Format product name
                        name = basic_info.get('name', 'NA')
                        
                        if is_duplicate(cursor, name):
                            print(f"Duplicate (Shopee): {name}")
                            continue
                        
                        # Convert price from Shopee format (in smallest currency unit) to standard format
                        price = basic_info.get('price', 0) / 100000  # Convert from Shopee's format (1 PHP = 100000 units)
                        
                        # Extract relevant fields
                        description = "NA"  # Not directly available in the API response
                        category = "NA"     # Not directly available in the API response
                        brand = basic_info.get('brand', 'NA')
                        currency = basic_info.get('currency', 'PHP')
                        rating = basic_info.get('item_rating', {}).get('rating_star', 'NA')
                        availability = "in_stock"
                        source_website = "Shopee"
                        
                        
                        # Create source URL from item and shop IDs
                        item_id = basic_info.get('itemid', '')
                        shop_id = basic_info.get('shopid', '')
                        source_url = f"https://shopee.ph/product/{shop_id}/{item_id}" if item_id and shop_id else "NA"
                        
                        # Insert into database
                        cursor.execute("""
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency,
                                rating, availability, source_website, source_url, user_id, group_id, search_name
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            name, description, category, brand, price, currency,
                            rating, availability, source_website, source_url, user_id, group_id, search_name
                        ))
                        shopee_count += 1
                
                print(f"{shopee_count} Shopee products inserted.")
                
            except Exception as e:
                print(f"Error with Shopee API: {e}")
                
            # 7. TIKTOK SHOP
            try:
                print("\nScraping TikTok Shop products...")
                conn_tiktok = http.client.HTTPSConnection("tiktok-data-api2.p.rapidapi.com")
                
                headers_tiktok = {
                    'x-rapidapi-key': "1b9956b92fmsh6a189d0e32e8631p131a58jsnbae6ad5adfa8",
                    'x-rapidapi-host': "tiktok-data-api2.p.rapidapi.com"
                }
                
                conn_tiktok.request("GET", f"/shop/search-shop?keyword={value_query}&country=PH&limit=10&offsite=0", headers=headers_tiktok)
                
                res_tiktok = conn_tiktok.getresponse()
                data_tiktok = res_tiktok.read()
                parsed_tiktok = json.loads(data_tiktok.decode("utf-8"))
                
                tiktok_count = 0
                for entry in parsed_tiktok.get("data", []):
                    for product in entry.get("products", []):
                        product_name = product.get("title", "N/A")
                        
                        if is_duplicate(cursor, product_name):
                            print(f"Duplicate (TikTok Shop): {product_name}")
                            continue
                        
                        currency = product.get("currency", "PHP")
                        price = product.get("price", "N/A")
                        detail_url = product.get("detail_url", "N/A")
                        
                        
                        # Get first image URL if available
                        image_url = "N/A"
                        for img in product.get("img", []):
                            url_list = img.get("url_list", [])
                            if url_list:
                                image_url = url_list[0]
                                break
                        
                        # Insert into database
                        cursor.execute("""
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency,
                                rating, availability, source_website, source_url, image_url, user_id, group_id, search_name
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            product_name, 'NA', 'NA', 'NA', price, currency,
                            'NA', 'in_stock', 'TikTok Shop', detail_url, image_url, user_id, group_id, search_name
                        ))
                        tiktok_count += 1
                
                print(f"{tiktok_count} TikTok Shop products inserted.")
                
            except Exception as e:
                print(f"Error with TikTok Shop API: {e}")

            # 8. LAZADA
            try:
                print("\nScraping Lazada products...")
                
                # Lazada search URL
                search_url = f'https://www.lazada.com.ph/tag/{value_query}'
                
                # Payload for Oxylabs
                payload_lazada = {
                    'source': 'universal',
                    'url': search_url,
                    'render': 'html',
                    'parse': 'false'
                }
                
                # Send request to Oxylabs Real-Time Crawler API
                response_lazada = requests.post(
                    'https://realtime.oxylabs.io/v1/queries',
                    auth=('raigye0118_BlrZS', 'LoveGod0118+'),
                    json=payload_lazada,
                )
                
                # Get the HTML content
                html_content_lazada = response_lazada.json().get('results', [{}])[0].get('content', '')
                
                # Parse the HTML
                soup_lazada = BeautifulSoup(html_content_lazada, 'html.parser')
                
                # Find all product blocks
                products_lazada = soup_lazada.find_all('div', class_='Bm3ON')
                
                print(f"Found {len(products_lazada)} Lazada products...")
                
                lazada_count = 0
                for product in products_lazada:
                    try:
                        a_tag = product.find('a', href=True)
                        img_tag = product.find('img')
                        
                        # Extract URL, title, and image
                        product_url = f"https:{a_tag['href']}" if a_tag else "NA"
                        product_image = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "NA"
                        product_title = img_tag['alt'] if img_tag and 'alt' in img_tag.attrs else "NA"
                        
                        
                        # Skip if product title is missing or duplicate
                        if product_title == "NA" or is_duplicate(cursor, product_title):
                            if product_title != "NA":
                                print(f"Duplicate (Lazada): {product_title}")
                            continue
                        
                        # Extract price
                        price_tag = product.find('span', class_='ooOxS')
                        product_price = price_tag.text.strip().replace('₱', '').replace(',', '') if price_tag else 'NA'
                        
                        # Insert into database
                        cursor.execute("""
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency,
                                rating, availability, source_website, source_url, image_url, user_id, group_id, search_name
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            product_title, 'NA', 'NA', 'NA', product_price, 'PHP',
                            'NA', 'in_stock', 'Lazada', product_url, product_image, user_id, group_id, search_name
                        ))
                        lazada_count += 1
                        
                    except Exception as e:
                        print(f"Error extracting Lazada product: {e}")
                        
                print(f"{lazada_count} Lazada products inserted.")
                
            except Exception as e:
                print(f"Error with Lazada scraping: {e}")
            
            # 9. AMAZON
            try:
                print("\nScraping Amazon products...")
                
                # Set up payload with API key and the URL for the product search
                payload_amazon = {
                    'api_key': 'e3ebed373fb3872d8e955acec5e2fa23',
                    'url': f'https://www.amazon.com/s?k={value_query}'
                }
                
                # Send the GET request to the API
                r_amazon = requests.get('https://api.scraperapi.com/', params=payload_amazon)
                
                # Trim from the first <div role="listitem"
                start_index = r_amazon.text.find('<div role="listitem"')
                trimmed_html = r_amazon.text[start_index:] if start_index != -1 else r_amazon.text
                
                # Parse the HTML content using BeautifulSoup
                soup_amazon = BeautifulSoup(trimmed_html, 'html.parser')
                
                # Find all product list items
                listitems = soup_amazon.find_all('div', attrs={'role': 'listitem'})
                
                print(f"Found {len(listitems)} Amazon products...")
                
                amazon_count = 0
                for item in listitems:
                    try:
                        # Extract product name
                        product_name_tag = item.find('img', {'class': 's-image'})
                        if not product_name_tag or 'alt' not in product_name_tag.attrs:
                            continue
                            
                        product_name = product_name_tag['alt']
                        
                        if is_duplicate(cursor, product_name):
                            print(f"Duplicate (Amazon): {product_name}")
                            continue
                        
                        # Extract product rating
                        product_rating_tag = item.find('span', {'class': 'a-icon-alt'})
                        product_rating = product_rating_tag.get_text(strip=True).replace(' out of 5 stars', '') if product_rating_tag else "NA"
                        
                        # Extract product price
                        product_price_tag = item.find('span', {'class': 'a-price-whole'})
                        product_price = product_price_tag.get_text(strip=True).replace('.', '') if product_price_tag else "NA"
                        
                        # Extract product URL
                        product_url_tag = item.find('a', {'class': 'a-link-normal'})
                        product_url = 'https://www.amazon.com' + product_url_tag.get('href') if product_url_tag and product_url_tag.get('href') else "NA"
                        

                        # Insert into database
                        cursor.execute("""
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency,
                                rating, availability, source_website, source_url, user_id, group_id, search_name
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            product_name, 'NA', 'NA', 'NA', product_price, 'USD',
                            product_rating, 'in_stock', 'Amazon', product_url, user_id, group_id, search_name
                        ))
                        amazon_count += 1
                        
                    except Exception as e:
                        print(f"Error extracting Amazon product: {e}")
                
                print(f"{amazon_count} Amazon products inserted.")
                
            except Exception as e:
                print(f"Error with Amazon scraping: {e}")
            
            # 10. ALIEXPRESS
            try:
                print("\nScraping AliExpress products...")
                
                # Set up payload with API key and the URL for the product search
                payload_aliexpress = {
                    'api_key': 'e3ebed373fb3872d8e955acec5e2fa23',
                    'url': f'https://www.aliexpress.com/w/wholesale-{value_query}.html'
                }
                
                # Send the GET request to the API
                r_aliexpress = requests.get('https://api.scraperapi.com/', params=payload_aliexpress)
                
                # Function to extract the content array from the response
                def extract_content_array(raw_text):
                    # Find "itemList" block
                    itemlist_match = re.search(r'"itemList"\s*:\s*\{', raw_text)
                    if not itemlist_match:
                        print("itemList block not found.")
                        return []
                    
                    # Locate "content":[
                    content_start = raw_text.find('"content":', itemlist_match.end())
                    if content_start == -1:
                        print("content array not found.")
                        return []
                    
                    # Find start of array
                    array_start = raw_text.find('[', content_start)
                    if array_start == -1:
                        print("Start of content array not found.")
                        return []
                    
                    # Extract array using bracket counting
                    bracket_count = 0
                    end_index = array_start
                    while end_index < len(raw_text):
                        char = raw_text[end_index]
                        if char == '[':
                            bracket_count += 1
                        elif char == ']':
                            bracket_count -= 1
                            if bracket_count == 0:
                                break
                        end_index += 1
                    
                    array_str = raw_text[array_start:end_index+1]
                    
                    # Parse the array
                    try:
                        return json.loads(array_str)
                    except json.JSONDecodeError as e:
                        print("JSON decoding error:", e)
                        return []
                
                # Extract and process content array
                content_array = extract_content_array(r_aliexpress.text)
                
                print(f"Extracted {len(content_array)} AliExpress products...")
                
                aliexpress_count = 0
                for item in content_array:
                    try:
                        # Extract product title
                        title_info = item.get('title', {})
                        product_name = title_info.get('displayTitle', 'NA') if isinstance(title_info, dict) else 'NA'
                        
                        if product_name == 'NA' or is_duplicate(cursor, product_name):
                            if product_name != 'NA':
                                print(f"Duplicate (AliExpress): {product_name}")
                            continue
                        
                        # Extract price
                        prices_info = item.get('prices', {})
                        price = 'NA'
                        currency = 'USD'
                        
                        if isinstance(prices_info, dict) and 'salePrice' in prices_info:
                            sale_price = prices_info.get('salePrice', {})
                            if isinstance(sale_price, dict):
                                price = sale_price.get('minPrice', 'NA')
                                currency = sale_price.get('currencyCode', 'USD')
                        
                        # Extract rating
                        evaluation_info = item.get('evaluation', {})
                        rating = evaluation_info.get('starRating', 'NA') if isinstance(evaluation_info, dict) else 'NA'
                        
                        # Extract product URL
                        product_id = item.get('productId', '')
                        product_url = f"https://www.aliexpress.com/item/{product_id}.html" if product_id else "NA"
                        
                        # Extract image URL
                        image_info = item.get('image', {})
                        image_url = ''
                        
                        if isinstance(image_info, dict) and 'imgUrl' in image_info:
                            img_url = image_info.get('imgUrl', '')
                            if img_url and img_url.startswith('//'):
                                image_url = f"https:{img_url}"
                            else:
                                image_url = img_url
                        
                        # Extract store information
                        store_info = item.get('store', {})
                        brand = store_info.get('storeName', 'NA') if isinstance(store_info, dict) else 'NA'
                        
                        # Insert into database
                        cursor.execute("""
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency,
                                rating, availability, source_website, source_url, image_url, user_id, group_id, search_name
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            product_name, 'NA', 'NA', brand, price, currency,
                            rating, 'in_stock', 'AliExpress', product_url, image_url, user_id, group_id, search_name
                        ))
                        aliexpress_count += 1
                        
                    except Exception as e:
                        print(f"Error extracting AliExpress product: {e}")
                
                print(f"{aliexpress_count} AliExpress products inserted.")
                
            except Exception as e:
                print(f"Error with AliExpress scraping: {e}")

           

            # Finalize inserts
            connection.commit()
            
            print("\nAll product data successfully committed to database.")
            return redirect('search')

        except Exception as e:
            print("Error occurred:", e)

        finally:
            try:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
            except NameError:
                pass
   
  
    context = { 
        'username' : username
    }
    return render(request, 'client/index.html', context)

# Create your views here.
def ecom(request):
    user_id = request.session.get('user_id', 'na') 
    username = request.session.get('username', 'na') 
    products = Products.objects.filter(user_id=user_id).order_by('-product_id')

   



    context = { 
        'username' : username,
        'products' : products
    }
    return render(request, 'client/ecom.html', context)

def products(request):
    role = request.session.get('role', 'na') 
    username = request.session.get('username', 'na') 
    products = Products.objects.all()
    
    if role == 'costumer' or username == 'na':
        return redirect('login_a')   
    context = { 
        'username' : username,
        'products' : products
    }
    return render(request, 'admin_p/products.html', context)

def customers(request):
    role = request.session.get('role', 'na') 
    username = request.session.get('username', 'na') 
    users = Users.objects.filter(role='costumer')
    
    if role == 'costumer' or username == 'na':
        return redirect('login_a')   
    context = { 
        'username' : username,
        'users' : users
    }
    return render(request, 'admin_p/user_customers.html', context)

def admins(request):
    role = request.session.get('role', 'na') 
    username = request.session.get('username', 'na') 
    users = Users.objects.filter(role='admin')
    
    if role == 'costumer' or username == 'na':
        return redirect('login_a')   
    context = { 
        'username' : username,
        'users' : users
    }
    return render(request, 'admin_p/user_admin.html', context)

# Create your views here.

def admin(request):
    role = request.session.get('role', 'na') 
    username = request.session.get('username', 'na') 
    products = ProductPriceBySource.objects.values('source_website', 'last_updated', 'min_price').order_by('last_updated')
    # Total number of products
    product_count = Products.objects.count()

    # Average product price
    product_average_price_raw = Products.objects.aggregate(avg_price=Avg('price'))['avg_price']
    product_average_price = round(product_average_price_raw, 2) if product_average_price_raw else 0.00

    # Most common source website (assuming you have a field called 'source_website')
    product_most_search_site = (
        Products.objects.values('source_website')
        .annotate(count=Count('source_website'))
        .order_by('-count')
        .first()
    )

    # If you just want the source_website name:
    most_searched_site = product_most_search_site['source_website'] if product_most_search_site else None

    grouped_prices = defaultdict(list)
    last_updated_labels = []

    if role == 'costumer' or username == 'na':
        return redirect('login_a')   

    for product in products:
        grouped_prices[product['source_website']].append(float(product['min_price']))  # Convert Decimal to float
        if str(product['last_updated']) not in last_updated_labels:
            last_updated_labels.append(str(product['last_updated']))  # Ensure unique timestamps

    products = Products.objects.all().order_by('-product_id')[:10]
    logs = SystemLogs.objects.all()

    
    context = {
        "grouped_prices": json.dumps(dict(grouped_prices)),
        "last_updated_labels": json.dumps(last_updated_labels),
        'username' : username,
        'products' : products,
        'product_count' : product_count,
        'product_average_price' : product_average_price,
        'most_searched_site' : most_searched_site,
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
