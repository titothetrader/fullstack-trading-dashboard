import { useState, useEffect } from 'react'
import millify from 'millify'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js'
  import { Bar } from 'react-chartjs-2'
  import { faker } from '@faker-js/faker';

  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );

const StockBarChart = (props) => {
    // console.log(props.prices)
    const [mavPrice, setMaxPrice] = useState()
    const [minPrice, setMinPrice] = useState()
    const [chartLabels, setChartLabels] = useState()
    const [chartData, setChartData] = useState()
    
    const prepData =() => {
        props.prices?.map((bar) => {
            console.log(bar)
        })
    }

    prepData()

    const options = {
        type: 'bar',
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: `Price Chart for ${props.prices?.[0]?.symbol}`,
                },
            },
            scales: {
                x: {
                    grid: {
                        offset: true,                    
                    }
                },
                xAxes: [
                {
                    id: "bar-x-axis1",
                    stacked: true,
                    categoryPercentage: 0.5,
                    barPercentage: 0.5
                },
                {
                    id: "bar-x-axis2",
                    stacked: true,
                    categoryPercentage: 0.5,
                    barPercentage: 0.5
                }
            ],
                yAxes: [{
                    id: "bar-y-axis1",
                    stacked: false,
                    ticks:{
                        beginAtZero:true,
                        suggestedMax:50,
                        suggestedMin:1,
                        beginAtZero:true,
                        autoSkip:true,
                    }
                }]
            }
        },
    };
    
    //   const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
      const labels = props.prices?.map((bar) => bar.date)
    
      const data = {
        labels,
        grouped: false,
        datasets: [
          {
            label: 'Dataset 1',
            xAxisID: "bar-x-axis1",
            // barPercentage: 0.5,
            barThickness: 6,
            maxBarThickness: 8,
            // minBarLength: 2,
            data: props.prices?.map((bar) => {return [bar.open, bar.close]}),
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
          },
          {
            label: 'Dataset 1',
            xAxisID: "bar-x-axis2",
            // barPercentage: 0.5,
            barThickness: 1,
            maxBarThickness: 1,
            // minBarLength: 2,
            data: props.prices?.map((bar) => {return [bar.high, bar.low]}),
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
          },
        ],
      };

  return (
    <div className=''>
        <div id="chart-candlestick">
            <div className="mixed-chart">
                <Bar options={options} data={data} />
          </div>
        </div>
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
  )
}

export default StockBarChart