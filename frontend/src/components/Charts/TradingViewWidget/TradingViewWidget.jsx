import React, { useEffect, useRef } from 'react'

let tvScriptLoadingPromise

export default function TradingViewWidget(props) {
  const onLoadScriptRef = useRef()

  useEffect(
    () => {
      onLoadScriptRef.current = createWidget;

      if (!tvScriptLoadingPromise) {
        tvScriptLoadingPromise = new Promise((resolve) => {
          const script = document.createElement('script')
          script.id = 'tradingview-widget-loading-script'
          script.src = 'https://s3.tradingview.com/tv.js'
          script.type = 'text/javascript'
          script.onload = resolve

          document.head.appendChild(script)
        })
      }

      tvScriptLoadingPromise.then(() => onLoadScriptRef.current && onLoadScriptRef.current())

      return () => onLoadScriptRef.current = null

      function createWidget() {
        if (document.getElementById('tradingview_widget') && 'TradingView' in window) {
          new window.TradingView.widget({
            autosize: true,
            symbol: `${props.exchange}:${props.symbol}`,
            interval: "D",
            timezone: "America/New_York",
            theme: "dark",
            style: "1",
            locale: "en",
            toolbar_bg: "#f1f3f6",
            enable_publishing: false,
            withdateranges: true,
            hide_side_toolbar: false,
            allow_symbol_change: false,
            container_id: "tradingview_widget"
          })
        }
      }
    },
    []
  );

  return (
    <div className='tradingview-widget-container'>
      <div id='tradingview_widget' className='h-[500px]'/>
      {/* <div className="tradingview-widget-copyright">
        <a href={`https://www.tradingview.com/symbols/${props.exchange}-${props.symbol}/`} rel="noopener" target="_blank"><span className="blue-text">{props.symbol} Trading View Chart</span></a>
      </div> */}
    </div>
  );
}