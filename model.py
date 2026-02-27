import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# =========================
# LOAD DATA
# =========================

data = pd.read_csv("data/real_mandi_data.csv")

# Keep required columns
data = data[[
    "STATE",
    "District Name",
    "Market Name",
    "Commodity",
    "Modal_Price",
    "Price Date"
]]

# Rename columns
data.columns = [
    "state",
    "district",
    "market",
    "commodity",
    "price",
    "date"
]

# Convert date column
data["date"] = pd.to_datetime(data["date"], errors="coerce")

# Remove missing values
data = data.dropna()

# =========================
# FEATURE ENGINEERING
# =========================

data["year"] = data["date"].dt.year
data["month"] = data["date"].dt.month
data["day"] = data["date"].dt.day

# Encode categorical columns
le_state = LabelEncoder()
le_district = LabelEncoder()
le_market = LabelEncoder()
le_commodity = LabelEncoder()

data["state_enc"] = le_state.fit_transform(data["state"])
data["district_enc"] = le_district.fit_transform(data["district"])
data["market_enc"] = le_market.fit_transform(data["market"])
data["commodity_enc"] = le_commodity.fit_transform(data["commodity"])

# Define features and target
X = data[[
    "state_enc",
    "district_enc",
    "market_enc",
    "commodity_enc",
    "year",
    "month",
    "day"
]]

y = data["price"]

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# MODEL TRAINING
# =========================

model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# EVALUATION
# =========================

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n===== MODEL PERFORMANCE =====")
print("Model MAE:", round(mae, 2))
print("Model R2 Score:", round(r2, 2))

# =========================
# FEATURE IMPORTANCE
# =========================

print("\n===== FEATURE IMPORTANCE =====")
importance = model.feature_importances_
features = X.columns

for i in range(len(features)):
    print(f"{features[i]}: {round(importance[i], 4)}")

# =========================
# PREDICTION FUNCTION
# =========================

def predict_price(state, district, market, commodity, year, month, day):
    try:
        input_data = pd.DataFrame({
            "state_enc": [le_state.transform([state])[0]],
            "district_enc": [le_district.transform([district])[0]],
            "market_enc": [le_market.transform([market])[0]],
            "commodity_enc": [le_commodity.transform([commodity])[0]],
            "year": [year],
            "month": [month],
            "day": [day]
        })

        prediction = model.predict(input_data)
        return round(prediction[0], 2)

    except Exception as e:
        return f"Error in prediction: {str(e)}"