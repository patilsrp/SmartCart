package com.smartcart.dto;

public class AIRecommendationRequest {
    private String question;
    private String sessionId;
    
    public AIRecommendationRequest() {}
    
    public AIRecommendationRequest(String question) {
        this.question = question;
    }
    
    public AIRecommendationRequest(String question, String sessionId) {
        this.question = question;
        this.sessionId = sessionId;
    }
    
    public String getQuestion() {
        return question;
    }
    
    public void setQuestion(String question) {
        this.question = question;
    }
    
    public String getSessionId() {
        return sessionId;
    }
    
    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }
}