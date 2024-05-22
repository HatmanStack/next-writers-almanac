import React from 'react';
import createDOMPurify from 'dompurify';
import {JSDOM}  from 'jsdom';
import Image from 'next/image';
import '../ui/poemdetails.css';

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
    
    <div className="PoemDetailsContainer" >  
      
      <h1 className="PoemDetailsContainerTitle" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poemtitle).replaceAll(/[^\x20-\x7E]/g, '')}}/>
      
      <p className="PoemDetailsContainerAuthor" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(author).replaceAll(/[^\x20-\x7E]/g, '')}}/> 
      <div className="PoemDetailsContainerPoemText"  dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poem).replaceAll(/[^\x20-\x7E]/g, '')}}/>
      
      <div className="Divider" >
        <Image src='/divider.png'alt="divider" layout="responsive" width={.1} height={.1} />
        </div>
      {analysis && <div className="PoemDetailsContainerAnalysis" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(analysis).replaceAll(/[^\x20-\x7E]/g, '')}}/>}
    </div>
    
  );
};

export default PoemDetails;
