package com.johnmiller.buildaturbine.data_and_backend_management; 
import org.springframework.stereotype.Repository;
import org.springframework.data.mongodb.repository.MongoRepository;


/* extending the interface JpaRepository allows for Spring boot to auto-generate
 the repository CRUD operations, which provides us with leeway to simply inject
 the repository into other classes */
@Repository
public interface UserProfileRepository extends MongoRepository<UserProfile, String>{
}



