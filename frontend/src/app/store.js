import { configureStore } from "@reduxjs/toolkit"

import { stocksApi } from "../services/stocksAPI"

export default configureStore({
    reducer: {
        [stocksApi.reducerPath]: stocksApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(stocksApi.middleware),
})