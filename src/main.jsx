import React from 'react'
import ReactDOM from 'react-dom/client'
import { TonConnectUIProvider } from '@tonconnect/ui-react'
import App from './App'
import Admin from './Admin'
import './index.css'

const manifestUrl = window.location.origin + '/tonconnect-manifest.json'

// Простой роутинг на основе pathname
const isAdminPage = window.location.pathname === '/admin'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <TonConnectUIProvider manifestUrl={manifestUrl}>
      {isAdminPage ? <Admin /> : <App />}
    </TonConnectUIProvider>
  </React.StrictMode>
)
