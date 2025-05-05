import requests
import re
import json
import pymysql
import uuid
import time

# Generate a random UUID group for this run
group_id = uuid.uuid4().hex

# Define search query and list of e-commerce sites
search = "specific iphone 14 cases"
shops = [
    "Shopee", "Lazada", "Zalora", "Carousell", "TikTok Shop", 
    "Citimart", "SM Department Store", "Amazon", "eBay", "AliExpress", 
    "Rakuten", "Temu", "Galleon.ph", "BeautyMNL"
]

# Database connection
conn = pymysql.connect(
    host='mysql-costmoe.alwaysdata.net',
    user='costmoe_user',
    password='hqaDY7FA',
    database='costmoe_db',
    port=3306
)
cursor = conn.cursor()

# Loop through each shop
inserted_total = 0
for shop in shops:
    print(f"Processing {shop}...")

    # Construct dynamic prompt
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

    response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
    
    try:
        data = response.json()
        content = data['choices'][0]['message']['content']
        cleaned_text = (
            content.strip()
            .replace("python", "")
            .replace("```", "")
            .replace("products = [", "[")
        )
        product_list = json.loads(cleaned_text)
    except Exception as e:
        print(f"Error processing {shop}: {e}")
        continue

    # Insert into MySQL
    inserted_rows = 0
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
                inserted_rows += 1
        except Exception as e:
            print(f"Insert error for {shop}: {e}")

    conn.commit()
    inserted_total += inserted_rows
    print(f"{inserted_rows} rows inserted from {shop}.")

    # Respectful delay to avoid rate limits
    time.sleep(2)

cursor.close()
conn.close()
print(f"Total inserted rows: {inserted_total}")
