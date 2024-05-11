import PoemDetails from '../../components/poemdetails';
import sortedPoems from '../../../public/Poems_sorted.js';
import Navigation from '../../components/navigation';
import rd from '../../../randomizedData.json';
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

interface PoemData {
  [key: string]: string;
}

export default async function Page({ params }: { params: { poemId: string } }) {
  
  const rdPoem: PoemData = rd['poem'];
  const data = await getData(poemId);
  const dayArray = Object.values(rdPoem)
  
  const matchingKey = dayArray.findIndex(day => day === poemId);

  const prevLink =
  matchingKey === 0
    ? '/poem/' + rdPoem[Object.keys(rdPoem).length.toString()]
    : '/poem/' + rdPoem[matchingKey.toString()];

  const nextLink =
    matchingKey + 1 === Object.keys(rdPoem).length
      ? '/poem/' + rdPoem[(matchingKey + 2).toString()]
      : '/poem/' + rdPoem['1'];

  
  return (
    <div> 
      <Navigation prevLink={prevLink} nextLink={nextLink}>
      <PoemDetails
        poemTitle={data.poemTitle}
        authorName={data.authorName}
        poem={data.poem}
        analysis={data.analysis}
      />
      </Navigation>
    </div>
  );
}