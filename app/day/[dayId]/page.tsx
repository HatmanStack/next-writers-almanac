import Poem from '../../components/poem';
import Note from '../../components/note';
import fs from 'fs';
import path from 'path';

export async function generateStaticParams() {
  return [{ params: { id: '20170101' } }, { params: { id: '02' } }];
}

async function getData(params: { dayId: string }) {
  
  try {
    const year = params.dayId.slice(0, 4);
    const month = params.dayId.slice(4, 6);

    const filePath = path.join(process.cwd(), '..', '..', 'Git','garrison', 'public', 'day', year, month, `${params.dayId}.json` );
    console.log(filePath)
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
      <script id="server-data" type="application/json">
        {JSON.stringify(data)}
      </script>
    </div>
  );
}