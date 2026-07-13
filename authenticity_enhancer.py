#!/usr/bin/env python3
"""
Authenticity Enhancer v1.0
Human voice detection, authenticity scoring, and transparency markers
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter


class AuthenticityEnhancer:
    """
    Enhances content with authentic human voice characteristics.
    Provides transparency markers for AI-generated content.
    """
    
    # Patterns that indicate AI-generated content
    AI_PATTERNS = {
        "corporate_buzzwords": [
            "leverage", "synergy", "paradigm", "innovative", "disruptive",
            "scalable", "streamline", "optimize", "maximize", "strategic"
        ],
        "ai_tells": [
            "delve", "intricate", "multifaceted", "underscores", "highlights",
            "furthermore", "moreover", "in conclusion", "to summarize",
            "it is important to note", "as we have seen", "in essence"
        ],
        "overly_formal": [
            "therefore", "thus", "hence", "consequently", "accordingly",
            "nevertheless", "nonetheless", "however", "furthermore", "moreover"
        ],
        "generic_openers": [
            "in the world of", "in today's", "in an era of", "in recent years",
            "with the rise of", "as we know", "it is well known that"
        ],
        "polished_perfection": [
            "flawless", "seamless", "perfect", "ideal", "ultimate", "optimal"
        ]
    }
    
    # Patterns that indicate authentic human voice
    HUMAN_PATTERNS = {
        "imperfections": [
            "honestly", "frankly", "to be honest", "not gonna lie",
            "confession", "I think", "in my opinion", "I feel like"
        ],
        "casual_language": [
            "gonna", "wanna", "kinda", "sorta", "yeah", "nah", "yep",
            "tbh", "imo", "ngl", "tbf"
        ],
        "personal_experience": [
            "I remember", "I noticed", "I saw", "I heard", "I learned",
            "last week", "the other day", "recently", "last year"
        ],
        "emotional_markers": [
            "excited", "worried", "confused", "surprised", "shocked",
            "honestly", "actually", "seriously", "literally"
        ],
        "imperfect_grammar": [
            "...", "—", "!", "??", "?!", "lol", "haha"
        ],
        "raw_photos": [
            "candid", "unfiltered", "raw", "behind the scenes", "real talk"
        ]
    }
    
    def __init__(self):
        self.transparency_template = self._load_transparency_template()
        
    def score_authenticity(self, content: str) -> Dict[str, Any]:
        """
        Score content authenticity on multiple dimensions.
        Returns detailed breakdown.
        """
        text_lower = content.lower()
        
        scores = {
            "ai_indicators": self._score_ai_indicators(text_lower),
            "human_voice": self._score_human_voice(text_lower),
            "vulnerability": self._score_vulnerability(text_lower),
            "conversational_tone": self._score_conversational_tone(text_lower),
            "personal_connection": self._score_personal_connection(text_lower),
            "raw_imperfection": self._score_raw_imperfection(text_lower)
        }
        
        # Calculate weighted total
        weights = {
            "ai_indicators": -0.3,  # Negative weight - lower is better
            "human_voice": 0.25,
            "vulnerability": 0.2,
            "conversational_tone": 0.15,
            "personal_connection": 0.15,
            "raw_imperfection": 0.15
        }
        
        total = 0.5  # Base score
        for dimension, score in scores.items():
            if dimension == "ai_indicators":
                total += score * weights[dimension]
            else:
                total += score * weights[dimension]
        
        total = max(0, min(1, total))
        
        return {
            "total_score": round(total, 2),
            "dimension_scores": {k: round(v, 2) for k, v in scores.items()},
            "classification": self._classify_authenticity(total),
            "improvements": self._suggest_improvements(scores)
        }
    
    def enhance_authenticity(self, content: str, target_score: float = 0.7) -> Dict[str, Any]:
        """
        Enhance content to sound more authentic.
        """
        original_score = self.score_authenticity(content)
        
        if original_score["total_score"] >= target_score:
            return {
                "original_content": content,
                "enhanced_content": content,
                "original_score": original_score["total_score"],
                "enhanced_score": original_score["total_score"],
                "changes_made": [],
                "message": "Content already meets authenticity target"
            }
        
        enhanced = content
        changes = []
        
        # Remove AI tells
        for ai_tell in self.AI_PATTERNS["ai_tells"]:
            if ai_tell in enhanced.lower():
                replacement = self._replace_ai_tell(ai_tell)
                enhanced = enhanced.replace(ai_tell, replacement)
                changes.append({
                    "type": "removed_ai_tell",
                    "original": ai_tell,
                    "replacement": replacement
                })
        
        # Remove generic openers
        for opener in self.AI_PATTERNS["generic_openers"]:
            if enhanced.lower().startswith(opener):
                enhanced = enhanced[len(opener):].strip()
                if enhanced[0].islower():
                    enhanced = enhanced[0].upper() + enhanced[1:]
                changes.append({
                    "type": "removed_generic_opener",
                    "original": opener
                })
        
        # Add human touches
        if original_score["dimension_scores"]["human_voice"] < 0.3:
            enhanced = self._add_casual_touch(enhanced)
            changes.append({"type": "added_casual_touch"})
        
        if original_score["dimension_scores"]["personal_connection"] < 0.3:
            enhanced = self._add_personal_connection(enhanced)
            changes.append({"type": "added_personal_element"})
        
        if original_score["dimension_scores"]["vulnerability"] < 0.3:
            enhanced = self._add_vulnerability(enhanced)
            changes.append({"type": "added_vulnerability"})
        
        # Score enhanced content
        enhanced_score = self.score_authenticity(enhanced)
        
        return {
            "original_content": content,
            "enhanced_content": enhanced,
            "original_score": original_score["total_score"],
            "enhanced_score": enhanced_score["total_score"],
            "target_score": target_score,
            "changes_made": changes,
            "improvement": round(enhanced_score["total_score"] - original_score["total_score"], 2)
        }
    
    def add_transparency_marker(self, content: str, 
                                 ai_involvement: str = "generated",
                                 human_review: bool = True) -> Dict[str, str]:
        """
        Add transparency markers to AI-generated content.
        Compliant with EU AI Act requirements.
        """
        markers = {
            "generated": "🤖 AI-generated",
            "assisted": "🤝 AI-assisted",
            "edited": "✏️ AI-edited",
            "researched": "🔍 AI-researched"
        }
        
        marker = markers.get(ai_involvement, markers["generated"])
        
        if human_review:
            marker += " • Human-reviewed ✓"
        
        # Build transparency disclosure
        transparency = f"{marker}\n\n{content}"
        
        return {
            "marked_content": transparency,
            "marker": marker,
            "disclosure": f"This content was {ai_involvement} with AI assistance. "
                         f"{'Human review and approval was conducted.' if human_review else ''}"
        }
    
    def detect_human_voice(self, content_samples: List[str]) -> Dict[str, Any]:
        """
        Analyze content samples to extract human voice characteristics.
        """
        voice_profile = {
            "common_phrases": [],
            "vocabulary_range": 0,
            "sentence_patterns": [],
            "emotional_markers": [],
            "formality_level": 0,
            "recommended_style": ""
        }
        
        all_text = " ".join(content_samples).lower()
        words = re.findall(r'\b\w+\b', all_text)
        
        # Vocabulary range
        unique_words = set(words)
        voice_profile["vocabulary_range"] = len(unique_words)
        
        # Common phrases (2-3 words)
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        common_bigrams = Counter(bigrams).most_common(10)
        voice_profile["common_phrases"] = [bg[0] for bg in common_bigrams]
        
        # Emotional markers
        emotional_hits = [m for m in self.HUMAN_PATTERNS["emotional_markers"] 
                         if m in all_text]
        voice_profile["emotional_markers"] = emotional_hits[:5]
        
        # Formality level
        formal_words = sum(1 for w in words if w in self.AI_PATTERNS["overly_formal"])
        casual_words = sum(1 for w in words if w in self.HUMAN_PATTERNS["casual_language"])
        
        if formal_words > casual_words * 2:
            voice_profile["formality_level"] = 0.8
            voice_profile["recommended_style"] = "More formal - consider adding casual elements"
        elif casual_words > formal_words:
            voice_profile["formality_level"] = 0.3
            voice_profile["recommended_style"] = "Casual and authentic - maintain this style"
        else:
            voice_profile["formality_level"] = 0.5
            voice_profile["recommended_style"] = "Balanced - good mix of formal and casual"
        
        return voice_profile
    
    def suggest_raw_content(self, topic: str) -> List[Dict[str, str]]:
        """
        Suggest raw, unpolished content formats for maximum authenticity.
        """
        suggestions = [
            {
                "format": "Behind-the-scenes photo",
                "description": f"Unedited photo related to {topic} with candid caption",
                "authenticity_boost": "High - Shows real moments",
                "example": f"Just finished working on {topic}. Messy desk, cold coffee, but progress! ☕"
            },
            {
                "format": "Personal story",
                "description": f"Share personal experience related to {topic}",
                "authenticity_boost": "High - Vulnerability creates connection",
                "example": f"When I first started with {topic}, I made every mistake possible. Here's what I learned..."
            },
            {
                "format": "Unscripted video",
                "description": "Raw, unedited video thoughts on topic",
                "authenticity_boost": "Very High - Real voice and presence",
                "example": "*shaky phone camera* 'Quick thoughts while walking...'"
            },
            {
                "format": "Honest confession",
                "description": f"Admit something about {topic} that most people won't say",
                "authenticity_boost": "Very High - Contrarian honesty",
                "example": f"Unpopular opinion: {topic} is overrated. Here's why..."
            },
            {
                "format": "Mistake highlight",
                "description": "Share something that went wrong",
                "authenticity_boost": "High - Imperfection is relatable",
                "example": f"Failed attempt at {topic} #3 today. Learning in public."
            }
        ]
        
        return suggestions
    
    def _score_ai_indicators(self, text: str) -> float:
        """Score presence of AI-generated content indicators."""
        score = 1.0
        
        for category, patterns in self.AI_PATTERNS.items():
            for pattern in patterns:
                if pattern in text:
                    score -= 0.1
        
        # Penalize over-structured content
        if text.count("\n") > 5:
            score -= 0.1
        
        # Penalize perfect grammar (simplistic check)
        sentences = text.split(".")
        capitalized_ratio = sum(1 for s in sentences if s.strip() and s.strip()[0].isupper()) / max(len(sentences), 1)
        if capitalized_ratio > 0.95:
            score -= 0.1
        
        return max(0, score)
    
    def _score_human_voice(self, text: str) -> float:
        """Score human voice characteristics."""
        score = 0.3
        
        for category, patterns in self.HUMAN_PATTERNS.items():
            for pattern in patterns:
                if pattern in text:
                    score += 0.1
        
        return min(1.0, score)
    
    def _score_vulnerability(self, text: str) -> float:
        """Score vulnerability/imperfection markers."""
        score = 0.3
        
        vulnerability_markers = [
            "not sure", "don't know", "struggling", "learning", "failed",
            "mistake", "wrong", "confused", "honest", "admit"
        ]
        
        for marker in vulnerability_markers:
            if marker in text:
                score += 0.1
        
        return min(1.0, score)
    
    def _score_conversational_tone(self, text: str) -> float:
        """Score conversational tone."""
        score = 0.4
        
        # Check for direct address
        if "you" in text or "your" in text:
            score += 0.2
        
        # Check for questions
        if "?" in text:
            score += 0.15
        
        # Check for casual contractions
        contractions = ["don't", "can't", "won't", "I'm", "it's", "that's"]
        for contraction in contractions:
            if contraction in text:
                score += 0.05
        
        return min(1.0, score)
    
    def _score_personal_connection(self, text: str) -> float:
        """Score personal connection markers."""
        score = 0.3
        
        personal_markers = [
            "I ", "my ", "me ", "I've", "I'm", "myself",
            "we ", "our ", "us ", "we've"
        ]
        
        for marker in personal_markers:
            if marker in text:
                score += 0.08
        
        return min(1.0, score)
    
    def _score_raw_imperfection(self, text: str) -> float:
        """Score raw/imperfect elements."""
        score = 0.3
        
        # Ellipses (hesitation)
        if "..." in text:
            score += 0.15
        
        # Em dashes (interruption)
        if "—" in text or " - " in text:
            score += 0.1
        
        # Multiple punctuation (emphasis)
        if "!!" in text or "??" in text:
            score += 0.1
        
        # Informal expressions
        if any(expr in text for expr in ["lol", "haha", "ugh", "hmm"]):
            score += 0.15
        
        return min(1.0, score)
    
    def _classify_authenticity(self, score: float) -> str:
        """Classify authenticity score."""
        if score >= 0.7:
            return "Highly Authentic"
        elif score >= 0.5:
            return "Moderately Authentic"
        elif score >= 0.3:
            return "Somewhat Processed"
        else:
            return "Highly Processed/AI-like"
    
    def _suggest_improvements(self, scores: Dict[str, float]) -> List[Dict]:
        """Suggest improvements for low-scoring dimensions."""
        suggestions = []
        
        dimension_advice = {
            "ai_indicators": "Remove corporate jargon and AI tells",
            "human_voice": "Add casual language and personal expressions",
            "vulnerability": "Include honest admissions or learning moments",
            "conversational_tone": "Use 'you' and questions to engage reader",
            "personal_connection": "Share personal experiences and use 'I' statements",
            "raw_imperfection": "Allow natural hesitations and informal punctuation"
        }
        
        for dimension, score in scores.items():
            if score < 0.4:
                suggestions.append({
                    "dimension": dimension,
                    "current_score": round(score, 2),
                    "suggestion": dimension_advice.get(dimension, "Review and improve")
                })
        
        return suggestions
    
    def _replace_ai_tell(self, ai_tell: str) -> str:
        """Replace AI tell with human alternative."""
        replacements = {
            "delve": "explore",
            "intricate": "complex",
            "multifaceted": "complicated",
            "underscores": "shows",
            "highlights": "shows",
            "furthermore": "also",
            "moreover": "plus",
            "in conclusion": "so",
            "to summarize": "in short",
            "it is important to note": "note",
            "as we have seen": "as shown",
            "in essence": "basically"
        }
        return replacements.get(ai_tell, ai_tell)
    
    def _add_casual_touch(self, text: str) -> str:
        """Add casual language touch."""
        casual_additions = [
            "Honestly, ",
            "Not gonna lie, ",
            "Real talk: ",
            "TBH, "
        ]
        
        import random
        addition = random.choice(casual_additions)
        
        return addition + text[0].lower() + text[1:]
    
    def _add_personal_connection(self, text: str) -> str:
        """Add personal connection element."""
        personal_prefixes = [
            "I recently realized ",
            "From my experience, ",
            "I've noticed that ",
            "Something I've learned: "
        ]
        
        import random
        prefix = random.choice(personal_prefixes)
        
        return prefix + text[0].lower() + text[1:]
    
    def _add_vulnerability(self, text: str) -> str:
        """Add vulnerability element."""
        vulnerable_additions = [
            "\n\n(I'm still learning about this, so tell me if I'm missing something.)",
            "\n\n(This is just my take—I could be wrong.)",
            "\n\n(Still figuring this out, honestly.)"
        ]
        
        import random
        return text + random.choice(vulnerable_additions)
    
    def _load_transparency_template(self) -> str:
        """Load transparency disclosure template."""
        return """🤖 AI-{involvement} • Human-reviewed ✓

{content}

---
Transparency: This content was {involvement} with AI assistance and human oversight."""


def main():
    """Example usage of Authenticity Enhancer."""
    enhancer = AuthenticityEnhancer()
    
    # Example AI-generated content
    ai_content = """In the world of modern technology, it is important to note that 
    artificial intelligence is revolutionizing content creation. Furthermore, 
    leveraging these tools can maximize efficiency and streamline workflows.
    In conclusion, businesses should embrace this paradigm shift."""
    
    print("=" * 60)
    print("Authenticity Analysis")
    print("=" * 60)
    
    # Score original
    original_score = enhancer.score_authenticity(ai_content)
    print(f"\nOriginal Score: {original_score['total_score']}")
    print(f"Classification: {original_score['classification']}")
    print("\nDimension Scores:")
    for dim, score in original_score['dimension_scores'].items():
        print(f"  {dim}: {score}")
    
    # Enhance
    print("\n" + "=" * 60)
    print("Enhancement Results")
    print("=" * 60)
    
    enhancement = enhancer.enhance_authenticity(ai_content, target_score=0.7)
    print(f"\nOriginal Score: {enhancement['original_score']}")
    print(f"Enhanced Score: {enhancement['enhanced_score']}")
    print(f"Improvement: +{enhancement['improvement']}")
    
    print(f"\nOriginal:\n{enhancement['original_content']}")
    print(f"\nEnhanced:\n{enhancement['enhanced_content']}")
    
    # Add transparency
    print("\n" + "=" * 60)
    print("Transparency Markers")
    print("=" * 60)
    
    marked = enhancer.add_transparency_marker(
        enhancement['enhanced_content'],
        ai_involvement="assisted",
        human_review=True
    )
    print(f"\n{marked['marked_content']}")
    
    # Suggest raw content
    print("\n" + "=" * 60)
    print("Raw Content Suggestions")
    print("=" * 60)
    
    suggestions = enhancer.suggest_raw_content("AI content creation")
    for i, suggestion in enumerate(suggestions[:3], 1):
        print(f"\n{i}. {suggestion['format']}")
        print(f"   Authenticity boost: {suggestion['authenticity_boost']}")
        print(f"   Example: {suggestion['example']}")


if __name__ == "__main__":
    main()
