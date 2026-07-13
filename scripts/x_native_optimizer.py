#!/usr/bin/env python3
"""
x_native_optimizer.py
X/Twitter Algorithm-Native Content Optimizer
Based on 2025-2026 X Algorithm Research

Features:
- Reply-first strategy (13.5x weighted engagement)
- Video content prioritization
- Link placement optimization (replies vs main tweet)
- Hashtag strategy (minimal use, semantic focus)
- First-30-minutes engagement velocity tracking
- Algorithm-friendly formatting
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


class ContentType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    POLL = "poll"
    THREAD = "thread"


class OptimizationPriority(Enum):
    REPLIES = "replies"        # 13.5x weight
    RETWEETS = "retweets"      # 20x weight
    BOOKMARKS = "bookmarks"    # 10x weight
    LIKES = "likes"            # 1x weight


@dataclass
class XOptimizationResult:
    """Result of X-specific optimization"""
    original_content: str
    optimized_content: str
    content_type: str
    optimization_score: float
    recommendations: List[str]
    reply_hook: Optional[str]
    main_tweet: str
    reply_tweets: List[str]
    best_posting_time: str
    estimated_engagement: float
    algorithm_notes: List[str]
    optimized_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "original_content": self.original_content,
            "optimized_content": self.optimized_content,
            "content_type": self.content_type,
            "optimization_score": self.optimization_score,
            "recommendations": self.recommendations,
            "reply_hook": self.reply_hook,
            "main_tweet": self.main_tweet,
            "reply_tweets": self.reply_tweets,
            "best_posting_time": self.best_posting_time,
            "estimated_engagement": self.estimated_engagement,
            "algorithm_notes": self.algorithm_notes,
            "optimized_at": self.optimized_at
        }


class XNativeOptimizer:
    """
    X/Twitter algorithm-native content optimizer
    Implements 2026 algorithm insights
    """
    
    # X Algorithm weights (from research)
    ALGORITHM_WEIGHTS = {
        "replies": 13.5,
        "retweets": 20.0,
        "bookmarks": 10.0,
        "likes": 1.0
    }
    
    # Optimal posting times (based on research - 5PM peak)
    OPTIMAL_HOURS = [9, 12, 17, 19]  # 9AM, 12PM, 5PM, 7PM
    
    # Content type priority (video > image > text)
    CONTENT_PRIORITY = {
        "video": 1.0,
        "image": 0.7,
        "text": 0.4,
        "poll": 0.6
    }
    
    # Engagement hook phrases
    REPLY_HOOKS = [
        "What do you think?",
        "Agree or disagree?",
        "Thoughts?",
        "What's your take?",
        "Have you experienced this?",
        "Drop your opinion below",
        "Convince me I'm wrong",
        "What's your biggest lesson?",
        "Which side are you on?",
        "Am I missing something?"
    ]
    
    def __init__(self, timezone: str = "Europe/Paris"):
        self.timezone = timezone
        self.optimization_history: List[XOptimizationResult] = []
        logger.info("XNativeOptimizer initialized")
    
    def optimize(self, content: str, 
                content_type: ContentType = ContentType.TEXT,
                has_media: bool = False,
                media_type: Optional[str] = None,
                include_link: Optional[str] = None,
                target_audience: Optional[str] = None) -> XOptimizationResult:
        """
        Optimize content for X/Twitter algorithm
        
        Args:
            content: Original content
            content_type: Type of content
            has_media: Whether content includes media
            media_type: Type of media (video, image, gif)
            include_link: URL to include (will be placed in reply)
            target_audience: Target audience segment
        
        Returns:
            XOptimizationResult with optimized content
        """
        logger.info(f"Optimizing content for X: {content[:50]}...")
        
        recommendations = []
        algorithm_notes = []
        
        # Step 1: Analyze original content
        analysis = self._analyze_content(content)
        
        # Step 2: Generate reply hook (13.5x weight strategy)
        reply_hook = self._generate_reply_hook(content, analysis)
        
        # Step 3: Structure main tweet
        main_tweet, reply_tweets = self._structure_tweets(
            content, reply_hook, include_link, analysis
        )
        
        # Step 4: Apply algorithm optimizations
        optimized = self._apply_optimizations(main_tweet, content_type, has_media, media_type)
        
        # Step 5: Calculate optimization score
        score = self._calculate_optimization_score(
            optimized, content_type, has_media, reply_hook
        )
        
        # Step 6: Generate recommendations
        recommendations = self._generate_recommendations(
            analysis, content_type, has_media, score
        )
        
        # Step 7: Estimate engagement
        estimated_engagement = self._estimate_engagement(score, content_type)
        
        # Step 8: Determine best posting time
        best_time = self._determine_best_posting_time()
        
        result = XOptimizationResult(
            original_content=content,
            optimized_content=optimized,
            content_type=content_type.value,
            optimization_score=score,
            recommendations=recommendations,
            reply_hook=reply_hook,
            main_tweet=main_tweet,
            reply_tweets=reply_tweets,
            best_posting_time=best_time,
            estimated_engagement=estimated_engagement,
            algorithm_notes=algorithm_notes
        )
        
        self.optimization_history.append(result)
        logger.info(f"Optimization complete: {score:.2f}/1.0")
        
        return result
    
    def _analyze_content(self, content: str) -> Dict:
        """Analyze content structure and elements"""
        return {
            "length": len(content),
            "word_count": len(content.split()),
            "has_numbers": bool(re.search(r'\d+%?|\$?\d+[KMB]?', content)),
            "has_question": '?' in content,
            "has_hook": any(term in content.lower() for term in 
                          ['here\'s why', 'the truth', 'unpopular opinion', 'nobody']),
            "has_cta": any(term in content.lower() for term in 
                         ['follow', 'share', 'retweet', 'like']),
            "has_hashtags": '#' in content,
            "has_url": 'http' in content.lower() or 'www.' in content.lower(),
            "sentence_count": len([s for s in content.split('.') if s.strip()]),
            "avg_sentence_length": len(content.split()) / max(len(content.split('.')), 1)
        }
    
    def _generate_reply_hook(self, content: str, analysis: Dict) -> str:
        """Generate reply hook based on content (13.5x strategy)"""
        
        # If content already has question, use it as hook
        if analysis["has_question"]:
            return None  # Already has engagement hook
        
        # Select appropriate hook based on content type
        if analysis["has_numbers"]:
            return "Does this number surprise you?"
        
        if "unpopular opinion" in content.lower() or "contrarian" in content.lower():
            return "Agree or disagree?"
        
        if analysis["has_hook"]:
            return "What do you think?"
        
        # Default hook
        return "Thoughts?"
    
    def _structure_tweets(self, content: str, reply_hook: Optional[str],
                          link: Optional[str], analysis: Dict) -> Tuple[str, List[str]]:
        """
        Structure content into main tweet + replies
        X algorithm: links penalized in main tweet
        """
        main = content.strip()
        replies = []
        
        # Remove hashtags from main tweet (minimal impact, can trigger spam filters)
        if analysis["has_hashtags"]:
            main = re.sub(r'#\w+', '', main).strip()
        
        # If content is too long, create thread
        if len(main) > 280:
            # Split into thread
            parts = self._split_into_thread(main)
            main = parts[0]
            replies = parts[1:]
        
        # Add reply hook to main tweet if not already present
        if reply_hook and reply_hook not in main:
            # Check if we can fit hook
            if len(main) + len(reply_hook) + 2 <= 280:
                main = f"{main}\n\n{reply_hook}"
        
        # Move link to first reply (algorithm-friendly)
        if link:
            link_reply = f"{link}\n\n[Link for those interested 👆]"
            replies.insert(0, link_reply)
            # Remove link from main
            main = re.sub(r'https?://\S+', '', main).strip()
        
        return main, replies
    
    def _split_into_thread(self, content: str, max_length: int = 270) -> List[str]:
        """Split long content into thread-friendly parts"""
        parts = []
        sentences = content.split('.')
        current_part = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            test_part = current_part + sentence + ". "
            
            if len(test_part) > max_length:
                if current_part:
                    parts.append(current_part.strip())
                current_part = sentence + ". "
            else:
                current_part = test_part
        
        if current_part:
            parts.append(current_part.strip())
        
        return parts
    
    def _apply_optimizations(self, content: str, content_type: ContentType,
                            has_media: bool, media_type: Optional[str]) -> str:
        """Apply algorithm-friendly formatting"""
        optimized = content
        
        # Ensure optimal length (100-280 chars ideal)
        if len(optimized) < 100:
            # Too short - might not provide enough value
            pass  # Keep as-is, brevity can work
        
        # Add line breaks for readability
        if '\n' not in optimized and len(optimized) > 150:
            # Split long sentences with line breaks
            optimized = self._add_line_breaks(optimized)
        
        # Emoji optimization (can increase engagement)
        # But don't overdo it (max 2-3 emojis)
        
        return optimized
    
    def _add_line_breaks(self, content: str) -> str:
        """Add strategic line breaks for readability"""
        # Break after periods in long content
        sentences = content.split('. ')
        if len(sentences) > 2:
            # Group into readable chunks
            chunks = []
            current = ""
            for i, sentence in enumerate(sentences):
                current += sentence
                if i < len(sentences) - 1:
                    current += "."
                if len(current) > 80 or i == len(sentences) - 1:
                    chunks.append(current.strip())
                    current = ""
            return "\n\n".join(chunks)
        return content
    
    def _calculate_optimization_score(self, content: str, 
                                     content_type: ContentType,
                                     has_media: bool,
                                     reply_hook: Optional[str]) -> float:
        """Calculate overall optimization score"""
        score = 0.0
        
        # Content type bonus (video highest)
        if content_type == ContentType.VIDEO:
            score += 0.25
        elif content_type == ContentType.IMAGE:
            score += 0.15
        elif has_media:
            score += 0.10
        
        # Reply hook bonus (13.5x weight strategy)
        if reply_hook:
            score += 0.20
        elif '?' in content:
            score += 0.15
        
        # Optimal length
        if 100 <= len(content) <= 280:
            score += 0.15
        elif len(content) <= 280:
            score += 0.10
        
        # No link in main tweet (algorithm-friendly)
        if 'http' not in content:
            score += 0.15
        
        # No excessive hashtags
        if content.count('#') <= 2:
            score += 0.10
        
        # Engagement elements
        if any(term in content.lower() for term in ['here\'s', 'thread', '🧵']):
            score += 0.10
        
        return min(1.0, score)
    
    def _generate_recommendations(self, analysis: Dict, content_type: ContentType,
                                  has_media: bool, score: float) -> List[str]:
        """Generate optimization recommendations"""
        recs = []
        
        if score < 0.7:
            recs.append("Consider adding a reply hook (13.5x engagement weight)")
        
        if not has_media and content_type == ContentType.TEXT:
            recs.append("Add visual media - videos prioritized in 'For You' feed")
        
        if analysis["has_url"]:
            recs.append("Move link to first reply - links penalized in main tweet")
        
        if analysis["has_hashtags"]:
            recs.append("Minimize hashtags - semantic NLP categorizes content automatically")
        
        if analysis["length"] > 280:
            recs.append("Content exceeds 280 chars - consider thread format")
        
        if not analysis["has_numbers"]:
            recs.append("Add data/numbers (+35% engagement according to research)")
        
        if not analysis["has_hook"]:
            recs.append("Add strong hook - 'Here's why', 'The truth about', etc.")
        
        return recs
    
    def _estimate_engagement(self, score: float, content_type: ContentType) -> float:
        """Estimate engagement based on optimization score"""
        base_engagement = score * 100
        
        # Content type multiplier
        multipliers = {
            ContentType.VIDEO: 2.0,
            ContentType.IMAGE: 1.5,
            ContentType.POLL: 1.3,
            ContentType.TEXT: 1.0,
            ContentType.THREAD: 1.8
        }
        
        multiplier = multipliers.get(content_type, 1.0)
        return base_engagement * multiplier
    
    def _determine_best_posting_time(self) -> str:
        """Determine optimal posting time based on audience"""
        now = datetime.now()
        
        # Check if we're near an optimal hour
        current_hour = now.hour
        
        if current_hour in self.OPTIMAL_HOURS:
            return f"Now ({current_hour}:00) is optimal"
        
        # Find next optimal time
        for hour in self.OPTIMAL_HOURS:
            if hour > current_hour:
                return f"{hour}:00 today"
        
        return f"{self.OPTIMAL_HOURS[0]}:00 tomorrow"
    
    def batch_optimize(self, contents: List[Dict]) -> List[XOptimizationResult]:
        """Optimize multiple content items"""
        results = []
        for item in contents:
            result = self.optimize(
                content=item.get('content', ''),
                content_type=ContentType(item.get('type', 'text')),
                has_media=item.get('has_media', False),
                media_type=item.get('media_type'),
                include_link=item.get('link')
            )
            results.append(result)
        return results
    
    def get_best_performer(self, results: List[XOptimizationResult]) -> Optional[XOptimizationResult]:
        """Get the highest-scoring content"""
        if not results:
            return None
        return max(results, key=lambda r: r.optimization_score)


# Example usage
if __name__ == "__main__":
    optimizer = XNativeOptimizer()
    
    # Test content
    test_content = """
    AI agents are transforming how we work.
    
    The key insight from 2026 research:
    Multi-agent systems with clear contracts outperform single mega-agents by 3x.
    
    Start with one workflow. Master it. Scale.
    
    https://research.example.com/ai-agents-2026
    """
    
    # Optimize
    result = optimizer.optimize(
        content=test_content,
        content_type=ContentType.TEXT,
        has_media=False,
        include_link="https://research.example.com/ai-agents-2026"
    )
    
    print("=" * 60)
    print("X NATIVE OPTIMIZATION RESULT")
    print("=" * 60)
    print(json.dumps(result.to_dict(), indent=2))
