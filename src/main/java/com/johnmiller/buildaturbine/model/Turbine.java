package com.johnmiller.buildaturbine.model;

import org.hibernate.validator.internal.engine.groups.Sequence;

import io.micrometer.common.lang.NonNull;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Turbine {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column
    @NonNull
    private String model;

    // constructor for JPA and Jackson
    public Turbine() {}
    
    /* personal constructor for programmatic turbine creation */ 
    public Turbine(String typeOfTurbine){
        this.model = typeOfTurbine;
    }

    // Getters
    public Integer getId(){
        return id;
    }

    public String getTurbineModel(){
        return model;
    }

    // Setters for JSON deserialization)
    public void setId(Integer id) {
        this.id = id;
    }

    public void setModel(String model) {
        this.model = model;
    }

}
