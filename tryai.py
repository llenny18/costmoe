import requests
import re

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "sonar-pro",
    "messages": [
        {"role": "user", "content": "get 10 best rated cheap iPhone 14 cases Shopee Philippines, get specifications, display rate, price, name, other specs then display product link as text and product image link as text too "}
    ],
    "max_tokens": 300
}
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()

print(data)
# Extract the table content
content = data['choices'][0]['message']['content']

# Use regex to extract table rows
rows = re.findall(r'\| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|', content)

# Convert rows to list of product dictionaries
products = []
for row in rows:
    product = {
        "Name": row[0],
        "Price": row[1],
        "Rating": row[2],
        "Key Specs": row[3],
        "Product Link": row[4],
        "Image Link": row[5]
    }
    products.append(product)

# Print each product's details
for idx, product in enumerate(products, start=1):
    print(f"\nProduct {idx}:")
    for key, value in product.items():
        print(f"{key}: {value}")
