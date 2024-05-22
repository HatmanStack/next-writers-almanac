import React from 'react';
import createDOMPurify from 'dompurify';
import {JSDOM}  from 'jsdom';
import Image from 'next/image';
import '../ui/authordetails.css';

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
  photos:  string[] ;  
};

const AuthorDetails: React.FC<AuthorDetailsProps> = ({ authorName, biography, poems, photos }) => {
  const photoUrls = photos ? photos.map(photo => `/image/${photo}`) : [];
  
  const poemEntries = poems ? Object.entries(poems) : [];
  
  return (
    <div className="AuthorDetailsContainer" > 
      <h1 dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(authorName).replaceAll(/[^\x20-\x7E]/g, '')}}/>
      
      {photoUrls.map((photoUrl: string, index) => (
        <img src={photoUrl} alt={`${authorName} photo ${index + 1}`} className="AuthorDetailsPhoto" key={index} />
      ))}
      
      {biography && 
        <div className="AuthorDetailsBiography">
          <p dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(biography).replaceAll(/[^\x20-\x7E]/g, '')}}/>
        </div>
      }
        {poemEntries.length > 0 && 
        <div className="Divider" >
        <Image src='/divider.png'alt="divider" layout="responsive" width={.1} height={.1} />
        </div>}
        <div className="AuthorDetailsPoemEntries">
        {poemEntries.map((website) => {
  const entries = typeof website[1] === 'string' ? JSON.parse(website[1]) : Object.entries(website[1]);
  
  if (Array.isArray(entries) && entries.length > 0) {
    return (
      
        <div>
          <h2 className="AuthorDetailsLinksTitle">{HeadingKey[website[0]]}</h2> 
          <div className="AuthorDetailsLinks">
          <ul>
            {entries.map(([poemTitle, poemUrl]) => (
              <li>
                <a href={poemUrl} dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(poemTitle).replaceAll(/[^\x20-\x7E]/g, '')}} />
              </li>
              
            ))}
          </ul>
        </div>
      </div>
    );
  }
})}
</div>
    </div>
  );
};

export default AuthorDetails;
