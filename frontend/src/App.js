import { useEffect, useState } from 'react'
import { Routes, Route, Link } from 'react-router-dom'

import { Navbar } from './components';
import { Home, Stocks, StockDetails, Crypto, CryptoDetails, Exchanges, Forex } from './pages'

function App() {


  return (
    <div className="text-center">
      <header className="bg-blue-400">
        <Navbar />
      </header>
      <div>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/stocks' element={<Stocks />} />
          <Route path='/stocks/:stockSymbol' element={<StockDetails />} />
          {/* <Route path='/stocks/:stockId' element={<StockDetails />} /> */}
          <Route path='/crypto' element={<Crypto />} />
          <Route path='/crypto/:cryptoSymbol' element={<CryptoDetails />} />
          <Route path='/exchanges' element={<Exchanges />} />
          <Route path='/forex' element={<Forex />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
