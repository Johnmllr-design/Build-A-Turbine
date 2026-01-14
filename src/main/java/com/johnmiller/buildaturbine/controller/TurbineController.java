package com.johnmiller.buildaturbine.controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.net.URI;
import java.net.http.*;

import com.johnmiller.buildaturbine.data_and_backend_management.TurbineService;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;




@RequestMapping("")
@CrossOrigin(origins="http://localhost:5173")
@RestController
public class TurbineController {
    
    /* service class: interface frontend with backend management logic */
    public TurbineService turbineService;

    /* Inject the service class into the contructor */
    public TurbineController(TurbineService service){
        this.turbineService = service;
    }

    /* Welcome string*/
    @GetMapping("/dummy")
    public String dummy() {
        return  "You called the java backend";
    }


    /* Welcome string*/
    @GetMapping("/getUser/{username}")
    public String getUser(@PathVariable String username) {
        if (username.length() == 0){
            return "Username cannot be null";
        }
        String currentProfile = turbineService.getUser(username);
        return currentProfile;
    }


    @GetMapping("/makenewuser/{username}")
    public String makeNewUser(@PathVariable String username) {
        if (username.length() == 0){
            return "Username cannot be null";
        }
        return turbineService.makeNewUser(username);
    }

    @GetMapping("/addturbine/{username}/{type}/{date}")
    public String addTurbine(@PathVariable String username, @PathVariable String type, @PathVariable String date) {
        if (username.length() == 0 || type.length() == 0 || date.length() == 0){
            return "Username and tyrbine information cannot be null";
        }
        String response = turbineService.addTurbine(username, type, date);;
        System.out.println(response);
        return response;
    }
}
