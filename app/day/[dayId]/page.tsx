import Poem from '../../components/poem';
import Note from '../../components/note';

import fs from 'fs';
import path from 'path';

export async function generateStaticParams() {
  return [{ params: { id: '20170101' } }, { params: { id: '02' } }];
}

async function getData(params: { dayId: string }) {
  /**const res = await fetch(
   `https://d3vq6af2mo7fcy.cloudfront.net/public/2017/01/${params.id}.json`
  );
  const data = await res.json();
  return data;**/
  
  //`../../../../Garrison/public/poem/${params.id}.json`
  try {
    const year = params.dayId.slice(0, 4);
    const month = params.dayId.slice(4, 6);

    const filePath = path.join(process.cwd(), '..', '..', 'Garrison', 'public', year, month, `${params.dayId}.json` );
    const fileContents = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(fileContents);
    return data;
  } catch (err) {
    console.error(err);
    return {};
  }
}

export default async function Page({ params }: { params: { dayId: string } }) {
  
  const data = await getData(params);
  
  return (
    <div className="main-content">
      <h1>{data.date}</h1>
      <h3>{data.dayofweek}</h3>
      <Poem
        poemTitle={data.poemtitle}
        poem={data.poem}
        poemByline={data.poembyline}
        author={data.author}
      />
      <Note note={data.notes} />
    </div>
  );
}