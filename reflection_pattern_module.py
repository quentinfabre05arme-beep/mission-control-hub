#!/usr/bin/env python3
"""
Reflection Pattern Module v1.0
Implements self-review and iterative improvement before final output
Based on 2025 AI agent best practices - Reflection Pattern
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

@dataclass
class ReviewResult:
    """Result of reflection review"""
    passes: bool
    score: float
    issues: List[str]
    improvements: List[str]
    confidence: float

class ReflectionReviewer:
    """Critic module for self-improvement before delivery"""
    
    def __init__(self):
        self.review_criteria = {
            "factual_accuracy": {
                "weight": 0.25,
                "description": "Are claims supported by evidence?",
                "checks": ["data_sources", "statistics_verified", "attribution"]
            },
            "clarity": {
                "weight": 0.20,
                "description": "Is the message clear and understandable?",
                "checks": ["no_jargon", "logical_flow", "concise"]
            },
            "engagement_potential": {
                "weight": 0.20,
                "description": "Will this drive engagement?",
                "checks": ["hook_strength", "call_to_action", "reply_hook"]
            },
            "brand_alignment": {
                "weight": 0.15,
                "description": "Does this match the brand voice?",
                "checks": ["tone_consistent", "values_aligned", "professional"]
            },
            "algorithm_optimization": {
                "weight": 0.10,
                "description": "Is this optimized for platform algorithms?",
                "checks": ["length_optimal", "hashtags", "timing_hint"]
            },
            "originality": {
                "weight": 0.10,
                "description": "Is this fresh or derivative?",
                "checks": ["unique_angle", "not_repetitive", "value_add"]
            }
        }
        
    def review_content(self, content: Dict, context: Dict = None) -> ReviewResult:
        """
        Review content before delivery
        Returns: ReviewResult with pass/fail, score, and improvements
        """
        issues = []
        improvements = []
        criterion_scores = {}
        
        # Check each criterion
        for criterion_name, config in self.review_criteria.items():
            score, criterion_issues, criterion_improvements = self._evaluate_criterion(
                criterion_name, config, content
            )
            criterion_scores[criterion_name] = {
                "score": score,
                "weight": config["weight"],
                "issues": criterion_issues
            }
            issues.extend(criterion_issues)
            improvements.extend(criterion_improvements)
        
        # Calculate weighted score
        weighted_score = sum(
            s["score"] * s["weight"] for s in criterion_scores.values()
        )
        
        # Determine if content passes review
        passes = weighted_score >= 0.75 and len(issues) <= 3
        
        return ReviewResult(
            passes=passes,
            score=weighted_score,
            issues=issues,
            improvements=self._prioritize_improvements(improvements),
            confidence=weighted_score
        )
        
    def _evaluate_criterion(self, name: str, config: Dict, content: Dict) -> Tuple[float, List[str], List[str]]:
        """Evaluate a single criterion"""
        content_text = content.get("text", "")
        score = 0.8  # Base score
        issues = []
        improvements = []
        
        if name == "factual_accuracy":
            # Check for unsupported claims
            if "data" in content and not content.get("sources"):
                issues.append("Data claims without sources")
                improvements.append("Add source attribution for data points")
                score -= 0.2
                
        elif name == "clarity":
            # Check text clarity
            if len(content_text) > 280 and "\n\n" not in content_text:
                issues.append("Long text without paragraph breaks")
                improvements.append("Add line breaks for readability")
                score -= 0.15
                
        elif name == "engagement_potential":
            # Check for engagement hooks
            if "?" not in content_text and "reply" not in content_text.lower():
                issues.append("No clear engagement mechanism")
                improvements.append("Add a question or invitation to reply")
                score -= 0.15
                
            # Check hook strength
            if content_text and not self._has_strong_hook(content_text):
                issues.append("Hook could be stronger")
                improvements.append("Start with specific stat or bold claim")
                score -= 0.1
                
        elif name == "brand_alignment":
            # Check for thesis-first style
            if content_text and not self._has_thesis_first_structure(content_text):
                issues.append("Not thesis-first structure")
                improvements.append("Lead with clear thesis statement")
                score -= 0.1
                
        elif name == "algorithm_optimization":
            # Check length
            if len(content_text) > 280:
                issues.append("Single post exceeds 280 chars")
                improvements.append("Split into thread or trim content")
                score -= 0.2
                
        elif name == "originality":
            # Check for repetitive phrases
            common_phrases = ["in conclusion", "to summarize", "it's important to note"]
            for phrase in common_phrases:
                if phrase in content_text.lower():
                    issues.append(f"Contains generic phrase: '{phrase}'")
                    improvements.append("Replace with original phrasing")
                    score -= 0.05
        
        return max(0, score), issues, improvements
        
    def _has_strong_hook(self, text: str) -> bool:
        """Check if text has a strong opening hook"""
        # Strong hooks start with numbers, bold claims, or questions
        strong_patterns = [
            r'^\d+',  # Starts with number
            r'^(Most|Every|All|Never|Always)',  # Bold claim starters
            r'^(What|Why|How)',  # Question words
            r'[$\d]+[BMK]',  # Dollar amounts
        ]
        for pattern in strong_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
        
    def _has_thesis_first_structure(self, text: str) -> bool:
        """Check for thesis-first structure"""
        # Thesis-first usually has clear claim in first sentence
        first_sentence = text.split('.')[0] if '.' in text else text
        return len(first_sentence) < 150 and ('is' in first_sentence or 'are' in first_sentence)
        
    def _prioritize_improvements(self, improvements: List[str]) -> List[str]:
        """Prioritize improvements by impact"""
        # High impact improvements
        high_impact = ["Add", "Start with", "Lead with"]
        medium_impact = ["Replace", "Consider", "Add line"]
        
        def priority_key(imp):
            for i, prefix in enumerate(high_impact):
                if imp.startswith(prefix):
                    return (0, i)
            for i, prefix in enumerate(medium_impact):
                if imp.startswith(prefix):
                    return (1, i)
            return (2, 0)
        
        return sorted(list(set(improvements)), key=priority_key)

class ReflectionOrchestrator:
    """Orchestrate reflection-enhanced content creation"""
    
    def __init__(self):
        self.reviewer = ReflectionReviewer()
        self.max_iterations = 3
        self.min_score_threshold = 0.80
        
    def create_with_reflection(self, generate_func, context: Dict = None) -> Dict:
        """
        Create content with reflection loop
        
        Args:
            generate_func: Function that generates content
            context: Additional context for generation
            
        Returns:
            Dict with final content, review history, and scores
        """
        iteration = 0
        review_history = []
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # Generate content
            content = generate_func(context)
            
            # Review content
            review = self.reviewer.review_content(content, context)
            
            review_history.append({
                "iteration": iteration,
                "score": review.score,
                "passes": review.passes,
                "issues": review.issues,
                "improvements": review.improvements
            })
            
            # Check if content passes
            if review.passes and review.score >= self.min_score_threshold:
                return {
                    "content": content,
                    "final_score": review.score,
                    "iterations": iteration,
                    "review_history": review_history,
                    "status": "approved"
                }
            
            # Update context with improvements for next iteration
            if context is None:
                context = {}
            context["improvements_from_last"] = review.improvements
            
            print(f"  Iteration {iteration}: Score {review.score:.2f} - {len(review.issues)} issues")
        
        # Return best attempt if max iterations reached
        return {
            "content": content,
            "final_score": review.score,
            "iterations": iteration,
            "review_history": review_history,
            "status": "max_iterations_reached",
            "note": "Content did not pass review threshold, manual review recommended"
        }

def example_content_generator(context: Dict) -> Dict:
    """Example content generator for testing"""
    improvements = context.get("improvements_from_last", [])
    
    # Simulate applying improvements
    text = "The infrastructure build phase is accelerating. Data centers representing $50B+ in investment are coming online in 2025."
    
    if "Add source attribution" in str(improvements):
        text += " [Source: McKinsey]"
    if "Add a question" in str(improvements):
        text += "\n\nWhat infrastructure plays are you tracking?"
    if "Start with specific stat" in str(improvements):
        text = "$50B+ in data center investment is hitting in 2025.\n\n" + text
    
    return {
        "text": text,
        "data": {"investment": "$50B+"},
        "sources": ["McKinsey"] if "Add source attribution" in str(improvements) else []
    }

def main():
    """Demonstrate reflection pattern"""
    orchestrator = ReflectionOrchestrator()
    
    print("=== Reflection Pattern Demo ===\n")
    
    result = orchestrator.create_with_reflection(
        generate_func=example_content_generator,
        context={"topic": "AI Infrastructure"}
    )
    
    print(f"\nFinal Status: {result['status']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Final Score: {result['final_score']:.2f}")
    print(f"\nContent:\n{result['content']['text']}")
    
    if result['review_history']:
        print("\nReview History:")
        for review in result['review_history']:
            print(f"  Iter {review['iteration']}: {review['score']:.2f} - {review['passes']}")

if __name__ == "__main__":
    main()
