import AuthorDetails from '../../components/authordetails';
import sortedAuthors from '../../../public/Authors_sorted.js';

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

export default async function Page({ params }: { params: { authorId: string } }) {
  const authorId = decodeURIComponent(params.authorId);
  
  const data = await getData(authorId);

  return (
    <main className="main-content">
      {data && ( 
        <AuthorDetails
          authorName={data.authorName}
          biography={data.biography}
          photos={data.photos}
          poems={data.poems}
        />
      )}
    </main>
  );
}

