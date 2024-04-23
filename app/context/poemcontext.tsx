
'use client'
import React, { createContext, useState, useContext } from 'react';

const PoemContext = createContext<null | { currentPoem: string, setCurrentPoem: React.Dispatch<React.SetStateAction<string>> }>(null);

interface PoemProviderProps {
    children: React.ReactNode;
  }

export const PoemProvider: React.FC<PoemProviderProps> = ({ children })=> {
  const [currentPoem, setCurrentPoem] = useState('');

  return (
    <PoemContext.Provider value={{ currentPoem, setCurrentPoem }}>
      {children}
    </PoemContext.Provider>
  );
};

export const usePoem = () => {
  const context = useContext(PoemContext);
  if (context === null) {
    throw new Error('usePoem must be used within a PoemProvider');
  }
  return context;
};