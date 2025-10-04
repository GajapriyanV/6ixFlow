"""
Data cleaning script for Toronto intersection count data.
Processes comptages_vehicules_cyclistes_pietons.csv and outputs cleaned data for 2022-2024.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def clean_counts_data():
    """
    Clean the intersection count dataset.
    Filters for 2022-2024 data and prepares features for ML.
    """
    
    # Check if raw data exists
    raw_file = "../data/raw/comptages_vehicules_cyclistes_pietons.csv"
    if not os.path.exists(raw_file):
        print(f"❌ Raw data file not found: {raw_file}")
        print("Please download comptages_vehicules_cyclistes_pietons.csv from Toronto Open Data")
        print("and place it in the data/raw/ directory.")
        return
    
    print("📊 Loading intersection count data...")
    df = pd.read_csv(raw_file)
    print(f"   Loaded {len(df)} records")
    
    # Display basic info about the dataset
    print(f"   Columns: {list(df.columns)}")
    
    # Find date column (could be named differently)
    date_col = None
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['date', 'time', 'datetime']):
            date_col = col
            break
    
    if not date_col:
        print("   ⚠️  No date column found, creating dummy dates")
        df['date'] = pd.date_range('2022-01-01', periods=len(df), freq='H')
    else:
        df['date'] = pd.to_datetime(df[date_col])
    
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    
    # Filter for 2022-2024 data only
    df_clean = df[(df['date'].dt.year >= 2022) & (df['date'].dt.year <= 2024)].copy()
    print(f"   Filtered to 2022-2024: {len(df_clean)} records")
    
    # Create time-based features
    df_clean['year'] = df_clean['date'].dt.year
    df_clean['month'] = df_clean['date'].dt.month
    df_clean['day_of_week'] = df_clean['date'].dt.dayofweek
    df_clean['hour'] = df_clean['date'].dt.hour
    df_clean['is_weekend'] = df_clean['day_of_week'].isin([5, 6]).astype(int)
    
    # Find vehicle, cyclist, and pedestrian count columns
    vehicle_col = None
    cyclist_col = None
    pedestrian_col = None
    
    for col in df_clean.columns:
        col_lower = col.lower()
        if 'vehicle' in col_lower or 'auto' in col_lower:
            vehicle_col = col
        elif 'cyclist' in col_lower or 'bike' in col_lower:
            cyclist_col = col
        elif 'pedestrian' in col_lower or 'ped' in col_lower or 'walk' in col_lower:
            pedestrian_col = col
    
    # Create total traffic count
    total_count = 0
    if vehicle_col:
        total_count += df_clean[vehicle_col].fillna(0)
        df_clean['vehicle_count'] = df_clean[vehicle_col].fillna(0)
    else:
        df_clean['vehicle_count'] = 0
    
    if cyclist_col:
        total_count += df_clean[cyclist_col].fillna(0)
        df_clean['cyclist_count'] = df_clean[cyclist_col].fillna(0)
    else:
        df_clean['cyclist_count'] = 0
    
    if pedestrian_col:
        total_count += df_clean[pedestrian_col].fillna(0)
        df_clean['pedestrian_count'] = df_clean[pedestrian_col].fillna(0)
    else:
        df_clean['pedestrian_count'] = 0
    
    df_clean['total_count'] = total_count
    
    # Create congestion level categories based on total traffic
    if df_clean['total_count'].sum() > 0:
        p33 = df_clean['total_count'].quantile(0.33)
        p66 = df_clean['total_count'].quantile(0.66)
        
        def categorize_congestion(count):
            if count <= p33:
                return 'Low'
            elif count <= p66:
                return 'Medium'
            else:
                return 'High'
        
        df_clean['congestion_level'] = df_clean['total_count'].apply(categorize_congestion)
        print(f"   Created congestion levels: {df_clean['congestion_level'].value_counts().to_dict()}")
    else:
        print("   ⚠️  No traffic count data found, creating dummy congestion levels")
        df_clean['congestion_level'] = 'Medium'  # Default value
    
    # Handle location data
    lat_cols = [col for col in df_clean.columns if 'lat' in col.lower()]
    lon_cols = [col for col in df_clean.columns if 'lon' in col.lower() or 'lng' in col.lower()]
    
    if not lat_cols or not lon_cols:
        print("   ⚠️  No lat/lon columns found, creating dummy coordinates for Toronto intersections")
        # Create realistic Toronto intersection coordinates
        df_clean['latitude'] = 43.6532 + np.random.normal(0, 0.2, len(df_clean))
        df_clean['longitude'] = -79.3832 + np.random.normal(0, 0.2, len(df_clean))
    else:
        df_clean['latitude'] = df_clean[lat_cols[0]]
        df_clean['longitude'] = df_clean[lon_cols[0]]
    
    # Handle missing values
    df_clean = df_clean.dropna(subset=['date'])
    
    # Select relevant columns for ML
    ml_columns = [
        'date', 'year', 'month', 'day_of_week', 'hour', 'is_weekend',
        'latitude', 'longitude', 'congestion_level',
        'vehicle_count', 'cyclist_count', 'pedestrian_count', 'total_count'
    ]
    
    # Keep any additional relevant columns
    for col in df_clean.columns:
        if col not in ml_columns and any(keyword in col.lower() for keyword in ['speed', 'volume', 'density', 'intersection']):
            ml_columns.append(col)
    
    df_final = df_clean[ml_columns].copy()
    
    # Save cleaned data
    output_file = "../data/processed/counts_clean_2022_2024.csv"
    df_final.to_csv(output_file, index=False)
    
    print(f"✅ Cleaned intersection data saved to: {output_file}")
    print(f"   Final dataset: {len(df_final)} records, {len(df_final.columns)} columns")
    print(f"   Columns: {list(df_final.columns)}")
    
    return df_final

if __name__ == "__main__":
    clean_counts_data()
