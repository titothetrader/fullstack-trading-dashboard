import { configureStore } from "@reduxjs/toolkit"

import { stocksApi } from "../services/stocksAPI"
import { cryptoApi } from "../services/cryptoAPI"

export default configureStore({
    reducer: {
        [stocksApi.reducerPath]: stocksApi.reducer,
        [cryptoApi.reducerPath]: cryptoApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(stocksApi.middleware, cryptoApi.middleware),
})