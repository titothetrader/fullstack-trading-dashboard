import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { useGetCryptoExchangesQuery } from '../../services/cryptoAPI';

const Exchanges = () => {
  const [exchanges, setExchanges] = useState()

  // REDUX TOOLKIT CALL
  const {data, isFetching } = useGetCryptoExchangesQuery(5)
  // console.log(data)
  

  useEffect(() => {
    
    setExchanges(data)

  },[isFetching])

  return (
    <div className='responsive-container rounded-2xl'>
      <h1 className="text-3xl underlie">Exchanges</h1>
      <table className="text-lg rounded-2xl mx-auto">
        <thead>
        <tr>
          <th>ID</th>
          <th>CoinGecko ID</th>
          <th>Exchange Name</th>
        </tr>
        </thead>
        <tbody>
      {exchanges?.map((exchange) => (
        <tr key={exchange.id} className="even:bg-slate-900 odd:bg-slate-800 hover:bg-sky-900">
          <td>{exchange.id}</td>
          <td>{exchange.coingecko_id}</td>
          <td>
              <Link className='link' to={`/exchanges/${exchange.coingecko_id}`}>{exchange.name}</Link>
          </td>
        </tr>
      ))}
      </tbody>
      </table>
    </div>
  )
}

export default Exchanges