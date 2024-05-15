import React from 'react';
import divider from '../../public/divider.png';
import Image from 'next/image';

import createDOMPurify from 'dompurify';
import {JSDOM}  from 'jsdom';

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

interface NoteProps {
  note: string[]; // Array of note paragraphs
}

const Note: React.FC<NoteProps> = ({ note }) => {
    return (
    <div>
      <br></br>
      {note && note.map((string, index) => (
      <div className="Note-Day" >
        <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(string).replaceAll(/[^\x20-\x7E]/g, '') }} />
          <div>{index < note.length - 1 && 
            <div className="Divider" style={{ backgroundColor: 'black', color: 'white' }}>
          <br></br>
            <Image src='/divider.png'alt="divider" layout="responsive" width={.1} height={.1} />
          </div>}
        </div>
      </div>
      ))}
    </div>
    );
};

export default Note;
