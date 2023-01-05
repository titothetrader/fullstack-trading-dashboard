import { Link } from 'react-router-dom'

const Navbar = () => {
    return (
        <div className="nav-bar">
                <div className='flex'>
                    <img src="#"/>
                </div>
            <div className=''>
                <ul className='flex justify-end mb-2'>
                    <li className="mr-6"><Link to="/">Home</Link></li>
                    <li className="mr-6"><Link to="/crypto">Crypto</Link></li>
                    <li className="mr-6"><Link to="/fx">Forex</Link></li>
                    <li className="mr-6"><Link to="/stocks">Stocks</Link></li>
                </ul>
            </div>
        </div>
    )
}

export default Navbar