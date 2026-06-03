package com.smartcart.repository;

import com.smartcart.entity.Cart;
import com.smartcart.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CartRepository extends JpaRepository<Cart, Long> {
    
    Optional<Cart> findByUser(User user);
    
    Optional<Cart> findBySessionId(String sessionId);
    
    Optional<Cart> findByUserId(Long userId);
}