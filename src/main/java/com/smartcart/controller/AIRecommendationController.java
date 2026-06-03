package com.smartcart.controller;

import com.smartcart.dto.AIRecommendationRequest;
import com.smartcart.dto.AIRecommendationResponse;
import com.smartcart.dto.ConversationalRequest;
import com.smartcart.service.AIRecommendationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = {"http://localhost:3000", "http://localhost:8080"})
public class AIRecommendationController {
    
    @Autowired
    private AIRecommendationService aiService;
    
    @PostMapping("/recommend")
    public ResponseEntity<AIRecommendationResponse> getRecommendation(
            @RequestBody AIRecommendationRequest request) {
        
        if (request.getQuestion() == null || request.getQuestion().trim().isEmpty()) {
            return ResponseEntity.badRequest().body(
                new AIRecommendationResponse("Please provide a question", null, null)
            );
        }
        
        AIRecommendationResponse response = aiService.getRecommendation(
            request.getQuestion(), 
            request.getSessionId()
        );
        
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/recommend/conversational")
    public ResponseEntity<AIRecommendationResponse> getConversationalRecommendation(
            @RequestBody ConversationalRequest request) {
        
        if (request.getQuestion() == null || request.getQuestion().trim().isEmpty()) {
            return ResponseEntity.badRequest().body(
                new AIRecommendationResponse("Please provide a question", null, null)
            );
        }
        
        AIRecommendationResponse response = aiService.getConversationalRecommendation(
            request.getQuestion(),
            request.getHistory(),
            request.getSessionId()
        );
        
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> checkHealth() {
        boolean isHealthy = aiService.checkAIServiceHealth();
        
        Map<String, Object> health = Map.of(
            "status", isHealthy ? "healthy" : "degraded",
            "ai_service", isHealthy ? "connected" : "disconnected",
            "timestamp", java.time.Instant.now().toString()
        );
        
        return ResponseEntity
            .status(isHealthy ? HttpStatus.OK : HttpStatus.SERVICE_UNAVAILABLE)
            .body(health);
    }
}