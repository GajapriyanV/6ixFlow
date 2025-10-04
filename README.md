# 🚦 6ixFlow - Toronto Traffic Hotspot Predictor

An AI-powered traffic congestion prediction platform for Toronto, built with machine learning and modern web technologies.

![Toronto Traffic](https://img.shields.io/badge/Location-Toronto-blue) ![ML](https://img.shields.io/badge/ML-Random%20Forest-green) ![Tech](https://img.shields.io/badge/Tech-FastAPI%20%2B%20Next.js-orange)

## 🎯 Overview

6ixFlow predicts traffic congestion levels and vehicle counts for 49 road segments across Toronto using machine learning models trained on historical traffic data from 2022-2024.

### ✨ Features

- **🤖 AI-Powered Predictions**: Random Forest models for congestion classification and vehicle count regression
- **🗺️ Interactive Map**: Real-time traffic visualization with Mapbox integration
- **📊 Smart Analytics**: Traffic statistics, congestion distribution, and hotspot identification
- **⚡ Real-time API**: FastAPI backend serving predictions with 89.5% accuracy
- **🎨 Modern UI**: Beautiful, responsive interface built with Next.js and shadcn/ui

## 🏗️ Architecture

```
6ixFlow/
├── 📊 Data Pipeline
│   ├── data/raw/          # Toronto Open Data (SVC 2020-2024)
│   ├── data/processed/    # Cleaned ML-ready datasets
│   └── ml/clean_svc.py    # Data preprocessing pipeline
│
├── 🤖 Machine Learning
│   ├── ml/train.py        # Model training (RF Classifier + Regressor)
│   └── ml/models/         # Trained models (.joblib files)
│
├── 🚀 Backend API
│   └── api/main.py        # FastAPI server with prediction endpoints
│
└── 🎨 Frontend
    └── web/               # Next.js app with Mapbox visualization
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Mapbox account (free tier available)

### 1. Clone the Repository

```bash
git clone https://github.com/GajapriyanV/6ixFlow.git
cd 6ixFlow/traffic-hotspot
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Train the ML models (if not already done)
cd ml
python clean_svc.py  # Clean the raw data
python train.py      # Train the models

# Start the FastAPI server
cd ../api
python main.py
```

The API will be available at `http://127.0.0.1:8000`

### 3. Frontend Setup

```bash
# Install Node.js dependencies
cd web
npm install

# Set up environment variables
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > .env.local
echo "NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here" >> .env.local

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📊 Model Performance

### Classification Model (Congestion Levels)
- **Accuracy**: 89.5%
- **Precision/Recall**:
  - High: 94% precision, 91% recall
  - Medium: 83% precision, 85% recall
  - Low: 92% precision, 92% recall

### Regression Model (Vehicle Counts)
- **MAE**: 6.6 vehicles
- **R² Score**: 95.3%

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | API health check and model status |
| `/predict_at` | POST | Get traffic predictions for specific datetime |
| `/road_segments` | GET | List all available road segments |
| `/model_info` | GET | Model metadata and performance metrics |

### Example API Usage

```bash
# Health check
curl http://127.0.0.1:8000/health

# Get predictions for 5 PM on October 3rd, 2024
curl -X POST http://127.0.0.1:8000/predict_at \
  -H "Content-Type: application/json" \
  -d '{"datetime": "2024-10-03T17:00:00"}'
```

## 🗺️ Map Visualization

The interactive map displays:
- **🟢 Green markers**: Low congestion (0-33rd percentile)
- **🟡 Yellow markers**: Medium congestion (33rd-66th percentile)
- **🔴 Red markers**: High congestion (66th-100th percentile)

Click any marker to see:
- Location name
- Predicted vehicle count
- Congestion level

## 📈 Data Sources

- **Toronto Open Data Portal**: Road Segment Volume Counts (2020-2024)
- **49 Road Segments**: Major intersections and thoroughfares across Toronto
- **15-minute intervals**: High-resolution traffic data
- **Multiple vehicle types**: Cars, buses, trucks, motorcycles

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **scikit-learn**: Machine learning models
- **pandas**: Data processing
- **joblib**: Model serialization

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: Modern component library
- **Mapbox GL JS**: Interactive maps
- **SWR**: Data fetching and caching

### ML Pipeline
- **Random Forest**: Classification and regression
- **OneHotEncoder**: Feature preprocessing
- **Cross-validation**: Model evaluation

## 📁 Project Structure

```
traffic-hotspot/
├── data/
│   ├── raw/                    # Original Toronto Open Data
│   └── processed/              # Cleaned datasets
├── ml/
│   ├── clean_svc.py           # Data cleaning pipeline
│   ├── train.py               # Model training
│   └── models/                # Trained models
├── api/
│   └── main.py                # FastAPI application
├── web/
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   ├── lib/                   # Utilities and types
│   └── package.json           # Dependencies
└── requirements.txt           # Python dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- **Toronto Open Data Portal** for providing the traffic data
- **Mapbox** for the mapping platform
- **FastAPI** and **Next.js** communities for excellent documentation

## 📞 Contact

**Gajapriyan V** - [@GajapriyanV](https://github.com/GajapriyanV)

Project Link: [https://github.com/GajapriyanV/6ixFlow](https://github.com/GajapriyanV/6ixFlow)

---

⭐ **Star this repository if you found it helpful!**
