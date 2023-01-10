import { Link } from 'react-router-dom'

const Navbar = () => {
    return (
        <div className="nav-bar">
                <div className='flex float-left'>
                    <a href="/">
                        <img 
                            src={require("../../assets/images/Tensai-logo-horizontal-digital.png")}
                            className="w-2/12 ml-10"    
                        />
                    </a>
                </div>
            <div className='flex justify-end mr-10'>
                <ul className='flex justify-end mb-2'>
                    <li className="mr-6"><Link to="/">Home</Link></li>
                    <li className="mr-6"><Link to="/stocks">Stocks</Link></li>
                    <li className="mr-6"><Link to="/crypto">Crypto</Link></li>
                    <li className="mr-6"><Link to="/exchanges">Exchanges</Link></li>
                    <li className=""><Link to="/forex">Forex</Link></li>
                </ul>
            </div>
        </div>
    )
}

export default Navbar