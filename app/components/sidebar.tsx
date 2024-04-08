import React from 'react'; 
//import { Link } from 'next/link'; // Assuming we'll use Next's Link Component

interface SidebarProps {
    isShowingContentByDate: boolean;
    setIsShowingContentByDate: (newState: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isShowingContentByDate, setIsShowingContentByDate }) => {
    return (
        <div className="Sidebar">
            <button onClick={() => setIsShowingContentByDate(true)}> Day </button>
            <button onClick={() => setIsShowingContentByDate(false)}> Author </button>
            <button onClick={() => setIsShowingContentByDate(false)}> Poem </button> 
            {/* Above will likely need to use Next.js 'Link' Component  */}
        </div>
    );
};

export default Sidebar;
