package com.smartcart.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import java.util.Map;

public class ConversationalRequest {
    private String question;
    
    private List<Map<String, String>> history;
    
    @JsonProperty("session_id")
    private String sessionId;
    
    public ConversationalRequest() {}
    
    public ConversationalRequest(String question, List<Map<String, String>> history, String sessionId) {
        this.question = question;
        this.history = history;
        this.sessionId = sessionId;
    }
    
    public String getQuestion() {
        return question;
    }
    
    public void setQuestion(String question) {
        this.question = question;
    }
    
    public List<Map<String, String>> getHistory() {
        return history;
    }
    
    public void setHistory(List<Map<String, String>> history) {
        this.history = history;
    }
    
    public String getSessionId() {
        return sessionId;
    }
    
    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }
}