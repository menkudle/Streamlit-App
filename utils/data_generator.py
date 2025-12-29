import pandas as pd
import numpy as np
import os

CSV_PATH = "data/market_data.csv"


def generate_market_data(n_rows=10000):
    """Generates synthetic data and returns a DataFrame."""
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=n_rows, freq="h")
    categories = ['Electronics', 'Furniture', 'Clothing', 'Groceries', 'Books', 'Toys']
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    payment_modes = ['Credit Card', 'PayPal', 'Debit Card', 'Crypto', 'Bank Transfer']
    segments = ['Consumer', 'Corporate', 'Home Office']

    data = pd.DataFrame({
        'Transaction_ID': range(1, n_rows + 1),
        'Date': dates,
        'Category': np.random.choice(categories, n_rows),
        'Region': np.random.choice(regions, n_rows),
        'Payment_Mode': np.random.choice(payment_modes, n_rows),
        'Segment': np.random.choice(segments, n_rows),
        'Sales': np.random.uniform(10, 5000, n_rows).round(2),
        'Profit': np.random.uniform(-100, 1500, n_rows).round(2),
        'Discount': np.random.uniform(0, 0.3, n_rows).round(2),
        'Rating': np.random.randint(1, 6, n_rows)
    })

    # Geographic Coords Logic
    region_coords = {
        'North America': {'lat': (25, 50), 'lon': (-130, -70)},
        'Europe': {'lat': (35, 60), 'lon': (-10, 40)},
        'Asia Pacific': {'lat': (-10, 40), 'lon': (70, 150)},
        'Latin America': {'lat': (-30, 10), 'lon': (-80, -40)},
        'Middle East': {'lat': (15, 35), 'lon': (35, 60)}
    }

    def get_lat_lon(region):
        lat_range = region_coords[region]['lat']
        lon_range = region_coords[region]['lon']
        return np.random.uniform(lat_range[0], lat_range[1]), np.random.uniform(lon_range[0], lon_range[1])

    coords = data['Region'].apply(lambda x: pd.Series(get_lat_lon(x), index=['Latitude', 'Longitude']))
    data = pd.concat([data, coords], axis=1)

    return data


def ensure_data_exists():
    """Checks if CSV exists, if not generates and saves it."""
    if not os.path.exists(CSV_PATH):
        print("CSV not found. Generating new dataset...")
        df = generate_market_data()
        df.to_csv(CSV_PATH, index=False)
        print(f"Data saved to {CSV_PATH}")
    return CSV_PATH


if __name__ == "__main__":
    # If run directly, save to CSV
    ensure_data_exists()