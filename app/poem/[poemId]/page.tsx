import PoemDetails from '../../components/poemdetails';
import sortedPoems from '../../../public/Poems_sorted.js';

import fs from 'fs';
import path from 'path';

export async function generateStaticParams() {
  const paths = sortedPoems.map((poem) => ({ params: { poemId: poem } }));
  return paths;
}

async function getData(params: { poemId: string }) {
  /**const res = await fetch(
    `https://d3vq6af2mo7fcy.cloudfront.net/public/authors/${params.peomId}.json`
    );
  const data = await res.json();
  return data; **/

  
//`../../../../Garrison/public/poem/${params.peomId}.json`

  const filePath = path.join(process.cwd(), '..', '..', 'Garrison', 'public', 'poem', `${params.poemId}.json`);
  const fileContents = fs.readFileSync(filePath, 'utf8');
  const data = JSON.parse(fileContents);
  return data;

}

export default async function Page({ params }: { params: { poemId: string } }) {
  const data = await getData(params);
  return (
    <div className="main-content">
      <PoemDetails
        poemTitle={data.poemTitle}
        authorName={data.authorName}
        poem={data.poem}
        analysis={data.analysis}
      />
    </div>
  );
}