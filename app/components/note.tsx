import React from 'react';

import Image from 'next/image';

import createDOMPurify from 'dompurify';
import {JSDOM}  from 'jsdom';
import '../ui/daydetails.css';

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

interface NoteProps {
  note: string[]; // Array of note paragraphs
}

const Note: React.FC<NoteProps> = ({ note }) => {
    return (
    <div className="DayDetailsNoteContainer">
      
      <div className="DayDetailsNoteTitle" >History</div>
            
      {note && note.map((string, index) => (
      <div className="DayDetailsNote" >
        <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(string).replaceAll(/[^\x20-\x7E]/g, '') }} />
          <div>{index < note.length - 1 && 
            <div className="DividerMarginTop" >
          
            <Image src='/divider.png'alt="divider" layout="responsive" width={.1} height={.1} />
          </div>}
        </div>
      </div>
      ))}
    </div>
    );
};

export default Note;
