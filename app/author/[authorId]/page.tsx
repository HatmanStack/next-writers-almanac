import AuthorDetails from '../../components/authordetails';
import sortedAuthors from '../../../public/Authors_sorted.js';
import Navigation from '../../components/navigation';
import md from '../../../main_dictionary.json';

import fs from 'fs';
import path from 'path';

export async function generateStaticParams() {
  const paths = sortedAuthors.map((author) => ({ params: { authorId: author } }));
  return paths;
}

async function getData( authorId: string ) {
  
  try {
  const filePath = path.join(process.cwd(), '..', '..', 'Git','garrison', 'public', 'author', `${authorId}.json` );
  const fileContents = fs.readFileSync(filePath, 'utf8');
  const data = JSON.parse(fileContents);
  return data;
  } catch (err) {
    console.error(err);
    return {};
  }
}

interface AuthorData {
  [key: string]: string;
}

export default async function Page({ params }: { params: { authorId: string } }) {
  const authorId = decodeURIComponent(params.authorId);
  
  const mdAuthor: AuthorData = md['author'];
  const data = await getData(authorId);
  const authorsArray = Object.values(mdAuthor)
  
  const matchingKey = authorsArray.findIndex(author => author === authorId + '.json');
  
  const authorCode = matchingKey + 1;

  const prevLink =
  authorCode === 1
    ? '/author/' + mdAuthor[Object.keys(mdAuthor).length.toString()]
    : '/author/' + mdAuthor[(authorCode - 1).toString()];

  const nextLink =
    authorCode === Object.keys(mdAuthor).length
      ? '/author/' + mdAuthor['1']
      : '/author/' + mdAuthor[(authorCode + 1).toString()];

  return (
   
    <div className="content">
      
      <Navigation prevLink={prevLink} nextLink={nextLink}>
      {data && ( 
        <AuthorDetails
          authorName={data.authorName}
          biography={data.biography}
          photos={data.media}
          poems={data.poems}
        />
      )}
      </Navigation>
      
      </div>
     
  );
}

