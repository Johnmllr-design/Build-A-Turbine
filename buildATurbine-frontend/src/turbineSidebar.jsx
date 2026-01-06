import {useState} from 'react'
import TurbineCard from './turbineCard'
import React from 'react'
import { Input } from 'react-select/animated';


function TurbineSidebar(props) {

    const current_turbines = props.newTurbines;
    console.log(current_turbines);

    return (
        <div>
            {current_turbines.map((turbine, i) => {
                return <TurbineCard key={i} turb={turbine}/>
            })}
        </div>
    )
}
export default TurbineSidebar