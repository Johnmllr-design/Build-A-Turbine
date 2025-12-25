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
        UserProfile up = new UserProfile(username);
        Object ob = turbineRepository.save(up);
        System.out.println(ob.getClass());
        return "made a new user with username " + username;
    }

    /* add a turbine to the  users UserProfile turbine array */
    public String addTurbine(String username, String turbineType, String turbineCreationDate) {
        try{
            UserProfile userProfile = turbineRepository.getReferenceById(username);
            System.out.printf("in addTurbine: Got the user profile %s\n", userProfile.getUserName());
            userProfile.addATurbine(turbineType, turbineCreationDate);
            System.out.printf("%s now has turbines %s\n", userProfile.getUserName(), userProfile.getTurbs().toString());
            turbineRepository.save(userProfile);
            return "Added turbine to " + username + " of type " + turbineType;
        }catch (jakarta.persistence.EntityNotFoundException exception){
            System.out.printf("couldn't find a corresponding user for the username\n");
            return "couldn't find a corresponding user for the username";
        }
    }

    public String getUser(String username){
        Optional<UserProfile> userProfile = turbineRepository.findById(username);
        if (!userProfile.isEmpty()){
            String ret = "The user has the following information: \nUsername:";
            UserProfile profile = userProfile.get();
            ret = ret + " " + profile.getUserName() + " \n and turbines:";
            for (Turbine t : profile.getTurbs()){
                ret = ret + " " + t.getTurbineModel();
            }
            return ret;
        }else{
            return "username doesn't correspond to any existing users";
        }
    }
      
}
