import Poem from '../../components/poem';
import Note from '../../components/note';
import fs from 'fs';
import path from 'path';
import Navigation from '../../components/navigation';
import md from '../../../main_dictionary.json';

export async function generateStaticParams() {
  return [{ params: { id: '20170101' } }, { params: { id: '02' } }];
}

async function getData(params: { dayId: string }) {
  
  try {
    const year = params.dayId.slice(0, 4);
    const month = params.dayId.slice(4, 6);

    const filePath = path.join(process.cwd(), '..', '..', 'Git','garrison', 'public', 'day', year, month, `${params.dayId}.json` );
    
    const fileContents = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(fileContents);
    return data;
  } catch (err) {
    console.error(err);
    return {};
  }
}

interface DayData {
  [key: string]: string;
}

export default async function Page({ params }: { params: { dayId: string } }) {
  
  const mdDay: DayData = md['day'];
  const data = await getData(params);
  const dayArray = Object.values(mdDay)
  
  const matchingKey = dayArray.findIndex(day => day === params.dayId + '.json');
  
  const dayCode = matchingKey + 1;

  const prevLink =
  dayCode === 1
    ? '/day/' + mdDay[Object.keys(mdDay).length.toString()]
    : '/day/' + mdDay[(dayCode - 1).toString()];

  const nextLink =
    dayCode === Object.keys(mdDay).length
      ? '/day/' + mdDay['1']
      : '/day/' + mdDay[(dayCode + 1).toString()];

      ;
  return (
   
    <div className="content">
      
      <Navigation prevLink={prevLink} nextLink={nextLink}>
    
      <h1>{data.date}</h1>
      <h3>{data.dayofweek}</h3>
      <Poem
        poemTitle={data.poemtitle}
        poem={data.poem}
        poemByline={data.poembyline}
        author={data.author}
      />
      <Note note={data.notes} />
      <script id="server-data" type="application/json">
        {JSON.stringify(data)}
      </script>
      </Navigation>
      
      </div>
      
  );
}