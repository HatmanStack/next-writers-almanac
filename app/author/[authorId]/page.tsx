import AuthorDetails from '../../components/authordetails';
import sortedAuthors from '../../../public/Authors_sorted.js';
import Navigation from '../../components/navigation';
import rd from '../../../randomizedData.json';

import fs from 'fs';
import path from 'path';

export async function generateStaticParams() {
  const paths = sortedAuthors.map((author) => ({ params: { authorId: author } }));
  return paths;
}

async function getData( authorId: string ) {
  
  try {
  const filePath = path.join(process.cwd(), '..', '..', 'Git','garrison', 'public', 'author', `${authorId}.json` );
  console.log(filePath)
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
  
  const rdAuthor: AuthorData = rd['author'];
  const data = await getData(authorId);
  const authorsArray = Object.values(rdAuthor)
  
  const matchingKey = authorsArray.findIndex(author => author === authorId);

  const prevLink =
  matchingKey === 0
    ? '/author/' + rdAuthor[Object.keys(rdAuthor).length.toString()]
    : '/author/' + rdAuthor[matchingKey.toString()];

  const nextLink =
    matchingKey + 1 === Object.keys(rdAuthor).length
      ? '/author/' + rdAuthor[(matchingKey + 2).toString()]
      : '/author/' + rdAuthor['1'];

  return (
    <div className="main-content">
      <Navigation prevLink={prevLink} nextLink={nextLink}>
      {data && ( 
        <AuthorDetails
          authorName={data.authorName}
          biography={data.biography}
          photos={data.photos}
          poems={data.poems}
        />
      )}
      </Navigation>
    </div>
  );
}

