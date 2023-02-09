import { useEffect, useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useLocation } from 'react-router-dom'

import { getStocks } from '../../services/stocksAPIaxios'
import { useGetStocksQuery } from '../../services/stocksAPI';

import LoadingSpinner from '../../components/Global/LoadingSpinner/LoadingSpinner'

const Stocks = () => {
  const queryParams = new URLSearchParams(window.location.search)
  const filter = queryParams.get("filter")
  // console.log(filter)
  
  const [stocks, setStocks] = useState()

  // REDUX TOOLKIT CALL
  const {data, isFetching } = useGetStocksQuery({limit: 10, filter: filter})
  // console.log(data)

  useEffect(() => {    
    setStocks(data)
  },[isFetching])

  return (
    <div className='responsive-container rounded-2xl'>
      <h1 className="text-3xl underline">Stocks</h1>
      
      <form method='get' action="/stocks" >
        <select name="filter">
          <option value="">All Stocks</option>
          <option value="new_intraday_highs">New Intraday Highs</option>
          <option value="new_closing_highs">New Closing Highs</option>
          <option value="new_intraday_lows">New Intraday Lows</option>
          <option value="new_closing_lows">New Closing Lows</option>
        </select>
        <button type="submit" className='block mx-auto'>Submit</button>
      </form>

      {isFetching &&
        <LoadingSpinner />
      }
      {!isFetching && stocks?.length > 0 &&
        <table className="text-lg rounded-2xl mx-auto">
          {/* {console.log(stocks)} */}
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
      }
      {!isFetching && stocks?.length < 1 &&
        <div>
          No results found
        </div>
      }
    </div>
  )
}

export default Stocks