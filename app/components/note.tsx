import React from 'react';
import DOMPurify from 'dompurify';
import divider from '../../public/divider.png';

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
                    <img src={divider} alt="divider" width="10%" height="auto" />
                </div>}
            </div>
        </div>
        ))}
    </div>
  );
};

export default Note;
