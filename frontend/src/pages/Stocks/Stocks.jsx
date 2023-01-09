import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { getStocks } from '../../services/stocksAPIaxios'
import { useGetStocksQuery } from '../../services/stocksAPI';

const Stocks = (props) => {
    const [stocks, setStocks] = useState()

    // REDUX TOOLKIT CALL
    const {data, isFetching } = useGetStocksQuery(5)
    // console.log(data)
    
  
    useEffect(() => {
      // AXIOS CALL
      // getStocks(10)
      //   .then((data) => {
      //     setStocks(data)
      //   })
      
      setStocks(data)
  
    },[isFetching])

    return (
    <div className='responsive-container rounded-2xl'>
        <h1 className="text-3xl underlie">Stocks</h1>
        <table className="text-2xl rounded-2xl mx-auto">
          <thead>
          <tr>
            <th>ID</th>
            <th>Symbol</th>
            <th>Stock Name</th>
          </tr>
          </thead>
          <tbody>
        {stocks?.map((stock) => (
          <tr key={stock.id} className="even:bg-slate-900 odd:bg-slate-800 hover:bg-sky-900">
            <td>{stock.id}</td>
            <td>{stock.symbol}</td>
            <td>
                <Link className='link' to={`/stocks/${stock.symbol}`}>{stock.name}</Link>
            </td>
          </tr>
        ))}
        </tbody>
        </table>
      </div>
    )
}

export default Stocks