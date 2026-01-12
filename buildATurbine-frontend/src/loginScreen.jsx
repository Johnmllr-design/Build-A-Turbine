import {useState} from 'react'
import TurbineCard from './turbineCard'
import TurbineSidebar from './turbineSidebar'
import React from 'react'
import Fullscreen from './fullscreen'
import './App.css'

function LoginScreen() {
    const [loggedIn, setLogin] = useState(false);
    
    function login(username, password, p2){
        if (username.length > 5 && password.length >= 8 && password == p2){
            setLogin(true);
        }
    }

    if (!loggedIn){
        return (
        <div>
            <div>
                <input className='div' id="uname" placeholder='username'/>
                <input className='div' id="pw" placeholder='password'/>
                <input className='div' id="pw2" placeholder='retype password'/><br/>
            </div>
            <button className='btn' onClick={() => {login(document.getElementById("uname").value, document.getElementById("pw").value, document.getElementById("pw2").value)}}>Log in</button>
        </div>
        )
    } else {
        /* when the login is successful, provide the main functionality */
        /* make a new user account on login */
        async function login(username){
            try{
            const apiString = "http://localhost:8080/makenewuser/" + username;
            const response = await fetch(apiString);
            const result = await response.text();
            console.log(result);
            }catch(error){
                console.log(error);
            }
        }
        login(document.getElementById('uname').value);

        return (
            <Fullscreen username={document.getElementById('uname').value}/>
        )
    }
}
export default LoginScreen