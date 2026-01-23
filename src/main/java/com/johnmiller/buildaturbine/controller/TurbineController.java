package com.johnmiller.buildaturbine.controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.johnmiller.buildaturbine.data_and_backend_management.CreateNewTurbine;
import com.johnmiller.buildaturbine.data_and_backend_management.CreateUserRequest;
import com.johnmiller.buildaturbine.data_and_backend_management.TurbineService;


import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;




@RequestMapping("https://determined-luck-production-4525.up.railway.app")
@CrossOrigin(origins="https://build-a-turbine-frontend-v287.vercel.app")
@RestController
public class TurbineController {
    
    /* service class: interface frontend with backend management logic */
    public TurbineService turbineService;

    /* Inject the service class into the contructor */
    public TurbineController(TurbineService service){
        this.turbineService = service;
    }


    /* make new users */
    @PostMapping("/makenewuser")
    public Boolean makeNewUser(@RequestBody CreateUserRequest body) {
        String username = body.username();
        String password = body.password();
        System.out.printf("in controller the result of already existing is %s\n", turbineService.userExists(username, password));
        if(!turbineService.userExists(username, password)){
            turbineService.makeNewUser(username, password);
            return true;
        }
        return false;
    }

    /* log in a existing user */
    @PostMapping("/loginuser")
    public Boolean loginUser(@RequestBody CreateUserRequest body) {
        String username = body.username();
        String password = body.password();
        return turbineService.validLogin(username, password);
    }

    @PostMapping("/addturbine")
    public String addTurbine(@RequestBody CreateNewTurbine newTurbine) {
        String username = newTurbine.username();
        String type = newTurbine.type();
        String date = newTurbine.date();

        if (username.length() == 0 || type.length() == 0 || date.length() == 0){
            return "Username and tyrbine information cannot be null";
        }
        String response = turbineService.addTurbine(username, type, date);;
        System.out.println(response);
        return response;
    }
}
