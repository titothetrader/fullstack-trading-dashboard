import { useState, useEffect } from 'react'
import millify from 'millify'

import { Chart } from "react-google-charts";


  export const chartOptions = {
    legend: "none",
    bar: { groupWidth: "85%" }, // Remove space between bars.
    candlestick: {
        fallingColor: { strokeWidth: 0, fill: "red" }, // red
        risingColor: { strokeWidth: 0, fill: "green" }, // green
        },
    series: {
        4: {
            type: 'bar'
        }
    }
  };

  export const lineOptions = {
    legend: "none",
    curveType: 'function',
    series: {
        1: {
            type: 'line',
        }
    }
  }

  export const comboOptions = {
    title : 'Monthly Coffee Production by Country',
    vAxis: {title: 'Cups'},
    hAxis: {title: 'Month'},
    seriesType: "candlesticks",
    candlestick: {
        fallingColor: { strokeWidth: 0, fill: "red" }, // red
        risingColor: { strokeWidth: 0, fill: "green" }, // green
        },
    series: {
        1: { type: "line",
             curveType: "function" },
        2: { type: "bars",
           }
      }
  };

const StockBarChart = (props) => {
    const [priceData, setPriceData] = useState([])
    const [priceAvg, setPriceAvg] = useState([])
    const [comboArray, setComboArray] = useState([])

    useEffect(() => {
        let array = [["Date", "Low", "Open", "Close", "High"]]
        let averages = [["Date", "Average"]]
        let comboArray = [["Date", "Low", "Open", "Close", "High", "Average", "Volume"]]
        props.prices?.map((bar) => {
            array.push([bar.date, bar.low, bar.open, bar.close, bar.high])
            averages.push([bar.date, bar.close > bar.open ? 
                                     bar.close / bar.open : bar.open / bar.close])
            comboArray.push([bar.date, bar.low, bar.open, bar.close, bar.high, ((bar.close+bar.open)/(2)), (bar.volume / 1000000)])
          })
        setPriceData(array)
        setPriceAvg(averages)
        setComboArray(comboArray)
    }, [props.prices])

    const loader = (
        <div className='w-full text-center'>
            <img 
                className="w-1/12 mx-auto"  
                src={require("../../assets/images/Tensai-logo-symbol-anim.gif")}  
            />
        </div>
    )

  return (
    <div className=''>
        <div id="chart-candlestick">
            <div className="mixed-chart">
            <Chart
                    chartType="ComboChart"
                    width="100%"
                    height="400px"
                    data={comboArray}
                    options={comboOptions}
                    loader={loader}
                />
            <Chart
                    chartType="CandlestickChart"
                    width="100%"
                    height="400px"
                    data={priceData}
                    options={chartOptions}
                    loader={loader}
                />
                <Chart 
                    chartType='LineChart'
                    data={priceAvg}
                    options={lineOptions}
                    loader={loader}
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