import PoemDetails from '../../components/poemdetails';
import sortedPoems from '../../../public/Poems_sorted.js';
import Navigation from '../../components/navigation';
import md from '../../../main_dictionary.json';
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
  
  const mdPoem: PoemData = md['poem'];
  const data = await getData(params);
  const dayArray = Object.values(mdPoem)
  
  const matchingKey = dayArray.findIndex(day => day === params.poemId + '.json');
  const poemCode = matchingKey + 1;

  const prevLink =
  poemCode === 1
    ? '/poem/' + mdPoem[Object.keys(mdPoem).length.toString()]
    : '/poem/' + mdPoem[(poemCode - 1).toString()];

  const nextLink =
    poemCode === Object.keys(mdPoem).length
      ? '/poem/' + mdPoem['1']
      : '/poem/' + mdPoem[(poemCode + 1).toString()];

  
  return (
 
  <div className="content">
    
    <Navigation prevLink={prevLink} nextLink={nextLink}>
      <PoemDetails
        poemtitle={data.poemtitle}
        author={data.author}
        poem={data.poem}
        analysis={data.analysis}
      />
    </Navigation>
    
  </div>
 
  );
}