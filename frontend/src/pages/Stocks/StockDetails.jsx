import HTMLReactParser from 'html-react-parser'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useGetStockDetailsQuery } from '../../services/stocksAPI'

import { StockBarChart, ApplyStrategy } from '../../components'
import { TradingViewWidget } from '../../components';

const StockDetails = () => {
  const { stockSymbol } = useParams()

  const [stockDetails, setStockDetails] = useState()
  const [stockPrices, setStockPrices] = useState()

  const { data: stockData, isFetching: isFetchingStocks, isSuccess: isSuccessStocks } = useGetStockDetailsQuery(stockSymbol)


  useEffect(() => {
    setStockDetails(stockData?.details[0])
    setStockPrices(stockData?.prices)
    // {console.log(stockData)}
  }, [isFetchingStocks])


  return (
    <div className='mt-6'>
      <h1 className='text-lg h-16 underline bold'>
        Stock Details: {stockDetails?.exchange} {'>>'} {stockDetails?.symbol} {'>>'} {stockDetails?.name}
      </h1>
      { stockDetails?.exchange &&
        <TradingViewWidget exchange={stockDetails?.exchange} symbol={stockDetails?.symbol} />
      }
      <ApplyStrategy assetType="stock" parentSymbol={stockDetails?.symbol} parentData={stockData} isParentSuccess={isSuccessStocks} isParentFetching={isFetchingStocks}/>
      <div className='my-8'>
        {stockDetails && Object.keys(stockDetails).map((key, i) => (
          <div key={i}> 
            <div>
              
            </div>
            <p>{key}: {stockDetails[key]}</p>
          </div>
        ))}
      </div>
        {!isFetchingStocks && stockPrices &&
          <StockBarChart prices={stockPrices} />
        }
    </div>
  )
}

export default StockDetails