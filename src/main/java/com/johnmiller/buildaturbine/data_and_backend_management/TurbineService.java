package com.johnmiller.buildaturbine.data_and_backend_management;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import io.micrometer.common.lang.NonNull;
import java.util.Optional;



@Service
public class TurbineService {

    public UserProfileRepository repository;
    private BCryptPasswordEncoder encoder;

    /* use a turbine repository inerface to make CRUD operations 
    in a springful way,making use of spring-boot's application 
    context container to manage an instance of Turbine repository for us
    */
    public TurbineService(UserProfileRepository tbr){
        this.repository = tbr;
        this.encoder = new BCryptPasswordEncoder();
    }

    /* make a new user */
    public String makeNewUser(String username, String password){
        // make a user profile with an encoded password
        System.out.println("in service, making a new user");
        String encodedPassword = this.encoder.encode(password);
        UserProfile up = new UserProfile(username, encodedPassword);

        //save the user's profile to DB
        repository.save(up);

        // Return a successful message
        return "made a new user with username " + username;
    }

    public Boolean userExists(String username, String password){
        //find the user based on the username
        if (username != null){
            return repository.existsById(username);
        }else{
            return false;
        }
    }

    public Boolean validLogin(String username, String password){
        //find the user based on the username
        if (username != null){
            if (repository.existsById(username)){
                Optional<UserProfile> user = repository.findById(username);
                UserProfile profile = user.get();
                return encoder.matches(password, profile.getPassword());
            }
            else{
                return false;
            }
        } else{
            return false;
        }
    }

    /* add a turbine to the  users UserProfile turbine array */
    public String addTurbine(@NonNull String username, String turbineType, String turbineCreationDate) {
        if (username != null){
            Optional<UserProfile> userProfile = repository.findById(username);
                if (userProfile.isPresent()){
                    UserProfile profile = userProfile.get();
                    profile.addATurbine(turbineType, turbineCreationDate);
                    repository.save(profile);
                    return "Added turbine to " + username + " of type " + turbineType;
                }else{
                    return "user profile not fould";
            }
        } else {
        return "user profile not fould";
        }
    }
}

