import Passing from './components/passing'; 
import logo from './logo_writersalmanac.png'; 
import classNames from 'classnames';
import Head from 'next/head'; 
import Image from 'next/image';
import './ui/global.css'

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    
    return (
        <html lang="en">
            <Head>
                <title>The Writer's Almanac</title> 
                <meta name="description" content="Project Description" /> {/* Meta description */}
                {/* Add other SEO meta tags as needed */}
            </Head>
            <body>
            
                <div className="AppHeader">
                    <Image className="LogoImage" src={logo} alt="LOGO" />
                    <div className="FormattingContainer" />
                    {/* Search component will go here */}
                </div>
                <div className={classNames({})}>
                    <Passing>
                    
                    <div className="MainContent">
                        {children}
                    </div>
                    </Passing>
                </div>   
            </body>
        </html>   
    );
};

export default Layout; 
