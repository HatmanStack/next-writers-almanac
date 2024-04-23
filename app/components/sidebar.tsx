import React, { useEffect, useState }   from 'react'; 
import Link from 'next/link';
import { usePoem } from '../context/poemcontext';
import { useAuthor } from '../context/authorcontext';


interface SidebarProps {
    isShowingContentByDate: boolean;
    setIsShowingContentByDate: (newState: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isShowingContentByDate, setIsShowingContentByDate }) => {
    const [currentDay, setCurrentDay] = useState('');
    const { currentPoem } = usePoem();
    const { currentAuthor } = useAuthor();

    useEffect(() => {
        const date = new Date();
        const formattedDate = `2013${(date.getMonth() + 1).toString().padStart(2, '0')}${(date.getDate()).toString().padStart(2, '0')}`;
        setCurrentDay(formattedDate);
    }, []);
    return (
        <div className="Sidebar">
            <Link href={`/day/${currentDay}`}>
                <button onClick={() => setIsShowingContentByDate(true)}> Day </button>
            </Link>
            <Link href={`/author/${currentAuthor}`}>
                <button onClick={() => setIsShowingContentByDate(false)}> Author </button>
            </Link>
            <Link href={`/poem/${currentPoem}`}>
                <button onClick={() => setIsShowingContentByDate(false)}> Poem </button>
            </Link>
        </div>
    );
};

export default Sidebar;