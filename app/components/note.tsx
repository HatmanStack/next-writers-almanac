import React from 'react';

import Image from 'next/image';

import createDOMPurify from 'dompurify';
import {JSDOM}  from 'jsdom';
import '../ui/daydetails.css';

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

interface NoteProps {
  notes: string[]; // Array of note paragraphs
}

const Note: React.FC<NoteProps> = ({ notes }) => {
    return (
    <div className="DayDetailsNoteContainer">
      
      <div className="DayDetailsNoteTitle" >History</div>
            
      {notes && notes.map((note, noteIndex) => {
      const parts = DOMPurify.sanitize(note).replaceAll(/[^\x20-\x7E]/g, '').split('</br></br>');
      return (
        <div key={noteIndex}>
          {parts.map((part, partIndex) => (
            <div className="DayDetailsNoteParagraph" key={partIndex} dangerouslySetInnerHTML={{ __html: part }} />
          ))}
          {noteIndex < notes.length - 1 && 
            <div className="DividerMarginTop">
              <Image src='/divider.png' alt="divider" layout="responsive" width={.1} height={.1} />
            </div>
          }
        </div>
      );
    })}
    
    </div>
    );
};

export default Note;
