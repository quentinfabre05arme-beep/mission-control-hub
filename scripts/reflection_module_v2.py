#!/usr/bin/env python3
"""
reflection_module_v2.py
Enhanced Reflection Pattern Module with 7-Dimension Quality Scoring
Based on 2025-2026 AI Agent Best Practices Research

Features:
- Self-review before final output (mandatory quality gate)
- 7-dimension comprehensive scoring
- Iterative improvement with pass/fail thresholds
- Automatic improvement suggestions
- Algorithm optimization for X/Twitter
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityDimension(Enum):
    FACTUAL_ACCURACY = "factual_accuracy"
    CLARITY = "clarity"
    ENGAGEMENT_POTENTIAL = "engagement_potential"
    BRAND_ALIGNMENT = "brand_alignment"
    ALGORITHM_OPTIMIZATION = "algorithm_optimization"
    ORIGINALITY = "originality"
    AUTHENTICITY = "authenticity"


class ReviewStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_REVISION = "needs_revision"


@dataclass
class QualityScore:
    """Individual dimension score"""
    dimension: str
    score: float  # 0.0 to 1.0
    weight: float  # Importance weight
    notes: List[str] = field(default_factory=list)
    
    @property
    def weighted_score(self) -> float:
        return self.score * self.weight


@dataclass
class ReflectionResult:
    """Complete reflection result"""
    content_id: str
    overall_score: float
    status: ReviewStatus
    dimension_scores: Dict[str, QualityScore]
    recommendations: List[str]
    improved_version: Optional[str]
    review_timestamp: str
    iteration: int = 1
    max_iterations: int = 3
    
    def to_dict(self) -> Dict:
        return {
            "content_id": self.content_id,
            "overall_score": round(self.overall_score, 2),
            "status": self.status.value,
            "dimensions": {
                dim: {
                    "score": round(qs.score, 2),
                    "weight": qs.weight,
                    "notes": qs.notes
                }
                for dim, qs in self.dimension_scores.items()
            },
            "recommendations": self.recommendations,
            "iteration": self.iteration,
            "max_iterations": self.max_iterations,
            "reviewed_at": self.review_timestamp
        }


class ReflectionModule:
    """
    Enhanced reflection module implementing 7-dimension quality scoring
    Based on 2025-2026 AI agent best practices research
    """
    
    # Dimension weights (customizable based on platform/strategy)
    DEFAULT_DIMENSIONS = {
        QualityDimension.FACTUAL_ACCURACY: 0.15,
        QualityDimension.CLARITY: 0.10,
        QualityDimension.ENGAGEMENT_POTENTIAL: 0.20,
        QualityDimension.BRAND_ALIGNMENT: 0.15,
        QualityDimension.ALGORITHM_OPTIMIZATION: 0.20,
        QualityDimension.ORIGINALITY: 0.10,
        QualityDimension.AUTHENTICITY: 0.10
    }
    
    # Pass threshold (configurable)
    PASS_THRESHOLD = 0.75
    EXCELLENCE_THRESHOLD = 0.85
    
    def __init__(self, custom_weights: Optional[Dict[str, float]] = None):
        self.dimensions = custom_weights or self.DEFAULT_DIMENSIONS
        self.review_history: List[ReflectionResult] = []
        logger.info("ReflectionModule v2.0 initialized")
    
    def reflect(self, content: str, content_id: str, 
                context: Optional[Dict] = None,
                iteration: int = 1) -> ReflectionResult:
        """
        Perform comprehensive reflection on content
        
        Args:
            content: The content to review
            content_id: Unique identifier for the content
            context: Additional context (platform, topic, brand voice, etc.)
            iteration: Current iteration number
        
        Returns:
            ReflectionResult with scores and recommendations
        """
        logger.info(f"Starting reflection for {content_id} (iteration {iteration})")
        
        dimension_scores = {}
        
        # Evaluate each dimension
        for dimension, weight in self.dimensions.items():
            score, notes = self._evaluate_dimension(dimension, content, context)
            dimension_scores[dimension.value] = QualityScore(
                dimension=dimension.value,
                score=score,
                weight=weight,
                notes=notes
            )
        
        # Calculate overall weighted score
        total_weight = sum(qs.weight for qs in dimension_scores.values())
        weighted_sum = sum(qs.weighted_score for qs in dimension_scores.values())
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(dimension_scores, content)
        
        # Determine status
        status = self._determine_status(overall_score, dimension_scores, iteration)
        
        # Generate improved version if needed
        improved_version = None
        if status == ReviewStatus.NEEDS_REVISION and iteration < self.max_iterations:
            improved_version = self._improve_content(content, dimension_scores, recommendations)
        
        result = ReflectionResult(
            content_id=content_id,
            overall_score=overall_score,
            status=status,
            dimension_scores=dimension_scores,
            recommendations=recommendations,
            improved_version=improved_version,
            review_timestamp=datetime.utcnow().isoformat(),
            iteration=iteration
        )
        
        self.review_history.append(result)
        logger.info(f"Reflection complete: {overall_score:.2f}/1.0 - {status.value}")
        
        return result
    
    def _evaluate_dimension(self, dimension: QualityDimension, 
                          content: str, 
                          context: Optional[Dict]) -> Tuple[float, List[str]]:
        """Evaluate a specific quality dimension"""
        
        notes = []
        score = 0.5  # Default baseline
        
        if dimension == QualityDimension.FACTUAL_ACCURACY:
            # Check for data, numbers, citations
            has_numbers = bool(re.search(r'\d+%?|\$\d+', content))
            has_data_refs = any(term in content.lower() for term in 
                              ['data', 'research', 'study', 'report', 'analysis'])
            
            if has_numbers and has_data_refs:
                score = 0.9
                notes.append("Strong data-backed claims")
            elif has_numbers:
                score = 0.75
                notes.append("Contains numeric data")
            else:
                score = 0.6
                notes.append("Consider adding data points")
        
        elif dimension == QualityDimension.CLARITY:
            # Check sentence structure, readability
            sentences = content.split('.')
            avg_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
            
            if avg_length < 15:
                score = 0.9
                notes.append("Clear, concise sentences")
            elif avg_length < 20:
                score = 0.75
                notes.append("Good readability")
            else:
                score = 0.6
                notes.append("Consider shorter sentences for social media")
        
        elif dimension == QualityDimension.ENGAGEMENT_POTENTIAL:
            # Check for engagement hooks
            has_question = '?' in content
            has_cta = any(term in content.lower() for term in 
                         ['what do you think', 'share your', 'comment', 'let me know'])
            has_hook = any(term in content.lower() for term in 
                          ['here\'s why', 'the truth about', 'most people', 'nobody talks about'])
            
            engagement_score = 0
            if has_question: engagement_score += 0.3; notes.append("Contains question")
            if has_cta: engagement_score += 0.3; notes.append("Has call-to-action")
            if has_hook: engagement_score += 0.3; notes.append("Strong hook")
            
            score = min(0.95, 0.3 + engagement_score)
        
        elif dimension == QualityDimension.BRAND_ALIGNMENT:
            # Check against brand voice (context-dependent)
            brand_voice = context.get('brand_voice', {}) if context else {}
            
            # Default: professional, data-driven, analytical
            has_analysis = any(term in content.lower() for term in 
                             ['analysis', 'trend', 'data', 'insight'])
            is_professional = not any(term in content.lower() for term in 
                                      ['omg', 'lol', 'wtf', 'dude'])
            
            if has_analysis and is_professional:
                score = 0.9
                notes.append("Aligned with analytical brand voice")
            elif is_professional:
                score = 0.75
                notes.append("Professional tone maintained")
            else:
                score = 0.6
                notes.append("Review brand voice alignment")
        
        elif dimension == QualityDimension.ALGORITHM_OPTIMIZATION:
            # X/Twitter algorithm optimization (from research)
            platform = context.get('platform', 'x') if context else 'x'
            
            if platform == 'x':
                # Check for reply hooks (13.5x weight)
                has_reply_hook = any(term in content.lower() for term in 
                                    ['what do you think', 'agree or disagree', 'thoughts?'])
                # Check for link placement (penalize in main tweet)
                has_link_main = 'http' in content
                # Check length (optimal: 100-280 chars)
                optimal_length = 100 <= len(content) <= 280
                
                score = 0.6
                if has_reply_hook: 
                    score += 0.2
                    notes.append("Reply hook present (13.5x weight)")
                if not has_link_main: 
                    score += 0.1
                    notes.append("No link in main tweet (algorithm-friendly)")
                if optimal_length: 
                    score += 0.1
                    notes.append("Optimal length for engagement")
        
        elif dimension == QualityDimension.ORIGINALITY:
            # Check for unique perspective
            has_contrarian = any(term in content.lower() for term in 
                                ['unpopular opinion', 'contrarian', 'actually', 'the truth'])
            has_fresh_take = any(term in content.lower() for term in 
                                ['nobody is talking about', 'what if i told you', 'here\'s what'])
            
            if has_contrarian or has_fresh_take:
                score = 0.9
                notes.append("Original/contrarian perspective")
            else:
                score = 0.7
                notes.append("Consider unique angle")
        
        elif dimension == QualityDimension.AUTHENTICITY:
            # Check for human voice (2026 research: authenticity wins)
            has_personal = any(term in content.lower() for term in 
                              ['i think', 'my', 'i\'ve', 'in my experience'])
            has_raw = any(term in content.lower() for term in 
                         ['honestly', 'real talk', 'let\'s be honest'])
            too_polished = len(content) > 250 and content.count('.') > 5
            
            if (has_personal or has_raw) and not too_polished:
                score = 0.9
                notes.append("Authentic human voice")
            elif has_personal:
                score = 0.75
                notes.append("Personal perspective present")
            else:
                score = 0.65
                notes.append("Consider adding personal touch")
        
        return round(score, 2), notes
    
    def _generate_recommendations(self, dimension_scores: Dict[str, QualityScore], 
                                  content: str) -> List[str]:
        """Generate improvement recommendations based on scores"""
        recommendations = []
        
        # Low scores trigger specific recommendations
        low_threshold = 0.75
        
        if dimension_scores.get('factual_accuracy', QualityScore('', 1, 0)).score < low_threshold:
            recommendations.append("Add specific data points, statistics, or research citations")
        
        if dimension_scores.get('engagement_potential', QualityScore('', 1, 0)).score < low_threshold:
            recommendations.append("Include a question or call-to-action to drive engagement")
        
        if dimension_scores.get('algorithm_optimization', QualityScore('', 1, 0)).score < low_threshold:
            recommendations.append("Add reply hook, optimize for X algorithm (replies weighted 13.5x)")
        
        if dimension_scores.get('authenticity', QualityScore('', 1, 0)).score < low_threshold:
            recommendations.append("Add personal experience or raw perspective for authenticity")
        
        if dimension_scores.get('originality', QualityScore('', 1, 0)).score < low_threshold:
            recommendations.append("Consider contrarian or less-discussed angle")
        
        if dimension_scores.get('clarity', QualityScore('', 1, 0)).score < low_threshold:
            recommendations.append("Simplify sentences for better readability")
        
        if not recommendations:
            recommendations.append("Content meets quality thresholds - no changes needed")
        
        return recommendations
    
    def _determine_status(self, overall_score: float, 
                          dimension_scores: Dict[str, QualityScore],
                          iteration: int) -> ReviewStatus:
        """Determine review status based on scores"""
        
        if overall_score >= self.EXCELLENCE_THRESHOLD:
            return ReviewStatus.PASSED
        elif overall_score >= self.PASS_THRESHOLD:
            # Check for any critical failures
            critical_failures = sum(1 for qs in dimension_scores.values() 
                                   if qs.score < 0.5)
            if critical_failures > 0 and iteration < self.max_iterations:
                return ReviewStatus.NEEDS_REVISION
            return ReviewStatus.PASSED
        elif iteration < self.max_iterations:
            return ReviewStatus.NEEDS_REVISION
        else:
            return ReviewStatus.FAILED
    
    def _improve_content(self, content: str, 
                        dimension_scores: Dict[str, QualityScore],
                        recommendations: List[str]) -> str:
        """Generate improved version of content"""
        # This would use LLM to rewrite based on recommendations
        # For now, return placeholder with suggestions
        improved = f"[IMPROVED VERSION WOULD BE GENERATED HERE]\n\n"
        improved += f"Original: {content[:100]}...\n\n"
        improved += "Improvements based on:\n"
        for rec in recommendations:
            improved += f"- {rec}\n"
        
        return improved
    
    def batch_reflect(self, contents: List[Dict], 
                     context: Optional[Dict] = None) -> List[ReflectionResult]:
        """Reflect on multiple content items"""
        results = []
        for item in contents:
            result = self.reflect(
                content=item.get('content', ''),
                content_id=item.get('id', ''),
                context=context
            )
            results.append(result)
        return results
    
    def get_best_content(self, results: List[ReflectionResult]) -> Optional[ReflectionResult]:
        """Get the highest-scoring content from batch"""
        if not results:
            return None
        return max(results, key=lambda r: r.overall_score)
    
    def export_history(self) -> List[Dict]:
        """Export review history for analysis"""
        return [r.to_dict() for r in self.review_history]


# Example usage
if __name__ == "__main__":
    # Initialize reflection module
    reflector = ReflectionModule()
    
    # Example content to review
    test_content = """
    73% of AI projects fail within the first year.
    
    Not because the technology doesn't work.
    Because organizations try to automate everything at once.
    
    The winners?
    They start with ONE workflow.
    They master it.
    Then they scale.
    
    What's your biggest automation mistake?
    """
    
    context = {
        "platform": "x",
        "brand_voice": {
            "tone": "analytical",
            "style": "data-driven"
        },
        "topic": "AI automation"
    }
    
    # Perform reflection
    result = reflector.reflect(
        content=test_content,
        content_id="test_post_001",
        context=context
    )
    
    # Print results
    print("=" * 60)
    print("REFLECTION RESULT")
    print("=" * 60)
    print(json.dumps(result.to_dict(), indent=2))
    
    # Check if content passed
    if result.status == ReviewStatus.PASSED:
        print("\n✅ Content PASSED quality gates")
    elif result.status == ReviewStatus.NEEDS_REVISION:
        print("\n⚠️ Content needs revision")
    else:
        print("\n❌ Content FAILED quality gates")
