import {useState} from 'react'
import TurbineCard from './turbineCard'
import React from 'react'
import { Input } from 'react-select/animated';


function TurbineSidebar(props) {

    const current_turbines = props.newTurbines;
    console.log(current_turbines);

    return (
        <div className='scrolldiv-2'>
            {current_turbines.map((turbine, i) => {
                return <TurbineCard key={i} turb={turbine}/>
            })}
        </div>
    )
}
export default TurbineSidebar