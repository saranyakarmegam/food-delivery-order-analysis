"""
Food Delivery Order Analysis

Analyzes food delivery orders across restaurants, cities, food categories,
ratings, order amounts, and delivery times.

Includes data cleaning, exploratory analysis, aggregation,
statistical analysis, and visualization.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Data

df = pd.read_csv("food_orders.csv")

# 2. Explore Data

print("Dataset Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Information:")
df.info()

print("\nDescriptive Statistics:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())

# 3. Data Cleaning

# Remove duplicate rows
df = df.drop_duplicates()

# Fill missing OrderAmount values using the mean
# OrderAmount for each FoodCategory
df["OrderAmount"] = df["OrderAmount"].fillna(
    df.groupby("FoodCategory")["OrderAmount"].transform("mean")
)

# Fill missing Rating values using the overall average rating
df["Rating"] = df["Rating"].fillna(df["Rating"].mean())

# 4. Delivery Speed Classification


def delivery_speed(minutes):
    if minutes <= 25:
        return "Fast"
    elif minutes <= 40:
        return "Normal"
    else:
        return "Slow"


df["DeliverySpeed"] = df["DeliveryTime_min"].apply(delivery_speed)

# 5. Filtering, Sorting and Renaming

# Orders with slow delivery
slow_orders = df[df["DeliverySpeed"] == "Slow"]

# Rename delivery time column
df = df.rename(columns={"DeliveryTime_min": "DeliveryMinutes"})

# Top 5 orders by order amount
top_5_orders = df.sort_values("OrderAmount",ascending=False).head(5)

print("\nNumber of Slow Orders:", len(slow_orders))

print("\nTop 5 Orders by Order Amount:")
print(top_5_orders[["Restaurant","FoodCategory","OrderAmount","DeliveryMinutes"]])


# 6. GroupBy Analysis

# Total revenue by restaurant
restaurant_revenue = (df.groupby("Restaurant")["OrderAmount"].sum().sort_values(ascending=False))

# Average rating by food category
category_rating = (df.groupby("FoodCategory")["Rating"].mean().sort_values(ascending=False))

# Total revenue by city and food category
city_category_revenue = (df.groupby(["City", "FoodCategory"])["OrderAmount"].sum().sort_values(ascending=False))

print("\nRevenue by Restaurant:")
print(restaurant_revenue)

print("\nAverage Rating by Food Category:")
print(category_rating)

print("\nRevenue by City and Food Category:")
print(city_category_revenue)

# 7. NumPy Analysis

delivery_array = df["DeliveryMinutes"].to_numpy()

print("\nDelivery Time Statistics:")
print("Mean:", round(np.mean(delivery_array), 2))
print("Median:", np.median(delivery_array))
print("Maximum:", np.max(delivery_array))

# 8. Restaurant Performance

restaurant_revenue_dict = restaurant_revenue.to_dict()

print("\nRestaurant Performance:")

for restaurant, revenue in restaurant_revenue_dict.items():
    if revenue > 1500:
        print(f"{restaurant}: High revenue performance")
    else:
        print(f"{restaurant}: Revenue below 1500")


# 9. Export Cleaned Data

df.to_csv("orders_cleaned.csv", index=False)

print("\nCleaned data exported successfully.")

# 10. Matplotlib Visualizations

# Distribution of delivery time
plt.figure(figsize=(8, 5))
plt.hist(df["DeliveryMinutes"], bins=10)
plt.xlabel("Delivery Time (minutes)")
plt.ylabel("Number of Orders")
plt.title("Distribution of Delivery Time")
plt.tight_layout()
plt.show()


# Revenue by restaurant
plt.figure(figsize=(9, 5))
restaurant_revenue.plot(kind="bar")
plt.xlabel("Restaurant")
plt.ylabel("Total Revenue")
plt.title("Revenue by Restaurant")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 11. Seaborn Visualizations

# Ratings by food category
plt.figure(figsize=(9, 5))
sns.boxplot(data=df, x="FoodCategory", y="Rating")
plt.xlabel("Food Category")
plt.ylabel("Rating")
plt.title("Ratings by Food Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Correlation between numerical variables
correlation = df[["OrderAmount", "DeliveryMinutes", "Rating"]].corr()

plt.figure(figsize=(7, 5))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Between Order Amount, Delivery Time and Rating")
plt.tight_layout()
plt.show()

# 12. Key Findings

top_restaurant = restaurant_revenue.idxmax()
top_revenue = restaurant_revenue.max()

category_delivery_time = df.groupby("FoodCategory")["DeliveryMinutes"].mean()

slowest_category = category_delivery_time.idxmax()
slowest_time = category_delivery_time.max()

print("\n" + "=" * 45)
print("KEY FINDINGS")
print("=" * 45)

print(f"Top restaurant by revenue: " f"{top_restaurant} ({top_revenue:.2f})")

print(
    f"Food category with the highest average delivery time: "
    f"{slowest_category} ({slowest_time:.2f} minutes)"
)

print(
    "Recommendation: Focus on improving delivery efficiency "
    f"for the {slowest_category} category."
)
