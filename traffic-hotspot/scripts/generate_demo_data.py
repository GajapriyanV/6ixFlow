"""
Generate demo data for testing the Traffic Hotspot Predictor.
This creates sample datasets when real Toronto data is not available.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_demo_svc_data():
    """Generate demo SVC (road segment) data."""
    
    print("📊 Generating demo SVC data...")
    
    # Create date range for 2022-2024
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Create sample locations around Toronto
    toronto_center = (43.6532, -79.3832)
    locations = []
    for i in range(-3, 4):  # 7x7 grid
        for j in range(-3, 4):
            lat = toronto_center[0] + i * 0.03  # ~3km spacing
            lon = toronto_center[1] + j * 0.03
            locations.append((lat, lon))
    
    # Generate data for each location and time
    data = []
    for date in dates:
        for lat, lon in locations:
            # Create realistic traffic patterns
            hour = date.hour
            day_of_week = date.weekday()
            
            # Base traffic count with time patterns
            base_count = 20
            
            # Rush hour multipliers
            if 7 <= hour <= 9:  # Morning rush
                multiplier = 2.5
            elif 17 <= hour <= 19:  # Evening rush
                multiplier = 2.2
            elif 22 <= hour or hour <= 5:  # Night
                multiplier = 0.3
            else:  # Regular hours
                multiplier = 1.0
            
            # Weekend reduction
            if day_of_week >= 5:  # Weekend
                multiplier *= 0.7
            
            # Seasonal variation
            month = date.month
            if month in [12, 1, 2]:  # Winter
                multiplier *= 0.9
            elif month in [6, 7, 8]:  # Summer
                multiplier *= 1.1
            
            # Add some randomness
            noise = np.random.normal(1, 0.2)
            vehicle_count = max(0, int(base_count * multiplier * noise))
            
            # Create congestion level
            if vehicle_count <= 30:
                congestion_level = 'Low'
            elif vehicle_count <= 60:
                congestion_level = 'Medium'
            else:
                congestion_level = 'High'
            
            data.append({
                'date': date,
                'latitude': lat,
                'longitude': lon,
                'vehicle_count': vehicle_count,
                'congestion_level': congestion_level
            })
    
    df = pd.DataFrame(data)
    
    # Add time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['hour'] = df['date'].dt.hour
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Save to raw data directory
    output_file = "data/raw/svc_raw_data_class_2020_2024.csv"
    df.to_csv(output_file, index=False)
    
    print(f"✅ Demo SVC data saved to: {output_file}")
    print(f"   Generated {len(df)} records for {len(locations)} locations")
    
    return df

def generate_demo_counts_data():
    """Generate demo intersection count data."""
    
    print("📊 Generating demo intersection count data...")
    
    # Create date range for 2022-2024
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Create sample intersection locations
    toronto_center = (43.6532, -79.3832)
    intersections = []
    for i in range(-2, 3):  # 5x5 grid
        for j in range(-2, 3):
            lat = toronto_center[0] + i * 0.05  # ~5km spacing
            lon = toronto_center[1] + j * 0.05
            intersections.append((lat, lon))
    
    # Generate data for each intersection and time
    data = []
    for date in dates:
        for lat, lon in intersections:
            # Create realistic traffic patterns
            hour = date.hour
            day_of_week = date.weekday()
            
            # Base counts for different vehicle types
            base_vehicles = 25
            base_cyclists = 5
            base_pedestrians = 10
            
            # Time-based multipliers
            if 7 <= hour <= 9:  # Morning rush
                vehicle_mult = 2.5
                cyclist_mult = 1.8
                pedestrian_mult = 2.0
            elif 17 <= hour <= 19:  # Evening rush
                vehicle_mult = 2.2
                cyclist_mult = 2.0
                pedestrian_mult = 2.2
            elif 22 <= hour or hour <= 5:  # Night
                vehicle_mult = 0.3
                cyclist_mult = 0.1
                pedestrian_mult = 0.2
            else:  # Regular hours
                vehicle_mult = 1.0
                cyclist_mult = 1.0
                pedestrian_mult = 1.0
            
            # Weekend patterns
            if day_of_week >= 5:  # Weekend
                vehicle_mult *= 0.7
                cyclist_mult *= 1.2  # More cyclists on weekends
                pedestrian_mult *= 1.3  # More pedestrians on weekends
            
            # Seasonal variation
            month = date.month
            if month in [12, 1, 2]:  # Winter
                vehicle_mult *= 0.9
                cyclist_mult *= 0.3  # Fewer cyclists in winter
                pedestrian_mult *= 0.8
            elif month in [6, 7, 8]:  # Summer
                vehicle_mult *= 1.1
                cyclist_mult *= 1.5  # More cyclists in summer
                pedestrian_mult *= 1.2
            
            # Add randomness
            vehicle_count = max(0, int(base_vehicles * vehicle_mult * np.random.normal(1, 0.2)))
            cyclist_count = max(0, int(base_cyclists * cyclist_mult * np.random.normal(1, 0.3)))
            pedestrian_count = max(0, int(base_pedestrians * pedestrian_mult * np.random.normal(1, 0.25)))
            
            total_count = vehicle_count + cyclist_count + pedestrian_count
            
            # Create congestion level
            if total_count <= 40:
                congestion_level = 'Low'
            elif total_count <= 80:
                congestion_level = 'Medium'
            else:
                congestion_level = 'High'
            
            data.append({
                'date': date,
                'latitude': lat,
                'longitude': lon,
                'vehicle_count': vehicle_count,
                'cyclist_count': cyclist_count,
                'pedestrian_count': pedestrian_count,
                'total_count': total_count,
                'congestion_level': congestion_level
            })
    
    df = pd.DataFrame(data)
    
    # Add time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['hour'] = df['date'].dt.hour
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Save to raw data directory
    output_file = "data/raw/comptages_vehicules_cyclistes_pietons.csv"
    df.to_csv(output_file, index=False)
    
    print(f"✅ Demo intersection data saved to: {output_file}")
    print(f"   Generated {len(df)} records for {len(intersections)} intersections")
    
    return df

def main():
    """Generate demo data for testing."""
    
    print("🚀 Generating demo data for Traffic Hotspot Predictor")
    print("=" * 50)
    
    # Create data directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # Generate demo datasets
    svc_data = generate_demo_svc_data()
    counts_data = generate_demo_counts_data()
    
    print("\n✅ Demo data generation completed!")
    print("\nNext steps:")
    print("1. Run: python ml/clean_svc.py")
    print("2. Run: python ml/clean_counts.py")
    print("3. Run: python ml/train.py")
    print("4. Start the API: cd api && python main.py")
    print("5. Start the frontend: cd web && npm run dev")

if __name__ == "__main__":
    main()

