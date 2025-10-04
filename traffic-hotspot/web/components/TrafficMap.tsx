'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import Map, { Marker, Popup } from 'react-map-gl';
import { TrafficPrediction, MapMarker } from '@/lib/types';
import { getTrafficColor, getTrafficIcon } from '@/lib/utils';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Car, MapPin } from 'lucide-react';

interface TrafficMapProps {
  predictions: TrafficPrediction[];
  isLoading?: boolean;
  className?: string;
}

export default function TrafficMap({ predictions, isLoading = false, className }: TrafficMapProps) {
  const [selectedMarker, setSelectedMarker] = useState<MapMarker | null>(null);
  const [viewState, setViewState] = useState({
    longitude: -79.3832, // Toronto center
    latitude: 43.6532,
    zoom: 11
  });

  // Convert predictions to map markers
  const markers: MapMarker[] = predictions.map(prediction => ({
    id: prediction.centreline_id.toString(),
    lat: prediction.latitude,
    lng: prediction.longitude,
    congestion_level: prediction.congestion_level,
    vehicle_count: prediction.predicted_vehicles,
    location_name: prediction.location_name,
  }));

  const handleMarkerClick = useCallback((marker: MapMarker) => {
    setSelectedMarker(marker);
  }, []);

  const handleClosePopup = useCallback(() => {
    setSelectedMarker(null);
  }, []);

  // Calculate map bounds to fit all markers
  useEffect(() => {
    if (markers.length > 0) {
      const lats = markers.map(m => m.lat);
      const lngs = markers.map(m => m.lng);
      
      const bounds = {
        north: Math.max(...lats),
        south: Math.min(...lats),
        east: Math.max(...lngs),
        west: Math.min(...lngs),
      };

      // Adjust view to fit all markers with some padding
      setViewState(prev => ({
        ...prev,
        longitude: (bounds.east + bounds.west) / 2,
        latitude: (bounds.north + bounds.south) / 2,
        zoom: 10
      }));
    }
  }, [markers]);

  const mapboxToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;

  if (!mapboxToken) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-5 w-5" />
            Traffic Map
          </CardTitle>
          <CardDescription>
            Mapbox token not configured
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-96 bg-gray-100 rounded-lg flex items-center justify-center">
            <div className="text-center">
              <p className="text-gray-600 mb-2">Mapbox token required</p>
              <p className="text-sm text-gray-500">Please add NEXT_PUBLIC_MAPBOX_TOKEN to .env.local</p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-5 w-5" />
            Traffic Map
          </CardTitle>
          <CardDescription>
            Loading traffic predictions...
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-96 bg-gray-100 rounded-lg flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MapPin className="h-5 w-5" />
          Traffic Map
        </CardTitle>
        <CardDescription>
          {markers.length} road segments • Click markers for details
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-96 rounded-lg overflow-hidden border">
          <Map
            {...viewState}
            onMove={evt => setViewState(evt.viewState)}
            mapStyle="mapbox://styles/mapbox/streets-v12"
            mapboxAccessToken={mapboxToken}
            style={{ width: '100%', height: '100%' }}
          >
            {markers.map((marker) => (
              <Marker
                key={marker.id}
                longitude={marker.lng}
                latitude={marker.lat}
                onClick={() => handleMarkerClick(marker)}
              >
                <div
                  className="w-6 h-6 rounded-full border-2 border-white shadow-lg cursor-pointer flex items-center justify-center text-white text-xs font-bold"
                  style={{ backgroundColor: getTrafficColor(marker.congestion_level) }}
                >
                  {getTrafficIcon(marker.congestion_level)}
                </div>
              </Marker>
            ))}

            {selectedMarker && (
              <Popup
                longitude={selectedMarker.lng}
                latitude={selectedMarker.lat}
                onClose={handleClosePopup}
                closeButton={true}
                closeOnClick={false}
                anchor="bottom"
              >
                <div className="p-2 min-w-[200px]">
                  <h3 className="font-semibold text-sm mb-2">{selectedMarker.location_name}</h3>
                  <div className="space-y-1 text-xs">
                    <div className="flex items-center gap-2">
                      <span className="font-medium">Congestion:</span>
                      <span
                        className="px-2 py-1 rounded text-white text-xs font-medium"
                        style={{ backgroundColor: getTrafficColor(selectedMarker.congestion_level) }}
                      >
                        {selectedMarker.congestion_level}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Car className="h-3 w-3" />
                      <span className="font-medium">Vehicles:</span>
                      <span>{selectedMarker.vehicle_count}</span>
                    </div>
                  </div>
                </div>
              </Popup>
            )}
          </Map>
        </div>
      </CardContent>
    </Card>
  );
}