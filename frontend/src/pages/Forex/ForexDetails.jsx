import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { ApplyStrategy, StockBarChart, TradingViewWidget } from '../../components'

import { useGetForexDetailsQuery } from '../../services/forexAPI'

const ForexDetails = () => {
  const { forexPair } = useParams()

  const [forexPairDetails, setForexPairDetails] = useState()
  const [forexPrices, setForexPrices] = useState()

  const { data: forexData, isFetching: isFetchingForex, isSuccess: isSuccessForex } = useGetForexDetailsQuery(forexPair)

  
  useEffect(() => {
    // console.log(forexData)
    setForexPairDetails(forexData?.details[0])
    setForexPrices(forexData?.prices)
  }, [isFetchingForex])
  
  return (
    <div className='mt-6'>
      <h1 className='text-lg h-16 underline bold'>
        FX Details: {forexPairDetails?.forex_pair} {'>>'} {forexPairDetails?.currency_a} / {forexPairDetails?.currency_b}
      </h1>
        {forexPairDetails &&
          <TradingViewWidget exchange="OANDA" symbol={forexPairDetails?.forex_pair.replace("_","")} />
        }
        <ApplyStrategy assetType="forex" parentSymbol={forexPairDetails?.forex_pair} parentData={forexData} isParentSuccess={isSuccessForex} isParentFetching={isFetchingForex}/>
      <div className='my-8'>
        {forexPairDetails && Object.keys(forexPairDetails).map((key, i) => (
          <div key={i}>
            <div>
              
            </div>
            <p>{key}: {forexPairDetails[key]}</p>
          </div>
        ))}
      </div>
      {!isFetchingForex && forexPrices &&
          <StockBarChart prices={forexPrices} />
        }
    </div>
  )
}

export default ForexDetails