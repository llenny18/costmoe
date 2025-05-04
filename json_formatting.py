import re
import json

# Simulated JSON response
response = {
    'id': '68add178-7c29-4b9e-8df7-8189bd2b6085',
    'model': 'sonar-pro',
    'created': 1746346025,
    'usage': {'prompt_tokens': 40, 'completion_tokens': 300, 'total_tokens': 340, 'search_context_size': 'low'},
    'citations': [
        'https://shopee.ph/list/iphone/14/case',
        'https://shopee.ph/list/iphone/14%20pro/case',
        'https://shopee.ph/list/iphone/14%20pro%20max/case',
        'https://shopee.ph/list/iphone/14%20plus/case',
        'https://pcit.dk/?p=176860817'
    ],
    'object': 'chat.completion',
    'choices': [{
        'index': 0,
        'finish_reason': 'length',
        'message': {
            'role': 'assistant',
            'content': '''
Here are 10 of the best-rated cheap iPhone 14 cases available on Shopee Philippines, with the relevant specifications, ratings, prices, product names, product and image links provided as text for easy reference. Detailed specifications are listed when available.

## Best Rated Cheap iPhone 14 Cases on Shopee Philippines

| Name | Price | Rating | Key Specs | Product Link | Image Link |
|------|-------|--------|-----------|--------------|------------|
| Acrylic Shockproof Anti-drop Airbag Case | ₱14 | 4.5 (1222 reviews) | Shockproof, Airbag corners, Acrylic material, Anti-drop | shopee.ph/list/iphone/14/case | [Image] |
| Ultra Slim Transparent Silicone Case | ₱25 | 4.6 | Slim fit, Transparent, Flexible silicone, Lightweight | shopee.ph/list/iphone/14/case | [Image] |
| Clear Soft TPU Protective Cover | ₱27 | 4.7 | TPU, Flexible, Scratch-resistant, Clear | shopee.ph/list/iphone/14/case | [Image] |
| Carbon Fiber Shockproof Armor Case | ₱40 | 4.7 | Carbon fiber design, Anti-shock, Raised edges | shopee.ph/list/iphone/14/case | [Image] |
| Matte Frosted Anti-fingerprint Case | ₱30 | 4.6 | Matte, Frosted | shopee.ph/list/iphone/14/case | [Image] |
'''
        },
        'delta': {'role': 'assistant', 'content': ''}
    }]
}

# Extract the table content
content = response['choices'][0]['message']['content']

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
