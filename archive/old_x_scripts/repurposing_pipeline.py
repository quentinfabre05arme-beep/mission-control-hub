"""
Social Media Operations System - Repurposing Pipeline
Phase 5: Multi-Platform Content Adaptation

Workflow: Single Input → Platform Adaptation → Parallel Prep → Approval Gate → Scheduled Publishing
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

sys.stdout.reconfigure(encoding='utf-8')

class Platform(Enum):
    X = "x"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    LINKEDIN = "linkedin"
    NEWSLETTER = "newsletter"

class ContentFormat(Enum):
    THREAD = "thread"
    SINGLE = "single"
    CAROUSEL = "carousel"
    VIDEO = "video"
    STORY = "story"
    ARTICLE = "article"

@dataclass
class PlatformAdaptation:
    """Content adapted for a specific platform"""
    platform: Platform
    format: ContentFormat
    content: str
    media: List[str]
    character_count: int
    hashtags: List[str]
    optimized_for: str  # engagement, reach, conversion
    ready: bool = False

@dataclass
class RepurposingJob:
    """A multi-platform repurposing job"""
    id: str
    source_id: str
    source_content: str
    source_type: str
    adaptations: Dict[str, PlatformAdaptation]
    status: str  # pending, adapting, ready, approved, published
    created_at: str
    scheduled_times: Dict[str, str] = field(default_factory=dict)

class RepurposingPipeline:
    """
    Multi-Platform Repurposing Pipeline
    
    Takes single input, adapts for each platform, queues for approval
    """
    
    def __init__(self, workspace_path: str = None):
        self.workspace = Path(workspace_path) if workspace_path else Path(__file__).parent
        self.jobs_file = self.workspace / "operations" / "repurposing_jobs.json"
        self.templates_file = self.workspace / "operations" / "platform_templates.json"
        
        self.jobs_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.jobs: Dict[str, RepurposingJob] = {}
        self.templates: Dict[str, Dict] = self._load_templates()
        
        self._load_jobs()
    
    def _load_templates(self) -> Dict:
        """Load platform-specific adaptation templates"""
        default_templates = {
            "x_thread": {
                "max_length": 280,
                "hashtag_count": 3,
                "tone": "analytical",
                "structure": "hook → thread",
                "best_time": "8-10am ET",
                "cta_options": ["What do you think?", "Agree or disagree?", "Thoughts?"]
            },
            "x_single": {
                "max_length": 280,
                "hashtag_count": 3,
                "tone": "concise",
                "structure": "insight + data",
                "best_time": "12-2pm ET",
                "cta_options": ["Drop a comment", "Thoughts?", "DM for details"]
            },
            "instagram_carousel": {
                "slides": "5-10",
                "slide_structure": "hook slide → point slides → CTA slide",
                "caption_length": 2200,
                "hashtag_count": 10,
                "tone": "visual + educational",
                "best_time": "6-9pm ET",
                "image_ratio": "4:5"
            },
            "instagram_story": {
                "slides": "3-5",
                "interactive": "polls, questions, sliders",
                "hashtag_stickers": True,
                "tone": "casual, behind-scenes",
                "best_time": "morning 8-10am, evening 7-9pm"
            },
            "youtube_shorts": {
                "duration": "30-60s",
                "hook": "first 3 seconds critical",
                "structure": "hook → insight → CTA",
                "caption_length": 100,
                "tone": "fast-paced, high energy"
            },
            "linkedin_article": {
                "length": "500-1000 words",
                "structure": "insight → data → analysis → conclusion",
                "hashtag_count": 5,
                "tone": "professional, authoritative",
                "best_time": "Tuesday-Thursday 8-10am",
                "cta_options": ["What's your take?", "Share your experience", "Comment below"]
            },
            "newsletter": {
                "length": "500-800 words",
                "structure": "subject line → hook → body → CTA",
                "sections": "intro, main point, supporting data, conclusion",
                "tone": "conversational, valuable",
                "best_day": "Tuesday or Thursday"
            }
        }
        
        if self.templates_file.exists():
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return {**default_templates, **json.load(f)}
        
        with open(self.templates_file, 'w', encoding='utf-8') as f:
            json.dump(default_templates, f, indent=2, ensure_ascii=False)
        
        return default_templates
    
    def _load_jobs(self):
        """Load repurposing jobs from disk"""
        if self.jobs_file.exists():
            with open(self.jobs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for job_id, job_data in data.items():
                    job_data['adaptations'] = {
                        k: PlatformAdaptation(**v) for k, v in job_data['adaptations'].items()
                    }
                    self.jobs[job_id] = RepurposingJob(**job_data)
    
    def _save_jobs(self):
        """Save repurposing jobs to disk"""
        data = {}
        for job_id, job in self.jobs.items():
            data[job_id] = {
                "id": job.id,
                "source_id": job.source_id,
                "source_content": job.source_content,
                "source_type": job.source_type,
                "adaptations": {
                    k: {
                        "platform": v.platform.value,
                        "format": v.format.value,
                        "content": v.content,
                        "media": v.media,
                        "character_count": v.character_count,
                        "hashtags": v.hashtags,
                        "optimized_for": v.optimized_for,
                        "ready": v.ready
                    }
                    for k, v in job.adaptations.items()
                },
                "status": job.status,
                "created_at": job.created_at,
                "scheduled_times": job.scheduled_times
            }
        
        with open(self.jobs_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_repurposing_job(self, source_id: str, source_content: str,
                              source_type: str, target_platforms: List[Platform] = None) -> RepurposingJob:
        """
        Create a repurposing job for multiple platforms
        """
        if target_platforms is None:
            target_platforms = [Platform.X, Platform.INSTAGRAM, Platform.LINKEDIN]
        
        job_id = f"repurpose_{self._slugify(source_id)}_{int(datetime.now().timestamp())}"
        
        job = RepurposingJob(
            id=job_id,
            source_id=source_id,
            source_content=source_content,
            source_type=source_type,
            adaptations={},
            status="pending",
            created_at=datetime.now().isoformat()
        )
        
        # Create adaptations for each platform
        for platform in target_platforms:
            adaptation = self._adapt_for_platform(source_content, source_type, platform)
            job.adaptations[platform.value] = adaptation
        
        job.status = "ready"
        self.jobs[job_id] = job
        self._save_jobs()
        
        print(f"[REPURPOSING] Job created: {job_id} for {len(target_platforms)} platforms")
        return job
    
    def _adapt_for_platform(self, content: str, content_type: str, 
                           platform: Platform) -> PlatformAdaptation:
        """Adapt content for a specific platform"""
        
        if platform == Platform.X:
            if content_type == "thread":
                return self._adapt_x_thread(content)
            else:
                return self._adapt_x_single(content)
        
        elif platform == Platform.INSTAGRAM:
            return self._adapt_instagram_carousel(content)
        
        elif platform == Platform.LINKEDIN:
            return self._adapt_linkedin_article(content)
        
        elif platform == Platform.NEWSLETTER:
            return self._adapt_newsletter(content)
        
        else:
            # Generic adaptation
            return PlatformAdaptation(
                platform=platform,
                format=ContentFormat.SINGLE,
                content=content[:280],
                media=[],
                character_count=len(content[:280]),
                hashtags=[],
                optimized_for="reach",
                ready=True
            )
    
    def _adapt_x_thread(self, content: str) -> PlatformAdaptation:
        """Adapt content to X thread format"""
        template = self.templates.get("x_thread", {})
        
        # Extract hook (first sentence)
        hook = content.split('.')[0] + "."
        if len(hook) > 280:
            hook = hook[:277] + "..."
        
        # Create thread structure
        posts = self._chunk_content(content, 280)
        thread_content = hook + "\n\n🧵" + "".join([f"\n\n[{i+1}/{len(posts)}]\n{post}" for i, post in enumerate(posts)])
        
        return PlatformAdaptation(
            platform=Platform.X,
            format=ContentFormat.THREAD,
            content=thread_content,
            media=[],
            character_count=len(thread_content),
            hashtags=["#ETH", "#Treasury", "#Crypto"],
            optimized_for="engagement",
            ready=True
        )
    
    def _adapt_x_single(self, content: str) -> PlatformAdaptation:
        """Adapt content to X single post format"""
        # Extract key insight, truncate to 280 chars
        single = content[:277] + "..." if len(content) > 280 else content
        
        return PlatformAdaptation(
            platform=Platform.X,
            format=ContentFormat.SINGLE,
            content=single,
            media=[],
            character_count=len(single),
            hashtags=["#ETH", "#Crypto"],
            optimized_for="reach",
            ready=True
        )
    
    def _adapt_instagram_carousel(self, content: str) -> PlatformAdaptation:
        """Adapt content to Instagram carousel format"""
        template = self.templates.get("instagram_carousel", {})
        
        # Create slide structure
        slides = self._create_carousel_slides(content)
        
        carousel_content = f"""📊 CAROUSEL STRUCTURE:

Slide 1 (Hook): {slides['hook']}

Slides 2-{len(slides['points'])+1}:
"""
        for i, point in enumerate(slides['points'], 1):
            carousel_content += f"\nSlide {i+1}: {point[:100]}..."
        
        carousel_content += f"\n\nLast Slide (CTA): {slides['cta']}"
        
        return PlatformAdaptation(
            platform=Platform.INSTAGRAM,
            format=ContentFormat.CAROUSEL,
            content=carousel_content,
            media=["image_1.png", "image_2.png", "..."],  # Placeholder
            character_count=len(carousel_content),
            hashtags=["#investing", "#crypto", "#finance", "#money", "#wealth"],
            optimized_for="reach",
            ready=True
        )
    
    def _adapt_linkedin_article(self, content: str) -> PlatformAdaptation:
        """Adapt content to LinkedIn article format"""
        # Expand with professional context
        article = f"""The Strategic Shift to Productive Treasury Assets

In recent months, we've seen a significant evolution in how corporations approach balance sheet management...

{content}

Key implications for CFOs:
1. Yield generation changes the holding cost equation
2. Staking provides operational flexibility
3. Early adoption offers narrative positioning

What's your view on productive treasury strategies?

#finance #treasury #crypto #investment"""
        
        return PlatformAdaptation(
            platform=Platform.LINKEDIN,
            format=ContentFormat.ARTICLE,
            content=article,
            media=[],
            character_count=len(article),
            hashtags=["#finance", "#treasury", "#crypto"],
            optimized_for="authority",
            ready=True
        )
    
    def _adapt_newsletter(self, content: str) -> PlatformAdaptation:
        """Adapt content to newsletter format"""
        newsletter = f"""Subject: The treasury playbook is evolving...

Hey [Name],

Quick insight from the markets today:

{content}

This matters because:
• Early movers get positioning advantage
• Yield changes the CFO math entirely
• Infrastructure is being built now

Worth watching: The 19 companies already holding ETH treasuries.

To alpha,
[Name]

P.S. — Reply with your thoughts. I read every email."""
        
        return PlatformAdaptation(
            platform=Platform.NEWSLETTER,
            format=ContentFormat.ARTICLE,
            content=newsletter,
            media=[],
            character_count=len(newsletter),
            hashtags=[],
            optimized_for="conversion",
            ready=True
        )
    
    def _chunk_content(self, content: str, max_length: int) -> List[str]:
        """Chunk content into segments of max_length"""
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', content)
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_length:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _create_carousel_slides(self, content: str) -> Dict:
        """Create Instagram carousel slide structure"""
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        return {
            "hook": sentences[0] if sentences else "Key insight:",
            "points": sentences[1:5] if len(sentences) > 1 else ["Supporting point 1", "Supporting point 2"],
            "cta": "Follow for more insights →"
        }
    
    def _slugify(self, text: str) -> str:
        """Convert text to slug"""
        return re.sub(r'[^\w\s-]', '', text).strip().lower().replace(' ', '_')[:30]
    
    def get_adaptation_summary(self, job_id: str) -> Dict:
        """Get summary of adaptations for a job"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        
        summary = {
            "job_id": job_id,
            "source": job.source_id,
            "status": job.status,
            "platforms": {}
        }
        
        for platform, adaptation in job.adaptations.items():
            summary["platforms"][platform] = {
                "format": adaptation.format.value,
                "character_count": adaptation.character_count,
                "optimized_for": adaptation.optimized_for,
                "ready": adaptation.ready,
                "preview": adaptation.content[:100] + "..."
            }
        
        return summary
    
    def approve_platform(self, job_id: str, platform: str):
        """Approve a specific platform adaptation"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        if platform in job.adaptations:
            job.adaptations[platform].ready = True
            self._save_jobs()
            print(f"[REPURPOSING] Approved {platform} for {job_id}")

if __name__ == "__main__":
    # Test repurposing pipeline
    pipeline = RepurposingPipeline("C:\\Users\\quent\\.openclaw\\workspace")
    
    # Create repurposing job
    test_content = """The BTC treasury playbook is proven. The next evolution is earning yield while holding — that's where ETH treasuries come in. 3-4% staking APR changes the math for CFOs. 19 public companies now hold ETH ($13B+). The treasury strategy is evolving from passive holding to productive assets."""
    
    job = pipeline.create_repurposing_job(
        source_id="eth_treasury_thread",
        source_content=test_content,
        source_type="thread",
        target_platforms=[Platform.X, Platform.INSTAGRAM, Platform.LINKEDIN, Platform.NEWSLETTER]
    )
    
    # Get summary
    summary = pipeline.get_adaptation_summary(job.id)
    
    print("\n" + "="*70)
    print("MULTI-PLATFORM REPURPOSING SUMMARY")
    print("="*70)
    print(f"Job ID: {summary['job_id']}")
    print(f"Source: {summary['source']}")
    print(f"Status: {summary['status']}")
    print("\nPlatform Adaptations:")
    
    for platform, details in summary['platforms'].items():
        print(f"\n  📱 {platform.upper()}")
        print(f"     Format: {details['format']}")
        print(f"     Length: {details['character_count']} chars")
        print(f"     Optimized for: {details['optimized_for']}")
        print(f"     Preview: {details['preview']}")
    
    print("="*70)
    print("\nStatus: READY FOR APPROVAL")
    print("Action: Review each platform adaptation and approve for scheduling")
