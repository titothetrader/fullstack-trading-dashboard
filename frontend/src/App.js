import { useEffect, useState } from 'react'
import { Routes, Route, Link } from 'react-router-dom'

import { Navbar } from './components';
import { Home, Stocks, StockDetails, Crypto, CryptoDetails, Coins, CoinDetails, Exchanges, ExchangeDetails, Commodities, Forex, ForexDetails, Strategies, StrategyDetails } from './pages'

function App() {


  return (
    <div className="text-center">
      <header className="">
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
          <Route path='/coins' element={<Coins />} />
          <Route path='/coins/:coinSymbol' element={<CoinDetails />} />
          <Route path='/exchanges' element={<Exchanges />} />
          <Route path='/exchanges/:exchangeId' element={<ExchangeDetails />} />          
          <Route path='/commodities' element={<Commodities />} />
          <Route path='/forex' element={<Forex />} />
          <Route path='/forex/:forexPair' element={<ForexDetails />} />
          <Route path='/strategies' element={<Strategies />} />
          <Route path='/strategies/:strategyCode' element={<StrategyDetails />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
