import React from 'react';

interface PoemDetailsProps {
  poemTitle: string;
  authorName: string; 
  poem: string;  
  analysis?: string;
}

const PoemDetails: React.FC<PoemDetailsProps> = ({ poemTitle, authorName, poem, analysis }) => {
  return (
    <div className="PoemDetailsContainer"> 
      <h1>{poemTitle}</h1>
      <p className="author">By: {authorName}</p> 
      <div className="poem-text">
        {poem}
      </div>
      {analysis && <div className="analysis">{analysis}</div>}
    </div>
  );
};

export default PoemDetails;
