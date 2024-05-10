import React from 'react';

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
      <h1>{authorName}</h1>

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
          <p>{biography}</p>
        </div>
      }

      <h2>Poems</h2>
      <ul>
      {poemEntries.map(([poemName, poemUrl]) => (
        <li key={poemName}>
          <a href={poemUrl}>{poemName}</a>
        </li>
      ))}
    </ul>
    </div>
  );
};

export default AuthorDetails;
