package com.johnmiller.buildaturbine;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

import com.johnmiller.buildaturbine.data_and_backend_management.TurbineService;

@SpringBootApplication
public class driver_code {

	public static void main(String[] args) {
		ConfigurableApplicationContext context = SpringApplication.run(driver_code.class, args);
		String[] beans = context.getBeanDefinitionNames();
	}
}
