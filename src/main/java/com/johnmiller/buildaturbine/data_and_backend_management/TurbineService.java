package com.johnmiller.buildaturbine.data_and_backend_management;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import io.micrometer.common.lang.NonNull;
import jakarta.validation.Valid;

import java.util.Optional;



@Service
public class TurbineService {

    public TurbineRepository turbineRepository;
    private BCryptPasswordEncoder encoder;

    /* use a turbine repository inerface to make CRUD operations 
    in a springful way,making use of spring-boot's application 
    context container to manage an instance of Turbine repository for us
    */
    public TurbineService(TurbineRepository tbr){
        this.turbineRepository = tbr;
        this.encoder = new BCryptPasswordEncoder();
    }

    /* make a new user */
    public String makeNewUser(String username, String password){
        // make a user profile with an encoded password
        System.out.println("in service, making a new user");
        String encodedPassword = this.encoder.encode(password);
        UserProfile up = new UserProfile(username, encodedPassword);

        //save the user's profile to DB
        turbineRepository.save(up);

        // Return a successful message
        return "made a new user with username " + username;
    }

    public Boolean userExists(String username, String password){
        //find the user based on the username
        Optional<UserProfile> userProfile = turbineRepository.findById(username);

        //if not null, return if the username matches the known password
        if (!userProfile.isEmpty()){
            UserProfile profile = userProfile.get();
            return encoder.matches(password, profile.getPassword());
        // else, return false
        }else{
            System.out.println("the user does not exist so returning false");
            return false;
        }
    }

    /* add a turbine to the  users UserProfile turbine array */
    public String addTurbine(@NonNull String username, String turbineType, String turbineCreationDate) {
        try{
            UserProfile userProfile = turbineRepository.getReferenceById(username);
            userProfile.addATurbine(turbineType, turbineCreationDate);
            turbineRepository.save(userProfile);
            return "Added turbine to " + username + " of type " + turbineType;
        }catch (jakarta.persistence.EntityNotFoundException exception){
            return "couldn't find a corresponding user for the username";
        }
    } 
}
