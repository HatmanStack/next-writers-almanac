import PoemDetails from '../../components/poemdetails';
import sortedPoems from '../../../public/Poems_sorted.js';
import fs from 'fs';
import path from 'path';

export async function generateStaticParams() {
  const paths = sortedPoems.map((poem) => ({ params: { matchingKey: poem } }));
  return paths;
}

async function getData(params: { poemId: string }) {
  try{
  const filePath = path.join(process.cwd(),  '..', '..', 'Git','garrison', 'public', 'poem',`${params.poemId}.json` );
  const fileContents = fs.readFileSync(filePath, 'utf8');
  const data = JSON.parse(fileContents);
  return data;
  } catch (err) {
    console.error(err);
    return {};
  }
}

export default async function Page({ params }: { params: { poemId: string } }) {
  
  const data = await getData(params);
  
  return (
    <div> 
      <PoemDetails
        poemTitle={data.poemTitle}
        authorName={data.authorName}
        poem={data.poem}
        analysis={data.analysis}
      />
    </div>
  );
}