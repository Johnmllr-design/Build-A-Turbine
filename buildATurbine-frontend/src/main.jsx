import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import TurbineSidebar from './turbineSidebar.jsx'
import Fullscreen from './fullscreen.jsx'

createRoot(document.getElementById('root')).render(
  <h3>
    <Fullscreen/>
  </h3>
)
