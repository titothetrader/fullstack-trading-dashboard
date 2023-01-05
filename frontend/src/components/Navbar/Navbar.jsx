import { Link } from 'react-router-dom'

const Navbar = () => {
    return (
        <div className="nav-title">
            <h1 className="text-3xl black underline">
                <Link to="/">Navbar</Link>
            </h1>
        </div>
    )
}

export default Navbar