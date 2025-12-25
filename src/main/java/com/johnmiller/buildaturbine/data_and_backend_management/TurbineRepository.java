package com.johnmiller.buildaturbine.data_and_backend_management; 
import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.JpaRepository;


/* extending the interface JpaRepository allows for Spring boot to auto-generate
 the repository CRUD operations, which provides us with leeway to simply inject
 the repository into other classes */
@Repository
interface TurbineRepository extends JpaRepository<UserProfile, String>{
}


