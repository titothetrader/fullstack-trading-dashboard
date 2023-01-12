import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { useGetCryptosQuery } from '../../services/cryptoAPI';

const Crypto = () => {
  const [cryptos, setCryptos] = useState()
  const [cryptoSlug, setCryptoSlug] = useState()

    // REDUX TOOLKIT CALL
    const {data, isFetching } = useGetCryptosQuery(5)
    // console.log(data)

    useEffect(() => {
      // AXIOS CALL
      // getStocks(10)
      //   .then((data) => {
      //     setStocks(data)
      //   })
      
      setCryptos(data)
      
    },[isFetching])

    return (
      <div className='responsive-container rounded-2xl'>
        <h1 className="text-3xl underlie">Cryptos</h1>
        <table className="text-lg rounded-2xl mx-auto">
          <thead>
          <tr>
            <th>ID</th>
            <th>Symbol</th>
            <th>Crypto Name</th>
          </tr>
          </thead>
          <tbody>
        {cryptos?.map((crypto) => (
          <tr key={crypto.id} className="even:bg-slate-900 odd:bg-slate-800 hover:bg-sky-900">
            {}
            <td>{crypto.id}</td>
            <td>{crypto.symbol}</td>
            <td>
                <Link className='link' to={`/crypto/${crypto.symbol.replace("/", "-")}`}>{crypto.name}</Link>
            </td>
          </tr>
        ))}
        </tbody>
        </table>
      </div>
    )
}

export default Crypto