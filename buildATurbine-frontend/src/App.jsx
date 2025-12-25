import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function CurrentTurbineCard() {
  const [count, setCount] = useState(50)

  return (
    <d>
      <div>Welcome to the homepage of BuildATurbine</div>
      <button onClick={() => {setCount(count => count + 1)}}>Increment me</button>
      <di2>the value of the value is {count}</di2>
    </d>
  )
}

export default CurrentTurbineCard