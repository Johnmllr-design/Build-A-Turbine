package com.johnmiller.buildaturbine.data_and_backend_management;
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

    @Column
    private String date;

    // constructor for JPA and Jackson
    public Turbine() {}
    
    /* personal constructor for programmatic turbine creation */ 
    public Turbine(String typeOfTurbine, String date){
        if (typeOfTurbine == null){
            throw new NullPointerException("the turbine cannot have a null class");
        }else{
            this.model = typeOfTurbine;
            this.date = date;
        }
    }

    public Integer getId(){
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
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
