# Raw Data Directory

Place your raw CSV files from Toronto Open Data Portal here:

## Required Files:

### 1. Road Segments Data
- **File**: `svc_raw_data_class_2020_2024.csv`
- **Source**: Toronto Open Data Portal - Road Segment Volume Counts
- **Description**: Contains traffic volume data for road segments across Toronto
- **URL**: https://open.toronto.ca/dataset/road-segment-volume-counts/

### 2. Intersection Counts Data  
- **File**: `comptages_vehicules_cyclistes_pietons.csv`
- **Source**: Toronto Open Data Portal - Vehicle, Cyclist, and Pedestrian Counts
- **Description**: Contains traffic counts for vehicles, cyclists, and pedestrians at intersections
- **URL**: https://open.toronto.ca/dataset/vehicle-cyclist-and-pedestrian-counts/

## File Structure Expected:

```
data/raw/
├── svc_raw_data_class_2020_2024.csv          # Road segment data
├── comptages_vehicules_cyclistes_pietons.csv # Intersection data
└── README.md                                  # This file
```

## Next Steps:

1. Download the CSV files from the Toronto Open Data Portal
2. Place them in this directory with the exact filenames above
3. Run the data cleaning scripts:
   ```bash
   python ml/clean_svc.py
   python ml/clean_counts.py
   ```
4. The cleaned data will be saved to `data/processed/`

## Alternative - Demo Data:

If you don't have access to the real data yet, you can generate demo data for testing:

```bash
python scripts/generate_demo_data.py
```

This will create sample datasets with realistic traffic patterns for development and testing.

