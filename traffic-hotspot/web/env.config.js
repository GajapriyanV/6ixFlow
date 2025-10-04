// Environment configuration for the Traffic Hotspot Predictor frontend
module.exports = {
  // API Configuration
  API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  
  // Mapbox Configuration (Optional - you can use Leaflet instead)
  // Get your free token at: https://account.mapbox.com/access-tokens/
  MAPBOX_TOKEN: process.env.NEXT_PUBLIC_MAPBOX_TOKEN || 'your_mapbox_token_here',
  
  // Alternative: Use Leaflet (100% free, no token required)
  USE_LEAFLET: process.env.NEXT_PUBLIC_USE_LEAFLET === 'true' || true,
  
  // Default map center (Toronto)
  DEFAULT_CENTER: {
    lat: 43.6532,
    lng: -79.3832
  },
  
  // Map zoom level
  DEFAULT_ZOOM: 11
};
