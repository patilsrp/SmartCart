import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from rag import SmartCartRAG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class RAGEvaluator:
    def __init__(self):
        self.rag = SmartCartRAG()
        self.test_cases = self._load_test_cases()
        
    def _load_test_cases(self) -> List[Dict[str, Any]]:
        """Define test queries with expected product matches."""
        return [
            {
                "query": "Show me a quiet laptop under 60k for college",
                "expected_products": ["Acer Aspire 5", "Dell Inspiron 15 3000", "ASUS VivoBook 15"],
                "expected_keywords": ["quiet", "student", "battery", "under", "budget"],
                "category": "laptop"
            },
            {
                "query": "I need a budget smartphone with good camera",
                "expected_products": ["OnePlus 11R"],
                "expected_keywords": ["camera", "budget", "affordable"],
                "category": "smartphone"
            },
            {
                "query": "What tablets do you have?",
                "expected_products": ["iPad Air", "Samsung Galaxy Tab S8"],
                "expected_keywords": ["tablet", "iPad", "Samsung"],
                "category": "tablet"
            },
            {
                "query": "Looking for noise canceling headphones",
                "expected_products": ["Sony WH-1000XM5", "AirPods Pro 2"],
                "expected_keywords": ["noise", "canceling", "ANC"],
                "category": "headphones"
            },
            {
                "query": "Best laptop for gaming under 80000",
                "expected_products": ["Lenovo IdeaPad Gaming 3"],
                "expected_keywords": ["gaming", "graphics", "RTX", "120Hz"],
                "category": "laptop"
            },
            {
                "query": "Cheapest laptop you have",
                "expected_products": ["Dell Inspiron 15 3000"],
                "expected_keywords": ["budget", "affordable", "42990"],
                "category": "laptop"
            },
            {
                "query": "iPhone for sale",
                "expected_products": ["iPhone 14"],
                "expected_keywords": ["iPhone", "iOS", "Apple"],
                "category": "smartphone"
            },
            {
                "query": "e-reader for reading books",
                "expected_products": ["Kindle Paperwhite"],
                "expected_keywords": ["Kindle", "e-reader", "books", "reading"],
                "category": "e-reader"
            },
            {
                "query": "lightweight laptop with good keyboard",
                "expected_products": ["HP Pavilion 14"],
                "expected_keywords": ["lightweight", "keyboard", "ultrabook"],
                "category": "laptop"
            },
            {
                "query": "Premium flagship phone",
                "expected_products": ["Samsung Galaxy S23", "iPhone 14"],
                "expected_keywords": ["flagship", "premium", "camera"],
                "category": "smartphone"
            }
        ]
    
    def evaluate_response(self, query: str, response: str, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single RAG response against expected results."""
        results = {
            "query": query,
            "response": response[:200] + "..." if len(response) > 200 else response,
            "metrics": {}
        }
        
        response_lower = response.lower()
        
        product_matches = sum(1 for product in test_case["expected_products"] 
                             if product.lower() in response_lower)
        results["metrics"]["product_recall"] = product_matches / len(test_case["expected_products"])
        
        keyword_matches = sum(1 for keyword in test_case["expected_keywords"]
                             if keyword.lower() in response_lower)
        results["metrics"]["keyword_coverage"] = keyword_matches / len(test_case["expected_keywords"])
        
        results["metrics"]["response_length"] = len(response)
        results["metrics"]["mentions_category"] = test_case["category"] in response_lower
        
        results["metrics"]["overall_score"] = (
            results["metrics"]["product_recall"] * 0.5 +
            results["metrics"]["keyword_coverage"] * 0.3 +
            (1 if results["metrics"]["mentions_category"] else 0) * 0.2
        )
        
        return results
    
    def run_evaluation(self) -> Dict[str, Any]:
        """Run evaluation on all test cases."""
        logger.info(f"Running evaluation on {len(self.test_cases)} test cases...")
        
        all_results = []
        total_scores = []
        
        for i, test_case in enumerate(self.test_cases, 1):
            logger.info(f"Test {i}/{len(self.test_cases)}: {test_case['query']}")
            
            try:
                response = self.rag.ask(test_case["query"])
                result = self.evaluate_response(test_case["query"], response, test_case)
                all_results.append(result)
                total_scores.append(result["metrics"]["overall_score"])
                
                logger.info(f"  Score: {result['metrics']['overall_score']:.2f}")
                
            except Exception as e:
                logger.error(f"  Error: {e}")
                all_results.append({
                    "query": test_case["query"],
                    "error": str(e),
                    "metrics": {"overall_score": 0}
                })
                total_scores.append(0)
        
        avg_score = sum(total_scores) / len(total_scores) if total_scores else 0
        
        summary = {
            "total_tests": len(self.test_cases),
            "average_score": avg_score,
            "passed_tests": sum(1 for score in total_scores if score >= 0.6),
            "failed_tests": sum(1 for score in total_scores if score < 0.6),
            "results": all_results
        }
        
        return summary
    
    def test_conversational_flow(self):
        """Test multi-turn conversation capability."""
        logger.info("\nTesting conversational flow...")
        
        conversation = [
            {"role": "user", "content": "Show me laptops"},
            {"role": "assistant", "content": "I can help you find the perfect laptop..."}
        ]
        
        follow_ups = [
            "Now show me the cheaper ones",
            "What about gaming laptops?",
            "Which one has the best battery life?"
        ]
        
        logger.info("Initial query: Show me laptops")
        initial_response = self.rag.ask("Show me laptops")
        logger.info(f"Initial response: {initial_response[:100]}...")
        
        conversation[1]["content"] = initial_response
        
        for follow_up in follow_ups:
            logger.info(f"\nFollow-up: {follow_up}")
            response = self.rag.ask_with_history(follow_up, conversation)
            logger.info(f"Response: {response[:100]}...")
            
            conversation.append({"role": "user", "content": follow_up})
            conversation.append({"role": "assistant", "content": response})
        
        return len(conversation) // 2

def main():
    """Run the evaluation suite."""
    evaluator = RAGEvaluator()
    
    print("=" * 80)
    print("SmartCart RAG System Evaluation")
    print("=" * 80)
    
    results = evaluator.run_evaluation()
    
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Average Score: {results['average_score']:.2%}")
    print(f"Passed Tests: {results['passed_tests']}/{results['total_tests']}")
    print(f"Failed Tests: {results['failed_tests']}/{results['total_tests']}")
    
    print("\n" + "=" * 80)
    print("DETAILED RESULTS")
    print("=" * 80)
    
    for result in results['results']:
        print(f"\nQuery: {result['query']}")
        if 'error' in result:
            print(f"  ERROR: {result['error']}")
        else:
            print(f"  Overall Score: {result['metrics']['overall_score']:.2f}")
            print(f"  Product Recall: {result['metrics']['product_recall']:.2f}")
            print(f"  Keyword Coverage: {result['metrics']['keyword_coverage']:.2f}")
    
    print("\n" + "=" * 80)
    print("CONVERSATIONAL TEST")
    print("=" * 80)
    
    turns = evaluator.test_conversational_flow()
    print(f"\nSuccessfully completed {turns} conversation turns")
    
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nDetailed results saved to evaluation_results.json")

if __name__ == "__main__":
    main()