package com.johnmiller.buildaturbine.data_and_backend_management;
import jakarta.validation.constraints.NotBlank;

public record CreateUserRequest(
    @NotBlank String username,
    @NotBlank String password
) {}
