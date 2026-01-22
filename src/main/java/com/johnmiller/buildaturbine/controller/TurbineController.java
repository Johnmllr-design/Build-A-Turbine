package com.johnmiller.buildaturbine.controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.johnmiller.buildaturbine.data_and_backend_management.CreateUserRequest;
import com.johnmiller.buildaturbine.data_and_backend_management.TurbineService;


import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;




@RequestMapping("")
@CrossOrigin(origins="https://build-a-turbine-frontend-v-git-4be107-johnmllr-designs-projects.vercel.app/")
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
        return turbineService.userExists(username, password);
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
