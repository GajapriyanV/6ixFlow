'use client';

import React, { useState, useEffect } from 'react';
import { TrafficPrediction, HealthStatus } from '@/lib/types';
import { apiClient } from '@/lib/api';
import DateTimePicker from '@/components/DateTimePicker';
import TrafficMap from '@/components/TrafficMap';
import PredictionStats from '@/components/PredictionStats';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MapPin, BarChart3, Clock, Wifi, WifiOff } from 'lucide-react';

export default function HomePage() {
  const [predictions, setPredictions] = useState<TrafficPrediction[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Check API health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const health = await apiClient.getHealth();
        setHealthStatus(health);
        setError(null);
      } catch (err) {
        setError('Unable to connect to the prediction API. Please ensure the backend is running.');
        console.error('Health check failed:', err);
      }
    };

    checkHealth();
  }, []);

  const handleDateTimeChange = async (dateTime: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const newPredictions = await apiClient.predictTraffic({ datetime: dateTime });
      setPredictions(newPredictions);
    } catch (err) {
      setError('Failed to fetch traffic predictions. Please try again.');
      console.error('Prediction failed:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const isApiHealthy = healthStatus?.status === 'healthy' && healthStatus?.models_loaded;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Toronto Traffic Hotspot Predictor</h1>
              <p className="text-sm text-gray-600">AI-powered traffic congestion forecasting</p>
            </div>
            <div className="flex items-center gap-2">
              {isApiHealthy ? (
                <div className="flex items-center gap-2 text-green-600">
                  <Wifi className="h-4 w-4" />
                  <span className="text-sm font-medium">API Connected</span>
                </div>
              ) : (
                <div className="flex items-center gap-2 text-red-600">
                  <WifiOff className="h-4 w-4" />
                  <span className="text-sm font-medium">API Disconnected</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <Card className="mb-6 border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 text-red-800">
                <WifiOff className="h-4 w-4" />
                <span className="font-medium">Connection Error</span>
              </div>
              <p className="text-red-700 text-sm mt-1">{error}</p>
              <Button
                variant="outline"
                size="sm"
                className="mt-2"
                onClick={() => window.location.reload()}
              >
                Retry Connection
              </Button>
            </CardContent>
          </Card>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <DateTimePicker
              onDateTimeChange={handleDateTimeChange}
              isLoading={isLoading}
            />

            {healthStatus && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">System Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Models:</span>
                      <span className={healthStatus.models_loaded ? 'text-green-600' : 'text-red-600'}>
                        {healthStatus.models_loaded ? 'Loaded' : 'Not Loaded'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Road Segments:</span>
                      <span>{healthStatus.road_segments_count}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Status:</span>
                      <span className={healthStatus.status === 'healthy' ? 'text-green-600' : 'text-red-600'}>
                        {healthStatus.status}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-3 space-y-6">
            <TrafficMap
              predictions={predictions}
              isLoading={isLoading}
            />

            <PredictionStats
              predictions={predictions}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-600">
            <p>Powered by Machine Learning • Toronto Open Data • FastAPI + Next.js</p>
          </div>
        </div>
      </footer>
    </div>
  );
}