import { lazy, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Select from "react-select"
import './App.css'
import select from 'select'
import input from 'react'
import { Input } from 'react-select/animated'
import './App.css'


function TurbineCard(props) {
  const turbine = props.turb;
  const [pred, setPred] = useState('?')


  async function getModelPrediction(){
    const apiString = "http://localhost:8080/makeprediction";
    const result = await fetch(apiString);
    console.log(result);
    const textResults = await result.text();
    return textResults;
  }

  return (
    <div className='elegant-card'>
      {turbine.type} at {Math.floor(turbine.lat)}, {Math.floor(turbine.long)}
      <button className='btn' onClick={() => {setPred(getModelPrediction())}}>Get an AI value estimate!</button>
      <button className='div' > {pred} </button>
    </div>
  )
}
export default TurbineCard

