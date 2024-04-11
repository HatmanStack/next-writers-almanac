import React from 'react'; 
import Link from 'next/link';

interface SidebarProps {
    isShowingContentByDate: boolean;
    setIsShowingContentByDate: (newState: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isShowingContentByDate, setIsShowingContentByDate }) => {
    return (
        <div className="Sidebar">
            <Link href="/day">
                <button onClick={() => setIsShowingContentByDate(true)}> Day </button>
            </Link>
            <Link href="/author">
                <button onClick={() => setIsShowingContentByDate(false)}> Author </button>
            </Link>
            <Link href="/poem">
                <button onClick={() => setIsShowingContentByDate(false)}> Poem </button>
            </Link>
        </div>
    );
};

export default Sidebar;