import { useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom'
import { useMediaQuery } from 'react-responsive'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faEnvelope, faDiamond, faSquare, faCopy, faCircleHalfStroke, faCircleDot, faCircle, faCrosshairs } from '@fortawesome/free-solid-svg-icons'


const Navbar = () => {
    const isMobile = useMediaQuery({ query: `(max-width: 760px)`})

    useEffect(()=>{
        
    }, [])

    return (
        <div className='nav-bar flex flex-col float-left'>
            {console.log(useLocation().pathname)}
            <div>
                <a href="/">
                    <img
                        src={require("../../assets/images/Tensai-logo-horizontal-digital.png")}
                        className="w-6/12 mx-auto hidden md:block"
                    />
                    <img
                        src={require("../../assets/images/Tensai-logo-symbol.png")}
                        className="w-6/12 mx-auto block md:hidden"
                    />
                </a>
            </div>
            <div className='my-44'>
                <ul className='w-full flex flex-col'>
                    <li className={useLocation().pathname === '/' ? 'selected' : ''}>
                        <Link to="/" className='md:p-0 md:space-x-5'>
                            <span className='hidden md:inline-block'>Dashboard</span>
                            <FontAwesomeIcon icon={faDiamond} size={isMobile ? '2xl' : 'md'} className='pt-3 md:pt-0'/>
                        </Link>
                    </li>
                    <li className={useLocation().pathname === '/stocks' ? 'selected' : ''}>
                        <Link to="/stocks" className='md:p-0 md:space-x-5'>
                            <span className='hidden md:inline-block'>Stocks</span>
                            <FontAwesomeIcon icon={faSquare} size={isMobile ? '2xl' : 'md'} className='pt-3 md:pt-0'/>
                        </Link>
                    </li>
                    <li className={useLocation().pathname === '/forex' ? 'selected' : ''}>
                        <Link to="/forex" className='md:p-0 md:space-x-5'>
                            <span className='hidden md:inline-block'>Forex</span>
                            <FontAwesomeIcon icon={faCopy} size={isMobile ? '2xl' : 'md'} className='pt-3 md:pt-0'/>
                        </Link>        
                    </li>
                    <li className={useLocation().pathname === '/crypto' ? 'selected' : ''}>
                        <Link to="/crypto" className='md:p-0 md:space-x-5'>
                            <span className='hidden md:inline-block'>Crypto</span>
                            <FontAwesomeIcon icon={faCircleHalfStroke} size={isMobile ? '2xl' : 'md'} className='pt-3 md:pt-0'/>
                        </Link>
                    </li>
                    <li className={useLocation().pathname === '/coins' ? 'selected' : ''}>
                        <Link to="/coins" className='md:p-0 md:space-x-5'>
                            <span className='hidden md:inline-block'>Coins</span>
                            <FontAwesomeIcon icon={faCircleDot} size={isMobile ? '2xl' : 'md'} className='pt-3 md:pt-0'/>
                        </Link>        
                    </li>
                    <li className={useLocation().pathname === '/exchanges' ? 'selected' : ''}>
                        <Link to="/exchanges" className='md:p-0 md:space-x-5'>
                            <span className='hidden md:inline-block'>Exchanges</span>
                            <FontAwesomeIcon icon={faCircle} size={isMobile ? '2xl' : 'md'} className='pt-3 md:pt-0'/>
                        </Link>
                    </li>
                    {/* <li className="m-6"><Link to="/commodities">Commodities</Link></li> */}
                    <li className={useLocation().pathname === '/strategies' ? 'selected' : ''}>
                        <Link to="/strategies" className='md:p-0 md:space-x-5'>
                            <span className='hidden md:inline-block'>Strategies</span>
                            <FontAwesomeIcon icon={faCrosshairs} size={isMobile ? '2xl' : 'md'} className='pt-3 md:pt-0'/>
                        </Link>
                    </li>
                </ul>
            </div>
        </div>
    )
}

export default Navbar