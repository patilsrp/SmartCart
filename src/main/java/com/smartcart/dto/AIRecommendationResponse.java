package com.smartcart.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AIRecommendationResponse {
    private String answer;
    
    @JsonProperty("session_id")
    private String sessionId;
    
    private String timestamp;
    
    public AIRecommendationResponse() {}
    
    public AIRecommendationResponse(String answer, String sessionId, String timestamp) {
        this.answer = answer;
        this.sessionId = sessionId;
        this.timestamp = timestamp;
    }
    
    public String getAnswer() {
        return answer;
    }
    
    public void setAnswer(String answer) {
        this.answer = answer;
    }
    
    public String getSessionId() {
        return sessionId;
    }
    
    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }
    
    public String getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }
}