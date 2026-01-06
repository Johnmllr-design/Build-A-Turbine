import {useState} from 'react'
import TurbineCard from './turbineCard'
import TurbineSidebar from './turbineSidebar'
import React from 'react'

import {
    APIProvider,
    Map,
    Pin,
    InfoWindow,
    AdvancedMarker
}from '@vis.gl/react-google-maps'


function Fullscreen() {

    const centerPos = {lat : 40, lng : 265};
    const [turbines, setTurbine] = useState([]);

    

    return(
        <div style={{display : 'flex', borderWidth :'10px'}}>
            {/*turbine sidebar component*/}
            <TurbineSidebar newTurbines={turbines}/>

            {/*Map component*/}
            <APIProvider apiKey='AIzaSyBTgKunKe6FIf4zdhWSjZh1oZZ76lhEG9I'>
                <div style={{height : "590px", width : "1390px", borderStyle : 'solid', borderWidth : "10px", borderColor: "grey"}}>
                    <Map id="map" colorScheme:black mapId="8a273d3da3a319bb876b5293" center={centerPos} zoom={4.3} 
                    onClick={(e) => {
                    document.getElementById("long").textContent = e.detail.latLng.lng 
                    document.getElementById("lat").textContent = e.detail.latLng.lat
                    document.getElementById("type").placeholder = "provide the type of turbine you want"
                    }}>
                    {
                    turbines.map((turb, i) => {return(
                     <AdvancedMarker key={i} position={{lat : Number(turb.lat), lng :  Number(turb.long)}}>
                        <Pin background = "pink" glyphColor="pink" borderColor="black"/>
                    </AdvancedMarker>)})
                    }
                    </Map>
                </div>
            </APIProvider>

            {/*new turbine component*/}
            <div className="div">
                <textarea placeholder='provide turbine type' id="type"></textarea><br/>
                <textarea placeholder='provide turbine longitude' id="long"></textarea><br/>
                <textarea placeholder='provide turbine latitude' id="lat"></textarea><br/>
                <button className="btn" onClick={() => {

                    /* set the new user's turbines for the sidebar */
                    setTurbine(turbines => [...turbines, {
                    type: document.getElementById("type").value, 
                    long: document.getElementById("long").value, 
                    lat:document.getElementById("lat").value
                    }])                    
                    }}>add turbine location</button>
            </div>
        </div>
    )
}

export default Fullscreen
