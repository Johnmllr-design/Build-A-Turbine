package com.johnmiller.buildaturbine.data_and_backend_management;

import jakarta.persistence.Embeddable;

@Embeddable
public class Turbine {
    
    private String model;
    private String date;

    /* no-arg constructor for spring */
    public Turbine(){
    }

    
    /* personal constructor for programmatic turbine creation */ 
    public Turbine(String typeOfTurbine, String date){
        if (typeOfTurbine == null){
            throw new NullPointerException("the turbine cannot have a null class");
        }else{
            this.model = typeOfTurbine;
            this.date = date;
        }
    }

    public String getTurbineModel(){
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    // Setters for JSON deserialization)
    public void setDate(String date) {
        this.date = date;
    }

    public String getDate() {
        return this.date;
    }
}
