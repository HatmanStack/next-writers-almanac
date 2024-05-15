import React from 'react';
import createDOMPurify from 'dompurify';
import {JSDOM}  from 'jsdom';

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window)

const HeadingKey: {
  poetsorg: string;
  allpoetry: string;
  poetryfoundation: string;
  writersAlmanac: string;
  [key: string]: string;
} = {
  poetsorg: 'Poets.org',
  allpoetry: 'All Poetry',
  poetryfoundation: 'Poetry Foundation',
  writersAlmanac: 'Writers Almanac',
};


type AuthorDetailsProps = {
  authorName: string;
  biography: string;
  poems: { [key: string]: string };
  photos: { [key: string]: string | { image: string; credit: string } };
  
};

const AuthorDetails: React.FC<AuthorDetailsProps> = ({ authorName, biography, poems, photos }) => {
  const photoUrls = photos ? Object.values(photos).map(photo => typeof photo === 'string' ? photo : photo.image) : [];
  
  const poemEntries = poems ? Object.entries(poems) : [];
  
  return (
    <div className="AuthorDetailsContainer" style={{ backgroundColor: 'black', color: 'white' }}> 
      <h1 dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(authorName).replaceAll(/[^\x20-\x7E]/g, '')}}/>

      {photoUrls.length > 0 && (
        <div className="authorPhotos" style={{ backgroundColor: 'black', color: 'white' }}>
          {photoUrls.map((photoUrl, index) => (
            <img src={photoUrl} alt={`${authorName} photo ${index + 1}`} className="authorPhoto" key={index} />
          ))}
        </div>
      )}

      {biography && 
        <div className="biography">
          <h2>Biography</h2>
          <p dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(biography).replaceAll(/[^\x20-\x7E]/g, '')}}/>
        </div>
      }
        <h2>Poems</h2>
        {poemEntries.map((website) => {
          
          return (
            <div >
              <h2>{HeadingKey[website[0]]}</h2> 
              <ul>
                {Object.entries(website[1]).map(([poemTitle, poemUrl]) => (
                  <li key={poemTitle}>
                    <a href={poemUrl} dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poemTitle).replaceAll(/[^\x20-\x7E]/g, '')}} />
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
    </div>
  );
};

export default AuthorDetails;
