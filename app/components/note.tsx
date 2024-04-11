import React from 'react';
import DOMPurify from 'dompurify';
import divider from '../../public/divider.png';
import Image from 'next/image';

interface NoteProps {
  note: string[]; // Array of note paragraphs
}

const Note: React.FC<NoteProps> = ({ note }) => {
    return (
    <div>
      {note && note.map((string, index) => (
      <div className="Note-Day">
        <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(string).replaceAll(/[^\x20-\x7E]/g, '') }} />
          <div>{index < note.length - 1 && 
            <div className="Divider">
          <br></br>
            <Image src={divider} alt="divider" width={10} height={undefined} />
          </div>}
        </div>
      </div>
      ))}
    </div>
    );
};

export default Note;
