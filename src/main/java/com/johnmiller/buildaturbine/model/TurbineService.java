package com.johnmiller.buildaturbine.model;
import org.springframework.stereotype.Service;
import java.util.Objects;
import io.micrometer.common.lang.NonNull;
import jakarta.validation.Valid;

@Service
public class TurbineService {

    public TurbineRepository turbineRepository;

    /* use a turbine repository inerface to make CRUD operations in a abstract way,
    making use of spring-boot's application context container to manage an instance 
    of Turbine repository for us*/
    public TurbineService(TurbineRepository tbr){
        this.turbineRepository = tbr;
    }

    /* Provide a compile time @NonNull annotation and a dynamic Objects chech for 
    both compile time and runtime */
    public void saveTurbineToDatabase(@NonNull Turbine turbine) {
        System.out.println("in the turbineService call to save the new turbine to the repository");
        Objects.requireNonNull(turbine, "The turbine object must be non-null for database calls");
        turbineRepository.save(turbine);
    }
}
