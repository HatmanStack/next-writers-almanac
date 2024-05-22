import React from 'react';
import createDOMPurify from 'dompurify';
import {JSDOM}  from 'jsdom';
import '../ui/daydetails.css';


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
    <div className="DayDetailsPoemContainer">
        {poemTitle && poemTitle.map((string, index) => (
          <div key={index}>
            <h2><p className="DayDetailsTitle" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poemTitle[index]).replaceAll(/[^\x20-\x7E]/g, '')}}/> </h2>
            {poemTitle.length > 1 && author.length == 1 && index != 0 ? null : (<p className="DayDetailsAuthor" ><span dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(author[index]).replaceAll(/[^\x20-\x7E]/g, '')}}/></p>)}
                
            <div className="DayDetailsPoem" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poem[index]).replaceAll(/[^\x20-\x7E]/g, '')}} />
                
            {index === poemTitle.length - 1 && <div className="DayDetailsByLine" dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poemByline).replaceAll(/[^\x20-\x7E]/g, '')}}/>}
          </div>
        ))}
    </div>
  );
};

export default Poem;
