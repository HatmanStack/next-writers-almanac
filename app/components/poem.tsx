import React from 'react';
import createDOMPurify from 'dompurify';
import {JSDOM}  from 'jsdom';

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

interface PoemProps {
  poemTitle: string[]; // Assuming an array of titles
  author: string[]; 
  poem: string[];  // Assuming an array of poem lines 
  poemByline: string;
}

const Poem: React.FC<PoemProps> = ({ poemTitle, author, poem, poemByline }) => {
  return (
    <div className="PoemContainer">
        {poemTitle && poemTitle.map((string, index) => (
          <div key={index}>
            <h2><p className="PoemTitle-Day" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poemTitle[index]).replaceAll(/[^\x20-\x7E]/g, '')}}/> </h2>
            {poemTitle.length > 1 && author.length == 1 && index != 0 ? null : (<p className="Author-Day" >by <span dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(author[index]).replaceAll(/[^\x20-\x7E]/g, '')}}/></p>)}
                <br/><br/>
            <div className="Poem-Day" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poem[index]).replaceAll(/[^\x20-\x7E]/g, '')}} />
                <br/><br/>
            {index === poemTitle.length - 1 && <div className="PoemByline" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poemByline).replaceAll(/[^\x20-\x7E]/g, '')}}/>}
          </div>
        ))}
    </div>
  );
};

export default Poem;
