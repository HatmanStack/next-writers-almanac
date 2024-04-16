import Poem from '../../components/poem';
import Note from '../../components/note';


  export async function generateStaticParams() {
    return [{ id: '01' }, { id: '02' }]
  }

  async function getData(params) {
    const res = await fetch(`https://d3vq6af2mo7fcy.cloudfront.net/public/2017/01/${params.id}.json`)
    const data = await res.text()
   
    return data
  }

  export default async function Page({ params }) {
    const data = await getData(params)
   
    return (
      <div className="main-content">
      {/* Render day-specific data here */}
      <h1>{data.date}</h1>
      <h3>{data.dayOfWeek}</h3> 
      {/* ...Other Day components for transcript, etc. */}
  
      {/* TRANSCRIPT BUTTON */}
      <Poem 
        poemTitle={data.poemTitle}
        poem={data.poem}
        poemByline={data.poemByline}
        author={data.author}
      />
      <Note note={data.notes} />
    </div>
    ); 
  }