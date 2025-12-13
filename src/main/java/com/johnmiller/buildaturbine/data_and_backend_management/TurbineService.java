package com.johnmiller.buildaturbine.data_and_backend_management;
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
import jakarta.validation.constraints.Null;


@Service
public class TurbineService {

    public TurbineRepository turbineRepository;
    public RestClient client;

    /* use a turbine repository inerface to make CRUD operations 
    in a springful way,making use of spring-boot's application 
    context container to manage an instance of Turbine repository for us
    */
    public TurbineService(TurbineRepository tbr){
        this.turbineRepository = tbr;
        this.client = RestClient.builder().baseUrl("https://energy.usgs.gov/api/uswtdb/v1/").build();
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
        try{
            // api response
            ArrayList<?> apiResponse = client.get()
            .uri("/turbines?&limit=1&offset=50")
            .retrieve()
            .body(ArrayList.class);

            // cast response to a map
            LinkedHashMap<String, String> lhm = (LinkedHashMap<String, String>) apiResponse.get(0);   // cast the object to a LinkedHashMap

            // make a new turbine object from the map object
            System.out.println(lhm.get("t_manu"));
            System.out.println(lhm);
            Object object = lhm.get("p_year");
            System.out.println(object);
            System.out.println(object.getClass());
            Turbine new_turb = new Turbine(lhm.get("t_manu"),  "eeifib");

            // save the new turbine to the database
            this.saveTurbineToDatabase(new_turb);
            return "Obtained a turbine with data " + new_turb.toString();

        // catch exception in event of failure to 
        }catch (Exception e){
            return "couldn't make is an object that you specified";
        }
    }

}
