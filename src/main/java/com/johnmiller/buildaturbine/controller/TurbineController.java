package com.johnmiller.buildaturbine.controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.johnmiller.buildaturbine.data_and_backend_management.TurbineService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;




@RequestMapping("")
@RestController
public class TurbineController {
    
    /* service class: interface frontend with backend management logic */
    public TurbineService turbineService;

    /* Inject the service class into the contructor */
    public TurbineController(TurbineService service){
        this.turbineService = service;
    }

    /* Welcome string*/

    @GetMapping("/showuser/{username}")
    public String showUsername(@PathVariable String username) {
        String currentProfile = turbineService.getUser(username);
        return currentProfile;
    }

    @GetMapping("/demoCall")
    public String demo_api_call() {
        return turbineService.makeNewUser("John Miller");
    }

    @GetMapping("/makenewuser/{username}")
    public String makeNewUser(@PathVariable String username) {
        return turbineService.makeNewUser(username);
    }

    @GetMapping("/addturbine/{username}/{type}/{date}")
    public String addTurbine(@PathVariable String username, @PathVariable String type, @PathVariable String date) {

        System.out.printf("adding a %s to %s's profile\n", type, username);
        return turbineService.addTurbine(username, type, date);
    }
}
