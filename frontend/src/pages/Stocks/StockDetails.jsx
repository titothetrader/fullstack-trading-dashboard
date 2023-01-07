import HTMLReactParser from 'html-react-parser'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useGetStockDetailsQuery } from '../../services/stocksAPI'

import { StockBarChart } from '../../components'

const StockDetails = () => {
  const { stockSymbol } = useParams()

  const [stockDetails, setStockDetails] = useState()
  const [stockPrices, setStockPrices] = useState()

  const { data, isFetching } = useGetStockDetailsQuery(stockSymbol)
  
  useEffect(() => {
    setStockDetails(data?.details?.[0])
    setStockPrices(data?.prices)
  }, [isFetching])

  // useEffect(() => {
  //   setBars(barsData?.[`0`])
  //   console.log(barsData)
  // }, [isFetchingBars])


  return (
    <div className='mt-6'>
      <h1 className='text-2xl h-16 underline bold'>
        Stock Details: {stockDetails?.exchange} {'>>'} {stockDetails?.symbol} {'>>'} {stockDetails?.name}
      </h1>
      <h2>{stockDetails?.status} | {stockDetails?.tradable}</h2>
        {!isFetching && stockPrices &&
          <StockBarChart prices={stockPrices} />
        }
    </div>
  )
}

export default StockDetails