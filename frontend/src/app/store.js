import { configureStore } from "@reduxjs/toolkit"

import { stocksApi } from "../services/stocksAPI"
import { cryptoApi } from "../services/cryptoAPI"
import { forexApi } from "../services/forexAPI"
import { strategyApi } from "../services/strategiesAPI"

export default configureStore({
    reducer: {
        [stocksApi.reducerPath]: stocksApi.reducer,
        [cryptoApi.reducerPath]: cryptoApi.reducer,
        [forexApi.reducerPath]: forexApi.reducer,
        [strategyApi.reducerPath]: strategyApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(stocksApi.middleware, cryptoApi.middleware, forexApi.middleware, strategyApi.middleware),
})