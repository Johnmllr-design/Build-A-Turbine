package com.johnmiller.buildaturbine;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.johnmiller.buildaturbine.controller.TurbineController;

@SpringBootTest
class BuildaturbineApplicationTests {

	// inject the controller to begin testing the backend API
	@Autowired
	private TurbineController controller;

	@Test
	void controllerRunningTest(){
		assertNotNull(controller);
	}


	/* Successful cases tests */
	@Test
	void makeUser(){
		assertEquals(controller.makeNewUser("John"), "made a new user with username John", "the username works");
	}

	/* Unsuccessful cases tests */
	@Test
	void getWrongUser(){
		assertEquals(controller.getUser("Jake"), "username doesn't correspond to any existing users");
	}

	@Test
	void makeEmptuUser(){
		assertEquals(controller.makeNewUser(""),"Username cannot be null");
	}
}
