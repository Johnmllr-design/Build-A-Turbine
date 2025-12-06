package com.johnmiller.buildaturbine.model;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestTemplate;
import com.fasterxml.jackson.databind.util.JSONPObject;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Objects;
import java.util.Set;

import io.micrometer.common.lang.NonNull;


@Service
public class TurbineService {

    public TurbineRepository turbineRepository;
    public RestClient client;

    /* use a turbine repository inerface to make CRUD operations 
    in a springful way,making use of spring-boot's application 
    context container to manage an instance of Turbine repository for us
    */
    public TurbineService(TurbineRepository tbr, RestClient restClient){
        this.turbineRepository = tbr;
        this.client = restClient;
    }

    /* saveTurbineToDatabase : send a turbine object
     to be mapped to the database

    @Param turbine: A turbine object, throws a
    null pointer exception on turbine nullness

    @Output void: return nothing, void

    Provide a compile time @NonNull annotation and a dynamic Objects chech for 
    both compile time and runtime */
    public void saveTurbineToDatabase(@NonNull Turbine turbine) throws NullPointerException{
        System.out.println("in the turbineService call to save the new turbine to the repository");
        Objects.requireNonNull(turbine, "The turbine object must be non-null for database calls");
        turbineRepository.save(turbine);
    }

    /* getTurbibe is a demo API call to the turbine repository */
    public String getATurbine(){

       
        // api response
        try{
            ArrayList<?> apiResponse = client.get()
            .uri("/turbines?&limit=1")
            .retrieve()
            .body(ArrayList.class);
            LinkedHashMap<String, String> lhm = (LinkedHashMap<String, String>)apiResponse.get(0);   // cast the object to a LinkedHashMap
            System.out.println(lhm.get("t_manu"));
            Turbine new_turb = new Turbine(lhm.get("t_manu"));
            this.saveTurbineToDatabase(new_turb);
        }catch (Error e){
            return "couldn't make is an object that you specified";
        }


        return "made an API call";
    }

}
