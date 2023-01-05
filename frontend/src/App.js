import { useEffect, useState } from 'react'
import { Navbar } from './components';
import { getStocks } from './services/stocksAPIaxios'
import { useGetStocksQuery } from './services/stocksAPI';

function App() {
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
    <div className="text-center">
      <header className="bg-blue-400">
        <Navbar />
      </header>
      <div>
        <h1 className="text-3xl underlie text-white">Stocks</h1>
        <table className="text-2xl text-blue-400">
          <thead>
          <tr>
            <th>ID</th>
            <th>Symbol</th>
            <th>Stock Name</th>
          </tr>
          </thead>
          <tbody>
        {stocks?.map((stock) => (
          <tr key={stock.id}>
            <td>{stock.id}</td>
            <td>{stock.symbol}</td>
            <td>{stock.name}</td>
          </tr>
        ))}
        </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
