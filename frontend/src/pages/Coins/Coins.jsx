import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { useGetAllCoinsQuery } from '../../services/cryptoAPI';

const Coins = () => {
    const [coins, setCoins] = useState()

    // REDUX TOOLKIT CALL
    const {data, isFetching } = useGetAllCoinsQuery(5)
    // console.log(data)
    
  
    useEffect(() => {
      
        setCoins(data)
  
    },[isFetching])

    return (
        <div className='responsive-container rounded-2xl'>
          <h1 className="text-3xl underlie">Coins</h1>
          <table className="text-lg rounded-2xl mx-auto">
            <thead>
            <tr>
              <th>ID</th>
              <th>CoinGecko ID</th>
              <th>Exchange Name</th>
            </tr>
            </thead>
            <tbody>
          {coins?.map((coin) => (
            <tr key={coin.id} className="even:bg-slate-900 odd:bg-slate-800 hover:bg-sky-900">
              <td>{coin.id}</td>
              <td>{coin.coingecko_id}</td>
              <td>
                  <Link className='link' to={`/coins/${coin.symbol}`}>{coin.name}</Link>
              </td>
            </tr>
          ))}
          </tbody>
          </table>
        </div>
      )
}

export default Coins