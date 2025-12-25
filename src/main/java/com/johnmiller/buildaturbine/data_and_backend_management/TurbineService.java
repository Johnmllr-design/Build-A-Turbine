package com.johnmiller.buildaturbine.data_and_backend_management;
import org.springframework.stereotype.Service;

import java.util.Optional;



@Service
public class TurbineService {

    public TurbineRepository turbineRepository;

    /* use a turbine repository inerface to make CcRUD operations 
    in a springful way,making use of spring-boot's application 
    context container to manage an instance of Turbine repository for us
    */
    public TurbineService(TurbineRepository tbr){
        this.turbineRepository = tbr;
    }

    public String makeNewUser(String username){
        // make a user profile
        UserProfile up = new UserProfile(username);

        //save the user's profile to DB
        Object ob = turbineRepository.save(up);

        // Return a successful message
        return "made a new user with username " + username;
    }

    /* add a turbine to the  users UserProfile turbine array */
    public String addTurbine(String username, String turbineType, String turbineCreationDate) {
        try{
            UserProfile userProfile = turbineRepository.getReferenceById(username);
            userProfile.addATurbine(turbineType, turbineCreationDate);
            turbineRepository.save(userProfile);
            return "Added turbine to " + username + " of type " + turbineType;
        }catch (jakarta.persistence.EntityNotFoundException exception){
            return "couldn't find a corresponding user for the username";
        }
    }

    public String getUser(String username){
        //find the user based on the username
        Optional<UserProfile> userProfile = turbineRepository.findById(username);

        //if not null, turn the data object to a string
        if (!userProfile.isEmpty()){
            String ret = "The user has the following information: \nUsername:";
            UserProfile profile = userProfile.get();
            ret = ret + " " + profile.getUserName() + " \n and turbines:";
            for (Turbine t : profile.getTurbs()){
                ret = ret + " " + t.getTurbineModel();
            }
            return ret;

        // else, throw an error and return 
        }else{
            return "username doesn't correspond to any existing users";
        }
    }
      
}
