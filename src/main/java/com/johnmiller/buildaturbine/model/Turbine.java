package com.johnmiller.buildaturbine.model;
import io.micrometer.common.lang.NonNull;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.validation.Valid;

@Entity
public class Turbine {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column
    private String model;

    // constructor for JPA and Jackson
    public Turbine() {}
    
    /* personal constructor for programmatic turbine creation */ 
    public Turbine(String typeOfTurbine){
        if (typeOfTurbine == null){
            throw new NullPointerException("the turbine cannot have a null class");
        }else{
        this.model = typeOfTurbine;
        }
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
