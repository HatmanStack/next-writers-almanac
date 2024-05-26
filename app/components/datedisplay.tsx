'use client';
import React, { useEffect } from 'react';

interface DateDisplayProps {
  onDateChange: (date: Date) => void;
}

const DateDisplay: React.FC<DateDisplayProps> = ({ onDateChange }) => {
  const date = new Date();

  useEffect(() => {
    onDateChange(date);
  }, [date, onDateChange]);

  return <div>{date.toDateString()}</div>;
};

export default DateDisplay;