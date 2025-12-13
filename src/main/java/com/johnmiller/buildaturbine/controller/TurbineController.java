package com.johnmiller.buildaturbine.controller;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.johnmiller.buildaturbine.data_and_backend_management.Turbine;
import com.johnmiller.buildaturbine.data_and_backend_management.TurbineService;
import com.johnmiller.buildaturbine.data_and_backend_management.TurbineStatus;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import java.util.Optional;
import org.springframework.web.bind.annotation.RequestParam;





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

    @PostMapping("/post")
    public String postMethodName(@RequestBody Turbine turbine) {
        System.out.printf("the provided entity is %s with id of %d\n", turbine.getTurbineModel(), turbine.getId());
        turbineService.saveTurbineToDatabase(turbine);
        return " -- turbine obtained in the controller -- ";
    }

    @GetMapping("/demoCall")
    public String demo_api_call() {
        return turbineService.getATurbine();
    }
}
