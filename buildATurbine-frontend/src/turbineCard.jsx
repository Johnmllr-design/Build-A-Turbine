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

    // string to query the pytorch model
    const apiString = "http://127.0.0.1:8000/prediction";

    // make a get request
    const result = await fetch(apiString, { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: turbine.type, longitude : turbine.long, latitude : turbine.lat})});

    const json = await result.json();
    console.log(json.returnedVal);

    // get the results as a string
    const textResults = (await json.returnedVal);
    return textResults;
  }

  return (
    <div className='div2'>
      {turbine.type} at {Math.floor(turbine.lat)}, {Math.floor(turbine.long)}
      <button className='btn' onClick={() => {setPred(getModelPrediction())}}>Get an AI value estimate!</button>
      <div className='div3' > {pred} </div>
    </div>
  )
}
export default TurbineCard

