import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from joblib import dump

# Step 1: Read the CSV file
csv_file_path = 'BestProductsPerGroup.csv'  # Replace with your actual CSV file path
data = pd.read_csv(csv_file_path)

# Step 2: Select only the necessary columns
data = data[['product_id', 'product_name', 'price', 'rating', 'availability', 'source_website']]

# Step 3: Map website to numerical score for site_score
site_score_map = {
    'Amazon': 1.00, 'Shopee': 0.95, 'Lazada': 0.93, 'TikTok Shop': 0.88,
    'eBay': 0.85, 'AliExpress': 0.82, 'Rakuten': 0.80, 'Zalora': 0.78,
    'Carousell': 0.70, 'PhilGEPS': 0.65, 'BeautyMNL': 0.63, 'Citimart': 0.55,
    'Temu': 0.50, 'Galleon': 0.45
}
data['site_score'] = data['source_website'].map(site_score_map).fillna(0.5)
data['availability_flag'] = data['availability'].apply(lambda x: 1 if x == 'in_stock' else 0)

# Step 4: Create a target variable
data['is_best_product'] = data['rating'].apply(lambda x: 1 if x > 4.0 else 0)  # Example: rating > 4.0 means best product

# Step 5: Define features (X) and target (y)
X = data[['price', 'rating', 'site_score', 'availability_flag']]  # Features
y = data['is_best_product']  # Target: binary classification (best product or not)

# Step 6: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 7: Train the model with balanced class weights
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Step 8: Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Step 9: Save the trained model to a file
dump(model, 'ml_best_product_model.joblib')
print("Model saved as ml_best_product_model.joblib")
