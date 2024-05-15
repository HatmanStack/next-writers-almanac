import React from 'react';
import createDOMPurify from 'dompurify';
import {JSDOM}  from 'jsdom';

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window)

interface PoemDetailsProps {
  poemtitle: string;
  author: string; 
  poem: string;  
  analysis: string;
}

const PoemDetails: React.FC<PoemDetailsProps> = ({ poemtitle, author, poem, analysis }) => {

  
  return (
    
    <div className="PoemDetailsContainer" style={{ backgroundColor: 'black', color: 'white' }} >  
      <h1 dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poemtitle).replaceAll(/[^\x20-\x7E]/g, '')}}/>
      <p className="author" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(author).replaceAll(/[^\x20-\x7E]/g, '')}}/> 
      <div className="poem-text"  dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poem).replaceAll(/[^\x20-\x7E]/g, '')}}/>
      <br></br>
      <h2>Analysis</h2>
      {analysis && <div className="analysis" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(analysis).replaceAll(/[^\x20-\x7E]/g, '')}}/>}
    </div>
    
  );
};

export default PoemDetails;
