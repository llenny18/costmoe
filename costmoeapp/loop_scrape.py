import json
from bs4 import BeautifulSoup
import requests
import pymysql
import requests
import re
import json
import http.client
from bs4 import BeautifulSoup
from sklearn.linear_model import LogisticRegression
import csv
from datetime import datetime
import hashlib
import random
import string

products = [
    "Xiaomi Mi Band Fitness Trackers",
    "Anker Power Banks",
    "Baseus Car Phone Holders",
    "Philips Air Fryers",
    "Nike Air Force 1 Sneakers",
    "Adidas Ultraboost Running Shoes",
    "Levi's 501 Original Jeans",
    "H&M Basic T-Shirts",
    "Ray-Ban Wayfarer Sunglasses",
    "Preloved iPhones",
    "Vintage Vinyl Records",
    "Secondhand DSLR Cameras",
    "Used Furniture Sets",
    "Collectible Action Figures",
    "Niacinamide Whitening Soap",
    "LovePet Cat Treats",
    "Silicone Invisible Bra Inserts",
    "Assorted Chocolate and Cookie Combo",
    "Microfiber Bath Towels",
    "A4 Bond Paper (80gsm)",
    "HP LaserJet Toner Cartridges",
    "Dell OptiPlex Desktop Computers",
    "Epson L-Series Printers",
    "Executive Office Chairs",
    "Tarte Shape Tape Concealer",
    "Hozmay Waffle Dish Towels",
    "Dyson Supersonic Hair Dryer",
    "Anrabess Linen Two-Piece Set",
    "Apple AirPods Pro",
    "Vintage Pokémon Cards",
    "Antique Pocket Watches",
    "Rare Comic Books",
    "Limited Edition Sneakers",
    "Signed Sports Memorabilia",
    "Smart LED Light Bulbs",
    "Wireless Bluetooth Earbuds",
    "Magnetic Phone Holders",
    "Mechanical Gaming Keyboards",
    "Reusable Silicone Food Bags",
    "Shiseido Ultimune Power Infusing Concentrate",
    "Uniqlo Ultra Light Down Jackets",
    "Panasonic Nanoe Hair Dryers",
    "Muji Gel Ink Pens",
    "Nintendo Switch Consoles",
    "Hot Wheels Die-Cast Cars",
    "G.I. Joe Action Figures",
    "LED Star Projectors",
    "Cotton T-Shirts",
    "Silicone Kitchen Utensils",
    "KitchenAid Stand Mixer Attachments",
    "Brother Sewing Machine Accessories",
    "Instant Pot Pressure Cookers",
    "Fitbit Fitness Trackers",
    "Amazon Kindle Paperwhite",
    "Parfums de Marly Delina Perfume",
    "Dermalogica Daily Microfoliant",
    "The Ordinary Niacinamide 10% + Zinc 1%",
    "COSRX Acne Pimple Master Patch",
    "Laneige Lip Sleeping Mask"
]
def generate_hashed_string():
    # Generate a random string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    # Hash the string using SHA-256 and return first 10 characters of the hex digest
    hash_object = hashlib.sha256(random_string.encode())
    hashed_string = hash_object.hexdigest()[:10]
    
    return hashed_string
# Simple loop to print each product
for product in products:
    if(product!=""):
        group_id = generate_hashed_string()
        user_id = 1


        product_name1 = product
        product_name = product_name1.replace(" ", "%20")
        
        search_name = product_name1
        log_time = datetime.now() 



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