import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { useGetAllForexQuery } from '../../services/forexAPI'


const Forex = () => {
  const [forexPairs, setforexPairs] = useState()

  // REDUX TOOLKIT CALL
  const {data, isFetching } = useGetAllForexQuery(5)
  // console.log(data)
  

  useEffect(() => {
    
    setforexPairs(data)

  },[isFetching])

  return (
    <div className='responsive-container rounded-2xl'>
      <h1 className="text-3xl underlie">Forex</h1>
      <table className="text-lg rounded-2xl mx-auto">
        <thead>
        <tr>
          <th>Pair</th>
          <th>Countries</th>
          <th>Currencies</th>
        </tr>
        </thead>
        <tbody>
      {forexPairs?.map((forex) => (
        <tr key={forex.forex_pair} className="even:bg-slate-900 odd:bg-slate-800 hover:bg-sky-900">
          <td>
          <Link className='link' to={`/forex/${forex.forex_pair}`}>{forex.forex_pair}</Link>
          </td>
          <td>{forex.country_a} / {forex.country_b}</td>
          <td>{forex.currency_a} / {forex.currency_b}</td>
        </tr>
      ))}
      </tbody>
      </table>
    </div>
  )
}

export default Forex