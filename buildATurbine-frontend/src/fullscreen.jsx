import {useEffect, useState} from 'react'
import TurbineCard from './turbineCard'
import TurbineSidebar from './turbineSidebar'
import React from 'react'
import Select from 'react-select/base'
import './App.css'
import ScrollBar from './scrollBar'

import {
    APIProvider,
    Map,
    Pin,
    InfoWindow,
    AdvancedMarker
}from '@vis.gl/react-google-maps'


function Fullscreen(props) {

    const [centerPos, setPos] = useState({lat : 40, lng : 265})
    const [dz, setZoom] = useState(4.6)
    const [turbines, setTurbine] = useState([]);
    const [selectedTurbine, setSelected] = useState("select a type above");
    const [mapClicked, setClick] = useState(false);
    const username = props.username;
  

    /* add a turbine to the backend */
    async function addTurbine(username, type, date) {
        try {
        const backendApiString = "http://localhost:8080/addturbine/" + username + "/" + type + "/" + date;
        const response = await fetch(backendApiString);
        const result = await response.text();
        } catch (error) {
            console.log(error);
        }
    }

    /* function to ensure a turbine has been properly selected before adding to user queue */
    function selected(){
        return (selectedTurbine !== "select a type above" && mapClicked);
    }



    return(
        <div className='container'>
            {/*turbine sidebar component*/}
            <TurbineSidebar turbines={turbines} setTurbines={setTurbine}/>
            {/*api provider component*/}
            <APIProvider apiKey='AIzaSyBTgKunKe6FIf4zdhWSjZh1oZZ76lhEG9I'>
                <div style={{height : "590px", width : "1290px", borderStyle : 'solid', 
                            borderWidth : "10px", borderColor: 'white', touchAction : 'none', 
                            borderRadius: "20px", boxShadow: "5px 5px 10px grey"}}>
                    
                    {/*Map component*/}
                    <Map 
                    style={{ height: "100%", width: "100%" }}
                    id="map" 
                    mapId="8a273d3da3a319bb876b5293" 
                    defaultCenter={centerPos}
                    defaultZoom={dz}
                    gestureHandling={true}
                    colorScheme='DARK'
                    disableDefaultUI={true}
                    onClick={(e) => {
                    setClick(true);
                    document.getElementById("long").value = e.detail.latLng.lng 
                    document.getElementById("lat").value = e.detail.latLng.lat}}
                    >

                        {
                        turbines.map((turb, i) => 
                            {return(
                                <AdvancedMarker key={i} position={{lat : Number(turb.lat), lng :  Number(turb.long)}}>
                                    <Pin background = "pink" glyphColor="pink" borderColor="black" scale={0.5} />
                                </AdvancedMarker>)
                            })
                        }
                    </Map>
                </div>
            </APIProvider>

            {/*new turbine component*/}
            <div className= 'regular_card'>
                <ScrollBar selectedTurbine={selectedTurbine} setSelected={setSelected}/>
                <div className='div3' id="type">{selectedTurbine}</div>
                <input className='input' id="long" placeholder='click map for longitude'/>
                <input className='input' id="lat" placeholder='click map forlatitude'/><br/>
                <button className="btn" onClick={() => {
                            if(selected()){
                                /* set the new user's turbines for the sidebar */
                                setTurbine(turbines => [...turbines, {
                                type: selectedTurbine, 
                                long: document.getElementById("long").value, 
                                lat:document.getElementById("lat").value,
                                valid:true
                                }])  
                                
                                /* make a call to the backend to store this turbine in the database*/
                                const date = new Date();
                                const officialDate = "" + date.getMonth().toString() + "-" + date.getDate().toString() + "-" + date.getFullYear().toString();
                                console.log(officialDate);

                                addTurbine(username, selectedTurbine, officialDate);
                        }
                    }}>add turbine location</button>
            </div>
        </div>
    )
}

export default Fullscreen
