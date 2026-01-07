import { lazy, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Select from "react-select"
import './App.css'
import select from 'select'
import input from 'react'
import { Input } from 'react-select/animated'


function TurbineCard(props) {

  const turbine = props.turb;

  console.log(turbine);

  return (
    <div>
      Turbine: {turbine.type} in location {turbine.long}, {turbine.lat}
    </div>
  )
}
export default TurbineCard



/* <Select 
        options={options}
        placeholder="Select your wind turbine model..."
        styles={customStyles}
        isSearchable={false}
        isClearable={true}
        value={options.find(o => o.value == turbine)}
        onChange={(op) => {setTurbine(op.value)}}
      /> */
