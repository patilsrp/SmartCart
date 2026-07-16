package com.smartcart.controller;

import com.smartcart.dto.*;
import com.smartcart.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@CrossOrigin(origins = {"http://localhost:3000", "http://localhost:8080"})
public class AuthController {
    
    private final AuthService authService;
    
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest loginRequest) {
        AuthResponse response = authService.login(loginRequest);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@Valid @RequestBody RegisterRequest registerRequest) {
        AuthResponse response = authService.register(registerRequest);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    @GetMapping("/me")
    public ResponseEntity<UserDTO> getCurrentUser() {
        UserDTO user = authService.getCurrentUser();
        return ResponseEntity.ok(user);
    }
    
    @PutMapping("/profile")
    public ResponseEntity<UserDTO> updateProfile(@Valid @RequestBody UserDTO userDTO) {
        UserDTO updatedUser = authService.updateProfile(userDTO);
        return ResponseEntity.ok(updatedUser);
    }
    
    @PostMapping("/change-password")
    public ResponseEntity<MessageResponse> changePassword(@Valid @RequestBody ChangePasswordRequest request) {
        authService.changePassword(request.getOldPassword(), request.getNewPassword());
        return ResponseEntity.ok(new MessageResponse("Password changed successfully"));
    }
}