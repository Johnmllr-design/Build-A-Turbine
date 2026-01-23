package com.johnmiller.buildaturbine.data_and_backend_management;
import java.util.ArrayList;
import java.util.List;

import org.springframework.data.mongodb.core.mapping.Document;

import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Id;

@Document
public class UserProfile{

    @Id
    private String userName;

    @Column
    private String password;

    @Column
    @ElementCollection
    private List<Turbine> userTurbines;

    public UserProfile(){
    }

    public UserProfile(String name, String password){
        this.userName = name;
        this.password = password;
        this.userTurbines = new ArrayList<Turbine>();
    }

    public void addATurbine(String turbineModel, String turbineDate){
        // make a new turbine object
        Turbine newTurbine = new Turbine(turbineModel, turbineDate);

        // add the object to the user's collection
        userTurbines.add(newTurbine);
    }

    public void setUserName(String name){
        this.userName = name;
    }

    public String getUserName(){
        return this.userName;
    }

    public String getPassword(){
        return this.password;
    }

    public void setUserTurb(List<Turbine> turbines){
        this.userTurbines = turbines;
    }

    public List<Turbine> getTurbs(){
        return this.userTurbines;
    }
}