package com.johnmiller.buildaturbine.data_and_backend_management;
import jakarta.validation.constraints.NotBlank;

public record CreateNewTurbine(
    @NotBlank String username,
    @NotBlank String type,
    @NotBlank String date
) {}
