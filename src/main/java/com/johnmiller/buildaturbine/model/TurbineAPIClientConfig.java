package com.johnmiller.buildaturbine.model;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;

@Configuration  // tell spring boot this class makes a bean
public class TurbineAPIClientConfig {
    

    /*  
    this is a bean, an instance of a function 
    to tell spring boot to save the produced restClient 
    object
    */ 
    @Bean   
    RestClient restClent(){

        /* use the factory pattern within RestClient to
         build the RestClient object with the provided base
         URL */
        return RestClient.builder().baseUrl("https://energy.usgs.gov/api/uswtdb/v1/").build();
        }
}
