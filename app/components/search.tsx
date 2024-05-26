'use client';
import React, { useState, useEffect } from 'react';
import authorsData from '../authors.json';
import poemsData from '../poems.json';

// Define the type of authorsData and poemsData
const authorsDataTyped: Record<string, string> = authorsData;
const poemsDataTyped: Record<string, string> = poemsData;

// Get the values of authorsData and poemsData
const authors: string[] = Object.values(authorsDataTyped);
const poems: string[] = Object.values(poemsDataTyped);

const AutocompleteInput: React.FC = () => {
  const [input, setInput] = useState('');
  const [matches, setMatches] = useState<string[]>([]);

  useEffect(() => {
    const allOptions= [...authors, ...poems];
    const newMatches = allOptions.filter(option =>
      option.toLowerCase().startsWith(input.toLowerCase())
    );
    setMatches(newMatches);
  }, [input]);

  return (
    <div>
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        list="autocomplete-options"
      />
      <datalist id="autocomplete-options">
        {matches.map((match, index) => (
          <option key={index} value={match} />
        ))}
      </datalist>
    </div>
  );
};

export default AutocompleteInput;