# jruapp/utils/ml_insights.py

import pandas as pd
from joblib import load
from eli5.sklearn import PermutationImportance
import numpy as np

# Map website to numerical score
site_score_map = {
    'Amazon': 1.00, 'Shopee': 0.95, 'Lazada': 0.93, 'TikTok Shop': 0.88,
    'eBay': 0.85, 'AliExpress': 0.82, 'Rakuten': 0.80, 'Zalora': 0.78,
    'Carousell': 0.70, 'PhilGEPS': 0.65, 'BeautyMNL': 0.63, 'Citimart': 0.55,
    'Temu': 0.50, 'Galleon': 0.45
}

def enrich_with_ml_insights(products):
    model = load('ml_best_product_model.joblib')  # Trained classifier
    df = pd.DataFrame([{
        'id': p.product_id,
        'rating': p.rating or 0,
        'price': p.price or 0,
        'site_score': site_score_map.get(p.source_website, 0.5),
        'availability_flag': 1 if p.availability == 'in_stock' else 0
    } for p in products])

    feature_data = df[['rating', 'price', 'site_score', 'availability_flag']]
    
    # Generate predictions (assumes binary classification)
    y_pred = model.predict(feature_data)

    # Fit Permutation Importance (on the same data for now)
    perm = PermutationImportance(model, random_state=1).fit(feature_data, y_pred)
    importances = perm.feature_importances_

    # Rank features globally
    feature_names = feature_data.columns.tolist()
    global_rank = sorted(zip(feature_names, importances), key=lambda x: -x[1])

    # Attach ranked insights per product
    for i, product in enumerate(products):
        local_importance = []
        for j, feat in enumerate(feature_names):
            value = feature_data.iloc[i][feat]
            direction = "high" if value > np.mean(feature_data[feat]) else "low"
            if importances[j] > 0.01:
                local_importance.append(f"{feat.replace('_', ' ').title()} is {direction}")
        product.ml_insight = "; ".join(local_importance) or "No strong signals found."

    return products
