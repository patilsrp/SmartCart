package com.smartcart.service;

import com.smartcart.dto.AIRecommendationRequest;
import com.smartcart.dto.AIRecommendationResponse;
import com.smartcart.dto.ConversationalRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.UUID;

@Service
public class AIRecommendationService {
    
    private static final Logger logger = LoggerFactory.getLogger(AIRecommendationService.class);
    
    @Value("${ai.service.url:http://localhost:8001}")
    private String aiServiceUrl;
    
    private final RestTemplate restTemplate;
    
    public AIRecommendationService() {
        this.restTemplate = new RestTemplate();
    }
    
    public AIRecommendationResponse getRecommendation(String question, String sessionId) {
        try {
            String url = aiServiceUrl + "/recommend";
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("question", question);
            
            if (sessionId == null || sessionId.isEmpty()) {
                sessionId = UUID.randomUUID().toString();
            }
            requestBody.put("session_id", sessionId);
            
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestBody, headers);
            
            logger.info("Calling AI service for recommendation: {}", question);
            
            AIRecommendationResponse response = restTemplate.postForObject(
                url,
                request,
                AIRecommendationResponse.class
            );
            
            if (response != null) {
                response.setSessionId(sessionId);
            }
            
            return response;
            
        } catch (HttpClientErrorException e) {
            logger.error("Client error calling AI service: {}", e.getMessage());
            return createErrorResponse("Unable to process your request. Please try again.", sessionId);
        } catch (ResourceAccessException e) {
            logger.error("Cannot reach AI service: {}", e.getMessage());
            return createErrorResponse("AI service is temporarily unavailable. Please try again later.", sessionId);
        } catch (Exception e) {
            logger.error("Unexpected error calling AI service: {}", e.getMessage(), e);
            return createErrorResponse("An error occurred while getting recommendations.", sessionId);
        }
    }
    
    public AIRecommendationResponse getConversationalRecommendation(
            String question, 
            List<Map<String, String>> history, 
            String sessionId) {
        
        try {
            String url = aiServiceUrl + "/recommend/conversational";
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            ConversationalRequest requestBody = new ConversationalRequest();
            requestBody.setQuestion(question);
            requestBody.setHistory(history != null ? history : List.of());
            
            if (sessionId == null || sessionId.isEmpty()) {
                sessionId = UUID.randomUUID().toString();
            }
            requestBody.setSessionId(sessionId);
            
            HttpEntity<ConversationalRequest> request = new HttpEntity<>(requestBody, headers);
            
            logger.info("Calling AI service for conversational recommendation: {}", question);
            
            AIRecommendationResponse response = restTemplate.postForObject(
                url,
                request,
                AIRecommendationResponse.class
            );
            
            if (response != null) {
                response.setSessionId(sessionId);
            }
            
            return response;
            
        } catch (Exception e) {
            logger.error("Error calling conversational AI service: {}", e.getMessage(), e);
            return createErrorResponse("Unable to process conversational request.", sessionId);
        }
    }
    
    public boolean checkAIServiceHealth() {
        try {
            String url = aiServiceUrl + "/health";
            Map<String, Object> health = restTemplate.getForObject(url, Map.class);
            return health != null && "healthy".equals(health.get("status"));
        } catch (Exception e) {
            logger.warn("AI service health check failed: {}", e.getMessage());
            return false;
        }
    }
    
    private AIRecommendationResponse createErrorResponse(String message, String sessionId) {
        AIRecommendationResponse response = new AIRecommendationResponse();
        response.setAnswer(message);
        response.setSessionId(sessionId);
        response.setTimestamp(java.time.Instant.now().toString());
        return response;
    }
}