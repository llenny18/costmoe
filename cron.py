import requests
import re
import json
import pymysql
import uuid

# Generate a random UUID
random_uuid = uuid.uuid4().hex

search = "specific iphone 14"
shop = "Lazada"
content = 'only generate array, no other and no descriptions. Searching for two '+search+ 'cases products on '+shop +'Philippines, make an array using python, columns = name, similarity score(how similar to other websites) as decimal, brand, price, in_stock, image link and product link. Follow this format please : products =  { "name": "", "similarity_score": 0.00, "brand": "", "price": 000.00, "in_stock": "yes or no", "image_link": "https://img.lazcdn.com/g/p/a854c4ff07f9f4ffb033c40b66a28af1.png_2200x2200q80.png_.webp", "product_link": "https://www.lazada.com.ph/products/pdp-i4092198413-s22484847434.html" },'

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "sonar-pro",
    "messages": [
        {"role": "user", "content": content}
    ],
    "max_tokens": 4000
}
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()

# Extracting the relevant data from the response
content = data['choices'][0]['message']['content']

# Clean up the content to make it valid JSON
cleaned_text = content.strip().replace("python", "")  # Remove unwanted "python" text and strip extra spaces
cleaned_text = cleaned_text.strip().replace("```", "")  # Remove unwanted "python" text and strip extra spaces
cleaned_text = cleaned_text.strip().replace("products = [", "[")  # Remove unwanted "python" text and strip extra spaces

print(cleaned_text)
print("----------------------------------")

# Try to parse the cleaned text
try:
    product_list = json.loads(cleaned_text)
    print(product_list)
except json.decoder.JSONDecodeError as e:
    print(f"JSON Decode Error: {e}")
    print("Cleaned text might not be in a valid JSON format.")
    print(cleaned_text)


product_list = json.loads(cleaned_text)
print(product_list)
print("----------------------------------")


# Connect to MySQL
conn = pymysql.connect(
    host='mysql-costmoe.alwaysdata.net',
    user='costmoe_user',
    password='hqaDY7FA',
    database='costmoe_db',
    port=3306
)
cursor = conn.cursor()

# Initialize a counter for inserted rows
inserted_rows = 0
# Insert data
for product in product_list:
    sql = """
    INSERT INTO products (
        product_name, description, category, brand, price, currency, rating,
        availability, source_website, source_url, image_url, user_id, group_id,
        search_name, status, m_status, similarity
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Ensure all values match the placeholders
    values = (
        product["name"],                        # product_name
        None,                                   # description
        "null",                                 # category (ensure this is the correct placeholder for your schema)
        product["brand"],                       # brand
        product["price"],                       # price
        "PHP",                                  # currency
        0,                                   # rating
        "in_stock" if product["in_stock"] else "out_of_stock",  # availability
        shop,                                   # source_website
        product["product_link"],                # source_url
        product["image_link"],                  # image_url
        1,                                      # user_id (dummy value)
        uuid.uuid4().hex,                       # group_id (dummy value)
        search,                                 # search_name (sample search keyword)
        "null",                                 # status
        "active",                               # m_status
        round(product["similarity_score"] * 100, 2)  # similarity (scale to match schema)
    )
    
    # Ensure the number of placeholders and values match
    if len(values) != 17:
        print(f"Warning: Placeholder count mismatch. Expected 17 values, got {len(values)}.")
    else:
        cursor.execute(sql, values)
        inserted_rows += 1  # Increment the counter for each successful insertion

# Commit and close
conn.commit()

# Print the number of rows inserted
print(f"{inserted_rows} rows inserted successfully!")

cursor.close()
conn.close()
