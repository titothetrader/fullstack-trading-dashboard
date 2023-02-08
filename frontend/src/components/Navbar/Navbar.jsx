import { Link } from 'react-router-dom'

const Navbar = () => {
    return (
        <div className='nav-bar flex flex-col float-left top-0'>
            <div>
                <a href="/">
                    <img
                        src={require("../../assets/images/Tensai-logo-horizontal-digital.png")}
                        className="w-6/12 mx-auto"
                    />
                </a>
            </div>
            <div className='my-44'>
                <ul className='mb-2'>
                    <li className="m-6"><Link to="/">Home</Link></li>
                    <li className="m-6"><Link to="/stocks">Stocks</Link></li>
                    <li className="m-6"><Link to="/crypto">Crypto</Link></li>
                    <li className="m-6"><Link to="/coins">Coins</Link></li>
                    <li className="m-6"><Link to="/exchanges">Exchanges</Link></li>
                    {/* <li className="m-6"><Link to="/commodities">Commodities</Link></li> */}
                    <li className="m-6"><Link to="/forex">Forex</Link></li>
                    <li className=""><Link to="/strategies">Strategies</Link></li>
                </ul>
            </div>
        </div>
    )
}

export default Navbar