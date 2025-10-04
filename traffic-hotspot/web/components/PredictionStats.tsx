'use client';

import React from 'react';
import { TrafficPrediction } from '@/lib/types';
import { getTrafficColor } from '@/lib/utils';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart3, Car, TrendingUp, AlertTriangle } from 'lucide-react';

interface PredictionStatsProps {
  predictions: TrafficPrediction[];
  className?: string;
}

export default function PredictionStats({ predictions, className }: PredictionStatsProps) {
  if (predictions.length === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Traffic Statistics
          </CardTitle>
          <CardDescription>
            No predictions available
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-sm">Select a time to see traffic statistics</p>
        </CardContent>
      </Card>
    );
  }

  // Calculate statistics
  const totalVehicles = predictions.reduce((sum, p) => sum + p.predicted_vehicles, 0);
  const avgVehicles = Math.round(totalVehicles / predictions.length);
  
  const congestionCounts = predictions.reduce((acc, p) => {
    acc[p.congestion_level] = (acc[p.congestion_level] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const congestionPercentages = {
    Low: Math.round((congestionCounts.Low || 0) / predictions.length * 100),
    Medium: Math.round((congestionCounts.Medium || 0) / predictions.length * 100),
    High: Math.round((congestionCounts.High || 0) / predictions.length * 100),
  };

  const busiestLocation = predictions.reduce((max, p) => 
    p.predicted_vehicles > max.predicted_vehicles ? p : max
  );

  const quietestLocation = predictions.reduce((min, p) => 
    p.predicted_vehicles < min.predicted_vehicles ? p : min
  );

  return (
    <div className={className}>
      {/* Main Stats Card */}
      <Card className="mb-4">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Traffic Overview
          </CardTitle>
          <CardDescription>
            Summary of {predictions.length} road segments
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{avgVehicles}</div>
              <div className="text-sm text-muted-foreground">Avg Vehicles</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{totalVehicles}</div>
              <div className="text-sm text-muted-foreground">Total Vehicles</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Congestion Distribution */}
      <Card className="mb-4">
        <CardHeader>
          <CardTitle className="text-lg">Congestion Distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {(['Low', 'Medium', 'High'] as const).map((level) => (
              <div key={level} className="flex items-center gap-3">
                <div
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: getTrafficColor(level) }}
                />
                <div className="flex-1">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{level}</span>
                    <span>{congestionCounts[level] || 0} segments ({congestionPercentages[level]}%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                    <div
                      className="h-2 rounded-full"
                      style={{
                        width: `${congestionPercentages[level]}%`,
                        backgroundColor: getTrafficColor(level)
                      }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Busiest & Quietest Locations */}
      <div className="grid grid-cols-1 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <TrendingUp className="h-4 w-4" />
              Busiest Location
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-1">
              <div className="font-medium text-sm">{busiestLocation.location_name}</div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Car className="h-3 w-3" />
                {busiestLocation.predicted_vehicles} vehicles
                <span
                  className="px-2 py-1 rounded text-white text-xs font-medium ml-auto"
                  style={{ backgroundColor: getTrafficColor(busiestLocation.congestion_level) }}
                >
                  {busiestLocation.congestion_level}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <AlertTriangle className="h-4 w-4" />
              Quietest Location
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-1">
              <div className="font-medium text-sm">{quietestLocation.location_name}</div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Car className="h-3 w-3" />
                {quietestLocation.predicted_vehicles} vehicles
                <span
                  className="px-2 py-1 rounded text-white text-xs font-medium ml-auto"
                  style={{ backgroundColor: getTrafficColor(quietestLocation.congestion_level) }}
                >
                  {quietestLocation.congestion_level}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}