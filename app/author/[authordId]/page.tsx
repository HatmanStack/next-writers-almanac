import AuthorDetails from '../../components/authordetails';
import sortedAuthors from '../../../public/Authors_sorted.js';

import fs from 'fs';
import path from 'path';

export async function generateStaticParams() {
  const paths = sortedAuthors.map((author) => ({ params: { authorId: author } }));
  return paths;
}

async function getData(params: { authorId: string }) {
  /**const res = await fetch(
    `https://d3vq6af2mo7fcy.cloudfront.net/public/authors/${params.authorId}.json`
  );
  const data = await res.json();
  return data;**/
 
  //`../../../../Garrison/public/poem/${params.authorId}.json`
async function getData(params: { authorId: string }) {
  const filePath = path.join(process.cwd(), '..', '..', 'GarrisonNew', 'public', 'author', `${params.authorId}.json`);
  const fileContents = fs.readFileSync(filePath, 'utf8');
  const data = JSON.parse(fileContents);
  return data;
}
}



export default async function Page({ params }: { params: { authorId: string } }) {
  const data = await getData(params);

  return (
    <main className="main-content">
      <AuthorDetails
        authorName={data.authorName}
        biography={data.biography}
        photos={data.photos}
        poems={data.poems}
      />
    </main>
  );
}