'use client';

import React, { useState } from 'react';
import { formatDateTime, parseDateTime } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Calendar, Clock } from 'lucide-react';

interface DateTimePickerProps {
  onDateTimeChange: (dateTime: string) => void;
  isLoading?: boolean;
  className?: string;
}

export default function DateTimePicker({ onDateTimeChange, isLoading = false, className }: DateTimePickerProps) {
  const [dateTime, setDateTime] = useState<string>(formatDateTime(new Date()));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onDateTimeChange(dateTime);
  };

  const handleQuickSelect = (hours: number) => {
    const now = new Date();
    now.setHours(now.getHours() + hours);
    const newDateTime = formatDateTime(now);
    setDateTime(newDateTime);
    onDateTimeChange(newDateTime);
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="h-5 w-5" />
          Prediction Time
        </CardTitle>
        <CardDescription>
          Select a date and time to predict traffic conditions
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="datetime">Date & Time</Label>
            <Input
              id="datetime"
              type="datetime-local"
              value={dateTime}
              onChange={(e) => setDateTime(e.target.value)}
              className="w-full"
            />
          </div>
          
          <div className="space-y-2">
            <Label>Quick Select</Label>
            <div className="flex gap-2 flex-wrap">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => handleQuickSelect(0)}
                disabled={isLoading}
              >
                Now
              </Button>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => handleQuickSelect(1)}
                disabled={isLoading}
              >
                +1 Hour
              </Button>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => handleQuickSelect(2)}
                disabled={isLoading}
              >
                +2 Hours
              </Button>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => handleQuickSelect(24)}
                disabled={isLoading}
              >
                Tomorrow
              </Button>
            </div>
          </div>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                Predicting...
              </>
            ) : (
              <>
                <Calendar className="h-4 w-4 mr-2" />
                Predict Traffic
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}