package com.smartcart.repository;

import com.smartcart.entity.Order;
import com.smartcart.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    
    List<Order> findByUser(User user);
    
    List<Order> findByUserId(Long userId);
    
    Optional<Order> findByOrderNumber(String orderNumber);
    
    List<Order> findByStatus(Order.OrderStatus status);
    
    List<Order> findByUserOrderByCreatedAtDesc(User user);
}