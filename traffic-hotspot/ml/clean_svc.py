"""
Data cleaning script for Toronto road segment data (SVC).
Processes svc_raw_data_class_2020_2024.csv and outputs cleaned data for 2022-2024.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def clean_svc_data():
    """
    Clean the SVC (road segment) dataset.
    Filters for 2022-2024 data and prepares features for ML.
    """
    
    # Check if raw data exists
    raw_file = "../data/raw/svc_raw_data_class_2020_2024.csv"
    if not os.path.exists(raw_file):
        print(f"ERROR: Raw data file not found: {raw_file}")
        print("Please download svc_raw_data_class_2020_2024.csv from Toronto Open Data")
        print("and place it in the data/raw/ directory.")
        return
    
    print("Loading SVC raw data...")
    df = pd.read_csv(raw_file)
    print(f"   Loaded {len(df)} records")
    
    # Display basic info about the dataset
    print(f"   Columns: {list(df.columns)}")
    
    # Convert time columns to datetime
    df['time_start'] = pd.to_datetime(df['time_start'])
    df['time_end'] = pd.to_datetime(df['time_end'])
    
    # Use time_start as our primary datetime column
    df['datetime'] = df['time_start']
    
    print(f"   Date range: {df['datetime'].min()} to {df['datetime'].max()}")
    
    # Filter for 2022-2024 data only
    df_clean = df[(df['datetime'].dt.year >= 2022) & (df['datetime'].dt.year <= 2024)].copy()
    print(f"   Filtered to 2022-2024: {len(df_clean)} records")
    
    # Create time-based features
    df_clean['year'] = df_clean['datetime'].dt.year
    df_clean['month'] = df_clean['datetime'].dt.month
    df_clean['day_of_week'] = df_clean['datetime'].dt.dayofweek
    df_clean['hour'] = df_clean['datetime'].dt.hour
    df_clean['is_weekend'] = df_clean['day_of_week'].isin([5, 6]).astype(int)
    
    # Calculate total vehicle count from individual vehicle type columns
    vehicle_columns = [
        'vol_fwha1_motorbike', 'vol_fwha2_cars', 'vol_fwha3_pickups', 
        'vol_fwha4_buses', 'vol_fwha5', 'vol_fwha6', 'vol_fwha7', 
        'vol_fwha8', 'vol_fwha9', 'vol_fwha10', 'vol_fwha11', 'vol_fwha12', 'vol_fwha13'
    ]
    
    # Fill NaN values with 0 for vehicle counts
    for col in vehicle_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(0)
    
    # Calculate total vehicles
    df_clean['total_vehicles'] = df_clean[vehicle_columns].sum(axis=1)
    
    # Create individual vehicle type counts for better ML features
    df_clean['cars'] = df_clean['vol_fwha2_cars'].fillna(0)
    df_clean['buses'] = df_clean['vol_fwha4_buses'].fillna(0)
    df_clean['trucks'] = df_clean['vol_fwha3_pickups'].fillna(0)  # Using pickups as trucks
    df_clean['motorcycles'] = df_clean['vol_fwha1_motorbike'].fillna(0)
    
    # Create congestion level categories based on total vehicle counts
    # Use percentiles to create Low/Medium/High categories
    p33 = df_clean['total_vehicles'].quantile(0.33)
    p66 = df_clean['total_vehicles'].quantile(0.66)
    
    def categorize_congestion(count):
        if count <= p33:
            return 'Low'
        elif count <= p66:
            return 'Medium'
        else:
            return 'High'
    
    df_clean['congestion_level'] = df_clean['total_vehicles'].apply(categorize_congestion)
    print(f"   Created congestion levels: {df_clean['congestion_level'].value_counts().to_dict()}")
    
    # Handle missing values
    df_clean = df_clean.dropna(subset=['datetime', 'longitude', 'latitude'])
    
    # Ensure we have proper location data
    df_clean['latitude'] = df_clean['latitude'].astype(float)
    df_clean['longitude'] = df_clean['longitude'].astype(float)
    
    # Filter out any invalid coordinates (outside Toronto area)
    # Toronto bounds: lat 43.5-43.9, lon -79.8 to -79.0
    df_clean = df_clean[
        (df_clean['latitude'] >= 43.5) & (df_clean['latitude'] <= 43.9) &
        (df_clean['longitude'] >= -79.8) & (df_clean['longitude'] <= -79.0)
    ]
    
    print(f"   After coordinate filtering: {len(df_clean)} records")
    
    # Select relevant columns for ML
    ml_columns = [
        'datetime', 'centreline_id', 'location_name', 'longitude', 'latitude',
        'year', 'month', 'day_of_week', 'hour', 'is_weekend',
        'cars', 'buses', 'trucks', 'motorcycles', 'total_vehicles', 'congestion_level'
    ]
    
    df_final = df_clean[ml_columns].copy()
    
    # Sort by datetime for better organization
    df_final = df_final.sort_values('datetime').reset_index(drop=True)
    
    # Save cleaned data
    output_file = "../data/processed/svc_clean_2022_2024.csv"
    df_final.to_csv(output_file, index=False)
    
    print(f"SUCCESS: Cleaned SVC data saved to: {output_file}")
    print(f"   Final dataset: {len(df_final)} records, {len(df_final.columns)} columns")
    print(f"   Columns: {list(df_final.columns)}")
    print(f"   Date range: {df_final['datetime'].min()} to {df_final['datetime'].max()}")
    print(f"   Total vehicles range: {df_final['total_vehicles'].min()} to {df_final['total_vehicles'].max()}")
    
    return df_final

if __name__ == "__main__":
    clean_svc_data()
