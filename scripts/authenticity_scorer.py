#!/usr/bin/env python3
"""
authenticity_scorer.py
Human Voice Detection and Authenticity Scoring
Based on 2025-2026 Research: Authenticity Wins in AI-Saturated Landscape

Features:
- Human voice detection and scoring
- Raw/imperfect content suggestions
- Transparency markers for AI-generated content (EU AI Act compliance)
- Brand voice calibration without over-polishing
- Authenticity vs Polish balance scoring
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


class AuthenticityLevel(Enum):
    HIGHLY_AUTHENTIC = "highly_authentic"      # Raw, personal, genuine
    AUTHENTIC = "authentic"                      # Human voice maintained
    MODERATE = "moderate"                        # Some polish, some raw
    POLISHED = "polished"                        # Professional, less personal
    OVER_POLISHED = "over_polished"              # Risk of seeming AI-generated


class ContentOrigin(Enum):
    HUMAN_WRITTEN = "human_written"
    AI_ASSISTED = "ai_assisted"
    AI_GENERATED = "ai_generated"
    AI_EDITED = "ai_edited"


@dataclass
class AuthenticityScore:
    """Authenticity analysis result"""
    content_id: str
    overall_score: float  # 0-1, higher = more authentic
    level: AuthenticityLevel
    dimensions: Dict[str, float]
    red_flags: List[str]
    strengths: List[str]
    suggestions: List[str]
    transparency_required: bool
    transparency_label: Optional[str]
    analyzed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "content_id": self.content_id,
            "overall_score": round(self.overall_score, 2),
            "level": self.level.value,
            "dimensions": {k: round(v, 2) for k, v in self.dimensions.items()},
            "red_flags": self.red_flags,
            "strengths": self.strengths,
            "suggestions": self.suggestions,
            "transparency_required": self.transparency_required,
            "transparency_label": self.transparency_label,
            "analyzed_at": self.analyzed_at
        }


class AuthenticityScorer:
    """
    Human voice detection and authenticity scoring system
    Implements 2026 research finding: Authenticity wins over polish
    """
    
    # Human voice indicators (positive signals)
    HUMAN_INDICATORS = {
        "personal_pronouns": ['i', 'my', 'me', 'we', 'our'],
        "opinion_markers": ['i think', 'i believe', 'in my opinion', 'to me'],
        "experience_markers": ['i\'ve', 'i\'ve been', 'in my experience', 'what i\'ve learned'],
        "vulnerability_markers": ['honestly', 'i\'ll admit', 'i struggle with', 'not gonna lie'],
        "conversation_markers": ['you know', 'look', 'listen', 'here\'s the thing'],
        "raw_markers": ['real talk', 'let me be honest', 'truth is', 'here\'s what nobody tells you'],
        "imperfection_markers": ['kind of', 'sort of', 'maybe', 'probably', 'i guess'],
        "story_markers": ['when i', 'back when', 'i remember', 'i once', 'there was a time']
    }
    
    # AI/over-polished indicators (red flags)
    AI_INDICATORS = {
        "formal_structures": ['furthermore', 'moreover', 'consequently', 'therefore', 'thus'],
        "buzzword_heavy": ['leverage', 'synergy', 'paradigm', 'optimization', 'strategic'],
        "overly_perfect": ['it is imperative', 'it is essential', 'it is crucial'],
        "generic_openings": ['in today\'s world', 'in the digital age', 'in conclusion', 'ultimately'],
        "corporate_speak": ['best practices', 'moving forward', 'circle back', 'touch base'],
        "list_cliches": ['without further ado', 'last but not least', 'to sum up'],
        "ai_phrases": ['as an ai', 'as a language model', 'i don\'t have personal experiences'],
        "excessive_enthusiasm": ['incredible', 'revolutionary', 'game-changing', 'groundbreaking']
    }
    
    # EU AI Act transparency requirements
    TRANSPARENCY_REQUIRED = {
        ContentOrigin.AI_GENERATED: True,
        ContentOrigin.AI_ASSISTED: True,
        ContentOrigin.AI_EDITED: False,  # May need disclosure depending on extent
        ContentOrigin.HUMAN_WRITTEN: False
    }
    
    def __init__(self, brand_voice: Optional[Dict] = None):
        self.brand_voice = brand_voice or {
            "tone": "analytical",
            "style": "professional",
            "authenticity_target": 0.75  # Target authenticity score
        }
        self.scoring_history: List[AuthenticityScore] = []
        logger.info("AuthenticityScorer initialized")
    
    def score(self, content: str, content_id: str,
             origin: ContentOrigin = ContentOrigin.AI_ASSISTED,
             author_type: str = "individual") -> AuthenticityScore:
        """
        Score content authenticity
        
        Args:
            content: Content to analyze
            content_id: Unique identifier
            origin: Origin of content (for transparency labeling)
            author_type: Type of author (individual, brand, corporate)
        
        Returns:
            AuthenticityScore with analysis
        """
        logger.info(f"Scoring authenticity for {content_id}")
        
        text_lower = content.lower()
        
        # Calculate dimension scores
        dimensions = {
            "personal_voice": self._score_personal_voice(text_lower),
            "rawness": self._score_rawness(text_lower),
            "conversational": self._score_conversational(text_lower),
            "vulnerability": self._score_vulnerability(text_lower),
            "imperfection": self._score_imperfection(text_lower),
            "storytelling": self._score_storytelling(text_lower),
            "ai_risk": self._score_ai_risk(text_lower)
        }
        
        # Calculate overall score
        # AI risk is inverted (lower = better)
        positive_dims = ["personal_voice", "rawness", "conversational", 
                        "vulnerability", "imperfection", "storytelling"]
        positive_avg = sum(dimensions[d] for d in positive_dims) / len(positive_dims)
        
        # Weight: 80% positive dimensions, 20% inverse AI risk
        overall_score = (positive_avg * 0.8) + ((1 - dimensions["ai_risk"]) * 0.2)
        
        # Determine authenticity level
        level = self._determine_level(overall_score, dimensions)
        
        # Identify red flags and strengths
        red_flags = self._identify_red_flags(text_lower, dimensions)
        strengths = self._identify_strengths(text_lower, dimensions)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(dimensions, red_flags)
        
        # Determine transparency requirements
        transparency_required = self.TRANSPARENCY_REQUIRED.get(origin, False)
        transparency_label = self._generate_transparency_label(origin) if transparency_required else None
        
        result = AuthenticityScore(
            content_id=content_id,
            overall_score=overall_score,
            level=level,
            dimensions=dimensions,
            red_flags=red_flags,
            strengths=strengths,
            suggestions=suggestions,
            transparency_required=transparency_required,
            transparency_label=transparency_label
        )
        
        self.scoring_history.append(result)
        logger.info(f"Authenticity score: {overall_score:.2f} ({level.value})")
        
        return result
    
    def _score_personal_voice(self, text: str) -> float:
        """Score personal voice indicators"""
        indicators = self.HUMAN_INDICATORS["personal_pronouns"]
        opinion_markers = self.HUMAN_INDICATORS["opinion_markers"]
        
        words = text.split()
        pronoun_count = sum(1 for word in words if word in indicators)
        opinion_count = sum(1 for marker in opinion_markers if marker in text)
        
        # Normalize scores
        pronoun_score = min(1.0, pronoun_count / max(len(words) * 0.05, 1))
        opinion_score = min(1.0, opinion_count / 2)
        
        return (pronoun_score * 0.6) + (opinion_score * 0.4)
    
    def _score_rawness(self, text: str) -> float:
        """Score raw/unfiltered voice"""
        raw_markers = self.HUMAN_INDICATORS["raw_markers"]
        conversation_markers = self.HUMAN_INDICATORS["conversation_markers"]
        
        raw_count = sum(1 for marker in raw_markers if marker in text)
        conv_count = sum(1 for marker in conversation_markers if marker in text)
        
        return min(1.0, (raw_count * 0.3) + (conv_count * 0.15))
    
    def _score_conversational(self, text: str) -> float:
        """Score conversational tone"""
        # Check for questions
        has_questions = text.count('?') > 0
        
        # Check for direct address
        has_you = 'you' in text or 'your' in text
        
        # Check for contractions
        contractions = len(re.findall(r"\w+'\w+", text))
        
        score = 0
        if has_questions: score += 0.3
        if has_you: score += 0.3
        score += min(0.4, contractions * 0.1)
        
        return score
    
    def _score_vulnerability(self, text: str) -> float:
        """Score vulnerability markers"""
        vuln_markers = self.HUMAN_INDICATORS["vulnerability_markers"]
        
        vuln_count = sum(1 for marker in vuln_markers if marker in text)
        return min(1.0, vuln_count * 0.4)
    
    def _score_imperfection(self, text: str) -> float:
        """Score intentional imperfection (authenticity signal)"""
        imperfection_markers = self.HUMAN_INDICATORS["imperfection_markers"]
        
        # Count hedging words
        hedge_count = sum(1 for marker in imperfection_markers if marker in text)
        
        # Check for sentence fragments
        fragments = len([s for s in text.split('.') if len(s.strip()) < 10 and len(s.strip()) > 0])
        
        score = min(1.0, (hedge_count * 0.2) + (fragments * 0.1))
        return score
    
    def _score_storytelling(self, text: str) -> float:
        """Score storytelling elements"""
        story_markers = self.HUMAN_INDICATORS["story_markers"]
        
        story_count = sum(1 for marker in story_markers if marker in text)
        return min(1.0, story_count * 0.4)
    
    def _score_ai_risk(self, text: str) -> float:
        """Score risk of appearing AI-generated"""
        risk_score = 0
        
        # Check for AI indicators
        for category, phrases in self.AI_INDICATORS.items():
            count = sum(1 for phrase in phrases if phrase in text)
            if category == "ai_phrases":
                risk_score += count * 0.5  # Heavy penalty
            elif category == "formal_structures":
                risk_score += count * 0.15
            elif category == "generic_openings":
                risk_score += count * 0.2
            else:
                risk_score += count * 0.1
        
        # Check for overly perfect structure
        sentences = [s for s in text.split('.') if s.strip()]
        avg_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if 18 <= avg_length <= 22:  # AI often produces this range
            risk_score += 0.15
        
        # Check for lack of typos/imperfections
        # (In production, would check for actual human error patterns)
        
        return min(1.0, risk_score)
    
    def _determine_level(self, score: float, dimensions: Dict) -> AuthenticityLevel:
        """Determine authenticity level from score"""
        if score >= 0.85:
            return AuthenticityLevel.HIGHLY_AUTHENTIC
        elif score >= 0.70:
            return AuthenticityLevel.AUTHENTIC
        elif score >= 0.55:
            return AuthenticityLevel.MODERATE
        elif score >= 0.40:
            return AuthenticityLevel.POLISHED
        else:
            return AuthenticityLevel.OVER_POLISHED
    
    def _identify_red_flags(self, text: str, dimensions: Dict) -> List[str]:
        """Identify authenticity red flags"""
        flags = []
        
        if dimensions["ai_risk"] > 0.6:
            flags.append("High risk of appearing AI-generated")
        
        if dimensions["personal_voice"] < 0.3:
            flags.append("Lacks personal voice - too detached")
        
        if dimensions["rawness"] < 0.2:
            flags.append("Overly polished - lacks raw authenticity")
        
        # Check for specific AI phrases
        ai_phrases = self.AI_INDICATORS["ai_phrases"]
        for phrase in ai_phrases:
            if phrase in text:
                flags.append(f"Contains AI indicator phrase: '{phrase}'")
        
        return flags
    
    def _identify_strengths(self, text: str, dimensions: Dict) -> List[str]:
        """Identify authenticity strengths"""
        strengths = []
        
        if dimensions["personal_voice"] > 0.7:
            strengths.append("Strong personal voice with 'I' statements")
        
        if dimensions["vulnerability"] > 0.5:
            strengths.append("Shows vulnerability - builds trust")
        
        if dimensions["storytelling"] > 0.5:
            strengths.append("Uses storytelling - engaging narrative")
        
        if dimensions["rawness"] > 0.5:
            strengths.append("Raw, unfiltered voice - stands out")
        
        if dimensions["conversational"] > 0.6:
            strengths.append("Conversational tone - invites engagement")
        
        return strengths
    
    def _generate_suggestions(self, dimensions: Dict, red_flags: List) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if dimensions["personal_voice"] < 0.5:
            suggestions.append("Add personal pronouns ('I', 'my', 'I've') to humanize")
        
        if dimensions["vulnerability"] < 0.3:
            suggestions.append("Include vulnerability ('honestly', 'I'll admit') for authenticity")
        
        if dimensions["rawness"] < 0.3:
            suggestions.append("Use conversational markers ('look', 'here's the thing') for raw voice")
        
        if dimensions["ai_risk"] > 0.4:
            suggestions.append("Reduce formal structure - avoid 'furthermore', 'consequently'")
        
        if dimensions["storytelling"] < 0.3:
            suggestions.append("Add personal story or experience")
        
        if dimensions["conversational"] < 0.4:
            suggestions.append("Add questions or direct address ('you') to engage")
        
        return suggestions
    
    def _generate_transparency_label(self, origin: ContentOrigin) -> str:
        """Generate EU AI Act compliant transparency label"""
        labels = {
            ContentOrigin.AI_GENERATED: "AI-generated content",
            ContentOrigin.AI_ASSISTED: "AI-assisted content",
            ContentOrigin.AI_EDITED: "AI-edited content",
            ContentOrigin.HUMAN_WRITTEN: "Human-written content"
        }
        return labels.get(origin, "Content origin unknown")
    
    def suggest_improvements(self, content: str, 
                           target_score: float = 0.75) -> Dict:
        """
        Suggest specific improvements to increase authenticity
        
        Args:
            content: Original content
            target_score: Target authenticity score
        
        Returns:
            Suggested improvements
        """
        current_score = self.score(content, "temp", ContentOrigin.AI_ASSISTED)
        
        if current_score.overall_score >= target_score:
            return {
                "status": "meets_target",
                "current_score": current_score.overall_score,
                "target_score": target_score,
                "suggestions": []
            }
        
        # Generate specific improvements
        improvements = []
        
        if current_score.dimensions["personal_voice"] < 0.5:
            improvements.append({
                "type": "add_personal_voice",
                "suggestion": "Add personal perspective",
                "example": "Start with 'I've noticed...' or 'In my experience...'"
            })
        
        if current_score.dimensions["vulnerability"] < 0.3:
            improvements.append({
                "type": "add_vulnerability",
                "suggestion": "Show vulnerability",
                "example": "Add 'Honestly,' or 'Not gonna lie,' before a key point"
            })
        
        if current_score.dimensions["ai_risk"] > 0.4:
            improvements.append({
                "type": "reduce_formality",
                "suggestion": "Remove formal transitions",
                "example": "Replace 'Furthermore' with 'Plus' or 'Also'"
            })
        
        return {
            "status": "needs_improvement",
            "current_score": current_score.overall_score,
            "target_score": target_score,
            "gap": target_score - current_score.overall_score,
            "suggestions": improvements
        }
    
    def batch_score(self, contents: List[Dict]) -> List[AuthenticityScore]:
        """Score multiple content items"""
        results = []
        for item in contents:
            result = self.score(
                content=item.get('content', ''),
                content_id=item.get('id', ''),
                origin=item.get('origin', ContentOrigin.AI_ASSISTED),
                author_type=item.get('author_type', 'individual')
            )
            results.append(result)
        return results
    
    def get_highest_authenticity(self, results: List[AuthenticityScore]) -> Optional[AuthenticityScore]:
        """Get highest authenticity score from batch"""
        if not results:
            return None
        return max(results, key=lambda r: r.overall_score)


# Example usage
if __name__ == "__main__":
    scorer = AuthenticityScorer()
    
    # Test content - AI-generated feel
    ai_feeling_content = """
    Furthermore, it is imperative to understand that artificial intelligence 
    represents a paradigm shift in how organizations operate. Consequently, 
    businesses must leverage these technologies to optimize their strategic 
    initiatives moving forward.
    """
    
    # Test content - authentic feel
    authentic_content = """
    Here's what nobody tells you about AI.
    
    I've been working with these tools for 2 years now, and honestly? 
    Most companies are doing it wrong.
    
    They're trying to automate everything at once. 
    But here's what actually works...
    
    Start with ONE thing. Master it. Then scale.
    
    What's your experience been like?
    """
    
    print("=" * 60)
    print("AUTHENTICITY SCORING COMPARISON")
    print("=" * 60)
    
    # Score AI-feeling content
    result1 = scorer.score(ai_feeling_content, "ai_example", ContentOrigin.AI_GENERATED)
    print("\nAI-FEELING CONTENT:")
    print(f"Score: {result1.overall_score:.2f} ({result1.level.value})")
    print(f"Red flags: {result1.red_flags}")
    print(f"Transparency required: {result1.transparency_required}")
    print(f"Label: {result1.transparency_label}")
    
    # Score authentic content
    result2 = scorer.score(authentic_content, "authentic_example", ContentOrigin.AI_ASSISTED)
    print("\nAUTHENTIC CONTENT:")
    print(f"Score: {result2.overall_score:.2f} ({result2.level.value})")
    print(f"Strengths: {result2.strengths}")
    print(f"Suggestions: {result2.suggestions}")
    print(f"Transparency required: {result2.transparency_required}")
    print(f"Label: {result2.transparency_label}")
    
    print("\n" + "=" * 60)
    print("DETAILED DIMENSIONS (Authentic Content):")
    print("=" * 60)
    for dim, score in result2.dimensions.items():
        print(f"{dim}: {score:.2f}")
