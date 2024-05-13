import React from 'react';

interface PoemDetailsProps {
  poemtitle: string;
  author: string; 
  poem: string;  
  analysis: string;
}

const PoemDetails: React.FC<PoemDetailsProps> = ({ poemtitle, author, poem, analysis }) => {

  
  return (
    
    <div className="PoemDetailsContainer" style={{ backgroundColor: 'black', color: 'white' }}>  
      <h1>{poemtitle}</h1>
      <p className="author">By: {author}</p> 
      <div className="poem-text">
        {poem}
      </div>
      {analysis && <div className="analysis">{analysis}</div>}
    </div>
    
  );
};

export default PoemDetails;
