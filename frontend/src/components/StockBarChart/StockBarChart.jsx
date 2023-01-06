import { useState, useEffect } from 'react'
import millify from 'millify'
import { Chart } from "react-google-charts";

  export const options = {
    legend: "none",
    bar: { groupWidth: "85%" }, // Remove space between bars.
    candlestick: {
      fallingColor: { strokeWidth: 0, fill: "#a52714" }, // red
      risingColor: { strokeWidth: 0, fill: "#0f9d58" }, // green
    },
  };

const StockBarChart = (props) => {
    const [priceData, setPriceData] = useState([])

    useEffect(() => {
        let array = [["Date", "Low", "Open", "Close", "High"]]
        props.prices?.map((bar) => {
            array.push([bar.date, bar.low, bar.open, bar.close, bar.high])
          })
        setPriceData(array)
    }, [props.prices])

  return (
    <div className=''>
        {console.log(priceData)}
        <div id="chart-candlestick">
            <div className="mixed-chart">
                <Chart
                    chartType="CandlestickChart"
                    width="100%"
                    height="400px"
                    data={priceData}
                    options={options}
                />
          </div>
        </div>
        <div className='mt-8'>
            <table className='responsive-container'>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>High</th>
                        <th>Open</th>
                        <th>Low</th>
                        <th>Close</th>
                        <th>Volume</th>
                    </tr>
                </thead>
                <tbody>
                    {props.prices?.map((bar) => (
                        <tr key={bar.id} className="even:bg-slate-800 odd:bg-slate-700 hover:bg-slate-900">
                            <td>{bar?.date}</td>
                            <td>{bar?.high}</td>
                            <td>{bar?.open}</td>
                            <td>{bar?.low}</td>
                            <td>{bar?.close}</td>
                            <td>{bar?.volume}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    </div>
  )
}

export default StockBarChart