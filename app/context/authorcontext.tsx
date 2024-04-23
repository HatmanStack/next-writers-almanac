
'use client'
import React, { createContext, useState, useContext } from 'react';

const AuthorContext = createContext<null | { currentAuthor: string, setCurrentAuthor: React.Dispatch<React.SetStateAction<string>> }>(null);

interface AuthorProviderProps {
    children: React.ReactNode;
  }

export const AuthorProvider: React.FC<AuthorProviderProps> = ({ children })=> {
  const [currentAuthor, setCurrentAuthor] = useState('');

  return (
    <AuthorContext.Provider value={{ currentAuthor, setCurrentAuthor }}>
      {children}
    </AuthorContext.Provider>
  );
};

export const useAuthor = () => {
  const context = useContext(AuthorContext);
  if (context === null) {
    throw new Error('useAuthor must be used within a AuthorProvider');
  }
  return context;
};