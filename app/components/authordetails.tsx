import React from 'react';
import Link from 'next/link';

interface AuthorDetailsProps {
  authorName: string;
  biography: string;
  poems: { [poemName: string]: string }; // Link to the poem content
  photos?: string[]; // Optional if you have author photos
}

const AuthorDetails: React.FC<AuthorDetailsProps> = ({ authorName, biography, poems, photos}) => {
  return (
    <div className="AuthorDetailsContainer"> 
      <h1>{authorName}</h1>

      {photos && photos.length > 0 && (
        <div className="authorPhotos">
          {photos.map((photoUrl, index) => (
            <img src={photoUrl} alt={`${authorName} photo ${index + 1}`} className="authorPhoto" key={index} />
          ))}
        </div>
      )}

      {biography && 
        <div className="biography">
          <h2>Biography</h2>
          <p>{biography}</p>
        </div>
      }

      <h2>Poems</h2>
      <ul>
        {Object.entries(poems).map(([poemName, poemUrl]) => (
          <li key={poemName}>
            <Link href={`/poem/${poemName}`}>
              <a>{poemName}</a>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AuthorDetails;
