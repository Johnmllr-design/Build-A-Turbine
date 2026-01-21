import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import TurbineSidebar from './turbineSidebar.jsx'
import Fullscreen from './fullscreen.jsx'
import App from './welcomescreen.jsx'

createRoot(document.getElementById('root')).render(
  <div> 
    <App/>
  </div>
)
