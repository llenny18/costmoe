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
from .models import Users, Products, SystemLogs, BestProductsPerGroup, ProductGroups, ProductChoose,Quotations, ProductUserView,SystemLogsOverall
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
import requests
import re
import json
import pymysql
import uuid
import time

from difflib import SequenceMatcher
from .models import Products



def products_q(request):
    user_id = request.session.get('user_id', 'na') 
    username = request.session.get('username', 'na') 
    search_name_val = request.session.get('search_name', 'na') 
    similar_matches = request.session.get('similar_matches', 'na') 
    products = similar_matches
    
    return JsonResponse(list(products), safe=False)



def products_api(request):
    user_id = request.session.get('user_id', 'na') 
    username = request.session.get('username', 'na') 
    products = Products.objects.exclude(m_status="delete").order_by('-product_id').values()
    return JsonResponse(list(products), safe=False)

def products_api_c(request):
    user_id = request.session.get('user_id', 'na') 
    username = request.session.get('username', 'na') 
    products = ProductUserView.objects.filter(user_id=user_id, m_status="active").order_by('-product_id').values()
    return JsonResponse(list(products), safe=False)

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


import decimal

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimals(value) for key, value in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    return obj

def market_differentiation_q(request, search_name):
    search_name = search_name.replace("%20", " ")
    user_id = request.session.get('user_id', 'na') 
    username = request.session.get('username', 'na') 
    similar_matches = find_similar_products(search_name)
    products = Products.objects.filter(search_name=search_name).values().distinct()
    request.session['search_name_val'] = search_name
    
    # Convert Decimal values before saving
    request.session['similar_matches'] = convert_decimals(similar_matches)


    context = { 
        'username': username,
        'search_name': search_name,
        'products': similar_matches
    }
    return render(request, 'client/ecom_q.html', context)





def quotations(request):
        # Retrieve user_id from session (or set default if missing)
    user_id = request.session.get('user_id', 'na')
    username = request.session.get('username', 'na')
    if username == 'na':
        return redirect('login_c')
    quotations = Quotations.objects.filter(user_id=user_id)
    if request.method == 'POST':
        if "delete_quo" in request.POST:
            q_id = request.POST.get("q_id")
            quotation = Quotations.objects.get(quotation_id=q_id)

            # Construct full path to the file
            file_path = os.path.join(settings.BASE_DIR, 'costmoeapp/static', 'quotations', quotation.file_name)

            # Delete the file from the filesystem
            if os.path.exists(file_path):
                os.remove(file_path)

            # Delete the record from the database
            quotation.delete()
            return redirect('quotations')
        
        elif "create_quo" in request.POST:
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
                    is_analyzed=0,
                    uploaded_at=pd.Timestamp.now()
                )
                new_quotation.save()  # Save the file metadata to the database

                return redirect('quotations')
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'client/quotations.html', {'quotations' : quotations})

from decimal import Decimal



from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json, uuid, time, requests, pymysql

@csrf_exempt
@require_POST
def fetch_products(request):
    try:
        body = json.loads(request.body)
        search = body.get("search", "").strip()
        if not search:
            return JsonResponse({"error": "Search term is required."}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    shops = [
        "Shopee", "Lazada", "Zalora", "Carousell", "TikTok Shop", 
        "Citimart", "SM Department Store", "Amazon", "eBay", "AliExpress", 
        "Rakuten", "Temu", "Galleon.ph", "BeautyMNL"
    ]
    group_id = uuid.uuid4().hex
    inserted_total = 0

    conn = pymysql.connect(
        host='mysql-costmoe.alwaysdata.net',
        user='costmoe_user',
        password='hqaDY7FA',
        database='costmoe_db',
        port=3306
    )
    cursor = conn.cursor()

    for shop in shops:
        content = (
            f'only generate array, no other and no descriptions. '
            f'Searching for two {search} products on {shop} Philippines, '
            f'make an array using python, columns = name, similarity score(how similar to other websites) as decimal, '
            f'brand, price, in_stock, image link and product link. '
            f'Follow this format please : products =  {{ "name": "", "similarity_score": 0.00, "brand": "", '
            f'"price": 000.00, "in_stock": "yes or no", "image_link": "https://...", '
            f'"product_link": "https://..." }},'
        )

        payload = {
            "model": "sonar-pro",
            "messages": [{"role": "user", "content": content}],
            "max_tokens": 4000
        }
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
            data = response.json()
            raw_content = data['choices'][0]['message']['content']
            cleaned = raw_content.strip().replace("python", "").replace("```", "").replace("products = [", "[")
            product_list = json.loads(cleaned)
        except Exception:
            continue

        for product in product_list:
            try:
                sql = """
                INSERT INTO products (
                    product_name, description, category, brand, price, currency, rating,
                    availability, source_website, source_url, image_url, user_id, group_id,
                    search_name, status, m_status, similarity
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    product["name"],
                    None,
                    "null",
                    product["brand"],
                    product["price"],
                    "PHP",
                    0,
                    "in_stock" if product["in_stock"].lower() == "yes" else "out_of_stock",
                    shop,
                    product["product_link"],
                    product["image_link"],
                    1,
                    group_id,
                    search,
                    "null",
                    "active",
                    round(product["similarity_score"] * 100, 2)
                )
                if len(values) == 17:
                    cursor.execute(sql, values)
                    inserted_total += 1
            except:
                continue

        conn.commit()
        time.sleep(2)


    cursor.close()
    conn.close()
    return JsonResponse({'status': 'done', 'inserted': inserted_total})

def get_similarity(a, b):
    """Return similarity score between two strings as a percentage."""
    return round(SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100, 2)

def find_similar_products(product_name, threshold=50):
    """
    Compare product_name to all products in the DB and return a list
    of similar products with their similarity scores.
    """
    similar_products = []
    all_products = Products.objects.all()

    for product in all_products:
        score = get_similarity(product_name, product.product_name)
        if score >= threshold:
            similar_products.append({
                'product_id': product.product_id,
                'source_website': product.source_website,
                'product_name': product.product_name,
                'brand': product.brand,
                'price': product.price,
                'm_status': product.m_status,
                'in_stock': "in_stock",
                'similarity': product.similarity,
                'score': score
            })

    # Sort descending by score
    similar_products.sort(key=lambda x: x['score'], reverse=True)
    return similar_products


def analyze_csv(request, c_id):
    products_sw = Products.objects.filter(m_status="active").values('source_website').distinct()
    
    # Fetch the quotation object by ID
    try:
        quotations = Quotations.objects.get(quotation_id=c_id)
    except Quotations.DoesNotExist:
        return HttpResponse("Quotation not found.", status=404)
    
    # Construct the full local file path
    file_name = quotations.file_name
    file_path = os.path.join(settings.BASE_DIR, 'costmoeapp', 'static', 'quotations', file_name)
    
    second_column_data = []

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) > 1:  # Ensure there's a second column
                    second_column_data.append(row[1])
    except Exception as e:
        return HttpResponse(f"Error reading CSV: {e}", status=500)

    # Print each item (this would log to server console; for web, return or render it)
    for item in second_column_data:
        if quotations.is_analyzed != 1:
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) > 1:  # Ensure there's a second column
                            second_column_data.append(row[1])
            except Exception as e:
                return HttpResponse(f"Error reading CSV: {e}", status=500)

            # Print each item (this would log to server console; for web, return or render it)
            for item in second_column_data:

                shops = [
                    "Shopee", "Lazada", "Zalora", "Carousell", "TikTok Shop", 
                    "Citimart", "SM Department Store", "Amazon", "eBay", "AliExpress", 
                    "Rakuten", "Temu", "Galleon.ph", "BeautyMNL"
                ]
                group_id = uuid.uuid4().hex
                inserted_total = 0

                conn = pymysql.connect(
                    host='mysql-costmoe.alwaysdata.net',
                    user='costmoe_user',
                    password='hqaDY7FA',
                    database='costmoe_db',
                    port=3306
                )
                cursor = conn.cursor()

                for shop in shops:
                    content = (
                        f'only generate array, no other and no descriptions. '
                        f'Searching for two {item} products on {shop} Philippines, '
                        f'make an array using python, columns = name, similarity score(how similar to other websites) as decimal, '
                        f'brand, price, in_stock, image link and product link. '
                        f'Follow this format please : products =  {{ "name": "", "similarity_score": 0.00, "brand": "", '
                        f'"price": 000.00, "in_stock": "yes or no", "image_link": "https://...", '
                        f'"product_link": "https://..." }},'
                    )

                    payload = {
                        "model": "sonar-pro",
                        "messages": [{"role": "user", "content": content}],
                        "max_tokens": 4000
                    }
                    headers = {
                        "Authorization": "Bearer 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",
                        "Content-Type": "application/json"
                    }

                    try:
                        response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
                        data = response.json()
                        raw_content = data['choices'][0]['message']['content']
                        cleaned = raw_content.strip().replace("python", "").replace("```", "").replace("products = [", "[")
                        product_list = json.loads(cleaned)
                    except Exception:
                        continue

                    for product in product_list:
                        try:
                            sql = """
                            INSERT INTO products (
                                product_name, description, category, brand, price, currency, rating,
                                availability, source_website, source_url, image_url, user_id, group_id,
                                search_name, status, m_status, similarity
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            values = (
                                product["name"],
                                None,
                                "null",
                                product["brand"],
                                product["price"],
                                "PHP",
                                0,
                                "in_stock" if product["in_stock"].lower() == "yes" else "out_of_stock",
                                shop,
                                product["product_link"],
                                product["image_link"],
                                1,
                                group_id,
                                item,
                                "null",
                                "active",
                                round(product["similarity_score"] * 100, 2)
                            )
                            if len(values) == 17:
                                cursor.execute(sql, values)
                                inserted_total += 1
                        except:
                            continue

                    conn.commit()
                    qouation_cert = Quotations.objects.get(quotation_id=c_id)
                    qouation_cert.is_analyzed = 1
                    qouation_cert.save()
                    time.sleep(2)


                cursor.close()
                conn.close()# or use logging# or use logging
                return redirect('analyze_csv', c_id=c_id)

    
    if not os.path.exists(file_path):
        return HttpResponse("CSV file not found.", status=404)

    try:
        # Read the CSV file
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = [row for row in reader]

        # Add m_status column if it doesn't exist
        if 'm_status' not in header:
            header.append('m_status')
            for row in rows:
                row.append('active')

            # Write the updated CSV back
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(rows)
            print("Column 'm_status' added.")
        else:
            print("Column 'm_status' already exists.")
        
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

            # Add count of similar products instead of similarity score
            product_name = standardized_dict.get('product_name', '')
            similar_matches = find_similar_products(product_name)

            # Add similar product count
            standardized_dict['similar_product_count'] = len(similar_matches)

            # Optionally still include similar products list
            standardized_dict['similar_products'] = similar_matches


            
            products_data.append(standardized_dict)
        # Now analyze the products with our function
        analyzed_products = analyze_products(products_data)
        

        
        # Pass the header, original rows, and analyzed products to the template
        return render(request, 'client/analyze_csv.html', {
            'header': header, 
            'rows': rows,
            'products': analyzed_products,  # Send analyzed products to template
            'quotation': quotations,
            'products_sw' : products_sw,
            'c_id' : c_id
        })

    except Exception as e:
        # Handle any unexpected errors
        import traceback
        error_details = traceback.format_exc()
        return HttpResponse(f"Error: {str(e)}<br><pre>{error_details}</pre>", status=500)



from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import csv, os

@csrf_exempt
def bulk_csv_update(request, c_id):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids[]')
        action = request.POST.get('action')

        try:
            quotation = Quotations.objects.get(quotation_id=c_id)
        except Quotations.DoesNotExist:
            return HttpResponse("Quotation not found.", status=404)

        file_path = os.path.join(settings.BASE_DIR, 'costmoeapp', 'static', 'quotations', quotation.file_name)
        if not os.path.exists(file_path):
            return HttpResponse("CSV file not found.", status=404)

        # ✅ First: Read data from CSV in read mode
        updated_rows = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            updated_rows.append(header)
            for row in reader:
                if row and row[0] in product_ids:  # assuming product ID is in column 0
                    if action == 'Enable':
                        row[17] = 'Active'
                    elif action == 'Disable':
                        row[17] = 'Inactive'
                    elif action == 'Delete':
                        continue
                updated_rows.append(row)

        # ✅ Second: Write updated data back to CSV
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




@require_POST
def update_products_status(request):
    user_id = request.session.get('user_id', 'na')

    product_ids = request.POST.getlist('product_ids[]')
    action = request.POST.get('action')

    if not product_ids or not action:
        return redirect('products')  # Change to match your template's name

    if action == 'Monitor':
        for pid in product_ids:
            ProductChoose.objects.create(
                user_id=user_id,
                product_id=pid,
                date_time=timezone.now()
            )
        messages.success(request, "Monitoring started for selected products.")
        return redirect('monitored_products') 
    else:
        status_map = {
            'Enable': 'active',
            'Disable': 'disabled',
            'Delete': 'delete',
        }

        new_status = status_map.get(action)
        if new_status:
            Products.objects.filter(product_id__in=product_ids).update(m_status=new_status)
            messages.success(request, f"{action}d selected products.")
        else:
            messages.error(request, "Invalid status action selected.")

    return redirect('search')  # Change to match your URL pattern

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
    
    # Determine the 3 websites to keep based on highest overall scores
    website_scores = {}
    for product in products:
        website = product.source_website
        if website not in website_scores:
            website_scores[website] = 0
        website_scores[website] += product.final_score
    
    # Select top 3 websites
    top_websites = sorted(website_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    top_websites = {website for website, _ in top_websites}
    
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
    
    # Build the table
    raw_data = defaultdict(list)
    
    # Filter products to only include the top 3 websites
    filtered_products = [p for p in products if p.source_website in top_websites]
    
    for product in filtered_products:
        raw_data[product.search_name].append(product)
    
    # Now build table_data using only products from the top 3 websites
    for search, entries in raw_data.items():
        table_data[search] = {}
        
        for product in entries:
            website = product.source_website
            table_data[search][website] = {
                'score': product.final_score,
                'price': product.price,
                'currency': product.currency,
                'product_name': product.product_name,
                'source_url': product.source_url
            }
            
            # Zero price
            if product.price == 0:
                differentiations['zero_price_urls'].append({
                    'search_name': search,
                    'website': website,
                    'product_name': product.product_name,
                    'source_url': product.source_url
                })
    
    # Find best product per search (highest score)
    best_products = {}
    
    for search, website_scores in table_data.items():
        if website_scores:  # Check if there are any entries for this search
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
        'all_websites': list(top_websites),  # Only include the top 3 websites
        'best_products': best_products,
        'differentiations': differentiations
    }
    return render(request, 'client/market_differentiation.html', context)



# Create your views here.
def home(request):
    group_id = generate_hashed_string()

    user_id = request.session.get('user_id', 'na') 
    username = request.session.get('username', 'na') 

    context = { 
        'username' : username
    }
    return render(request, 'client/index.html', context)

# Create your views here.
def ecom(request):
    user_id = request.session.get('user_id', 'na') 
    username = request.session.get('username', 'na') 
    products = Products.objects.filter(m_status="active").values('source_website').distinct()


    context = { 
        'username' : username,
        'products' : products
    }
    return render(request, 'client/ecom.html', context)



def ecom_choosen(request):
    user_id = request.session.get('user_id', 'na') 
    username = request.session.get('username', 'na') 
    products = Products.objects.filter(m_status="active").values('source_website').distinct()



    context = { 
        'username' : username,
        'products' : products
    }
    return render(request, 'client/ecom_chosen.html', context)




def system_logs_view(request):
    role = request.session.get('role', 'na') 
    username = request.session.get('username', 'na') 
    products = Products.objects.all()
    
    if role == 'costumer' or username == 'na':
        return redirect('login_a')   
    logs = SystemLogsOverall.objects.all()
    return render(request, 'admin_p/logs.html', {'logs': logs})

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
