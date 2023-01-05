import { useEffect, useState } from 'react'
import { Navbar } from './components';
import { getStocks } from './services/stocksAPI'

function App() {
  const [stocks, setStocks] = useState()



  useEffect(() => {
    getStocks()
      .then((data) => {
        setStocks(data)
      })
    
  },[])

  return (
    <div className="text-center">
      <header className="bg-blue-400">
        <Navbar />
      </header>
      <div>
        <h1 className="text-3xl underlie text-white">Stocks</h1>
        {stocks?.map((stock) => (
          <li key={stock.id} className="text-2xl text-blue-400">{stock.id}. {stock.symbol}</li>
        ))}
      </div>
    </div>
  );
}

export default App;
