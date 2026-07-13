"""
Social Media Operations System - Content Pipeline
Phase 2: Content Operations Workflow

Workflow: Research/Monitor → Process/Transform → Draft → Approval → Execute → Log
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

sys.stdout.reconfigure(encoding='utf-8')

@dataclass
class ContentDraft:
    """Represents a piece of content ready for review"""
    id: str
    title: str
    content_type: str  # thread, single, reply, carousel
    platform: str
    body: str
    hooks: List[str]
    hashtags: List[str]
    character_count: int
    media: List[str]
    source_file: str
    created_at: str
    status: str  # draft, ready, approved, posted
    scheduled_time: Optional[str] = None

class ContentPipeline:
    """
    Content Operations Pipeline
    
    Reads drafts from markdown files, prepares for posting,
    queues for approval, executes via Zernio/X skills
    """
    
    def __init__(self, workspace_path: str = None):
        self.workspace = Path(workspace_path) if workspace_path else Path(__file__).parent
        self.content_dir = self.workspace / "Mission Control" / "Content"
        self.drafts_dir = self.content_dir / "drafts"
        self.queue_file = self.workspace / "operations" / "content_queue.json"
        self.templates_file = self.workspace / "operations" / "content_templates.json"
        
        # Ensure directories exist
        self.drafts_dir.mkdir(parents=True, exist_ok=True)
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.drafts: Dict[str, ContentDraft] = {}
        self.templates: Dict[str, Dict] = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load or create content templates"""
        default_templates = {
            "eth_treasury": {
                "hooks": [
                    "The BTC treasury playbook is proven. The next evolution is earning yield while holding.",
                    "19 public companies now hold ETH. The treasury revolution is just starting.",
                    "Saylor had to sell $216M BTC. ETH treasuries won't have to.",
                ],
                "hashtags": ["#ETH", "#Treasury", "#Crypto"],
                "tone": "analytical",
                "cta": "What do you think — will ETH treasuries follow the BTC playbook?"
            },
            "hims_healthcare": {
                "hooks": [
                    "The drug gets the headlines. The infrastructure play is HIMS.",
                    "GLP-1s are disrupting healthcare. HIMS owns the rails.",
                    "$725M revenue, Novo Nordisk deal locked. This is infrastructure.",
                ],
                "hashtags": ["#HIMS", "#Healthcare", "#GLP1"],
                "tone": "insightful",
                "cta": "Healthcare infrastructure or just another pharma play?"
            },
            "ai_agentic_commerce": {
                "hooks": [
                    "McKinsey says $3-5T in agentic commerce by 2030.",
                    "The winners won't be LLM makers — they'll be the intelligence companies.",
                    "We're entering the agentic economy. Here's what that means.",
                ],
                "hashtags": ["#AI", "#Agents", "#Commerce"],
                "tone": "forward-looking",
                "cta": "Which companies are positioning for the agentic economy?"
            }
        }
        
        if self.templates_file.exists():
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return {**default_templates, **json.load(f)}
        
        # Save defaults
        with open(self.templates_file, 'w', encoding='utf-8') as f:
            json.dump(default_templates, f, indent=2, ensure_ascii=False)
        
        return default_templates
    
    def parse_thread_drafts(self, file_path: str = None) -> List[ContentDraft]:
        """
        Parse thread drafts from markdown file
        Expected format: ## Thread N: Title followed by numbered posts
        """
        if file_path is None:
            file_path = Path("C:/Users/quent/OneDrive/Mission Control/Content/threads_draft.md")
        
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"[PIPELINE] No thread drafts found at {file_path}")
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        drafts = []
        
        # Parse threads using regex
        # Pattern: ## (emoji) Thread N: Title
        thread_pattern = r'##\s*(?:[🧵🔥💎🏥🤖]\s*)?Thread\s*\d+:\s*([^\n]+)(.*?)(?=##\s*(?:[🧵🔥💎🏥🤖]\s*)?Thread|\Z)'
        post_pattern = r'\*\*Post\s*(\d+)/(\d+):\*\*\s*```\n(.*?)```'
        
        for match in re.finditer(thread_pattern, content, re.DOTALL):
            title = match.group(1).strip()
            thread_content = match.group(2)
            
            posts = []
            for post_match in re.finditer(post_pattern, thread_content, re.DOTALL):
                post_num = int(post_match.group(1))
                total_posts = int(post_match.group(2))
                post_content = post_match.group(3).strip()
                posts.append({
                    "number": post_num,
                    "total": total_posts,
                    "content": post_content,
                    "char_count": len(post_content)
                })
            
            if posts:
                draft_id = f"thread_{self._slugify(title)}_{int(datetime.now().timestamp())}"
                
                # Extract hooks from first post
                hooks = self._extract_hooks(posts[0]["content"])
                
                draft = ContentDraft(
                    id=draft_id,
                    title=title,
                    content_type="thread",
                    platform="x",
                    body=self._format_thread_body(posts),
                    hooks=hooks,
                    hashtags=self._extract_hashtags(posts[0]["content"]),
                    character_count=sum(p["char_count"] for p in posts),
                    media=[],
                    source_file=str(file_path),
                    created_at=datetime.now().isoformat(),
                    status="draft"
                )
                drafts.append(draft)
                self.drafts[draft_id] = draft
        
        print(f"[PIPELINE] Parsed {len(drafts)} thread drafts from {file_path}")
        return drafts
    
    def parse_single_posts(self, file_path: str = None) -> List[ContentDraft]:
        """Parse single posts from a file"""
        if file_path is None:
            file_path = Path("C:/Users/quent/OneDrive/Mission Control/Content/single_posts.md")
        
        file_path = Path(file_path)
        if not file_path.exists():
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        drafts = []
        # Parse single posts: ## Post Title followed by content
        post_pattern = r'##\s*([^\n]+)\n\n(.*?)(?=##|\Z)'
        
        for match in re.finditer(post_pattern, content, re.DOTALL):
            title = match.group(1).strip()
            body = match.group(2).strip()
            
            draft_id = f"post_{self._slugify(title)}_{int(datetime.now().timestamp())}"
            
            draft = ContentDraft(
                id=draft_id,
                title=title,
                content_type="single",
                platform="x",
                body=body,
                hooks=self._extract_hooks(body),
                hashtags=self._extract_hashtags(body),
                character_count=len(body),
                media=[],
                source_file=str(file_path),
                created_at=datetime.now().isoformat(),
                status="draft"
            )
            drafts.append(draft)
            self.drafts[draft_id] = draft
        
        print(f"[PIPELINE] Parsed {len(drafts)} single posts from {file_path}")
        return drafts
    
    def _slugify(self, text: str) -> str:
        """Convert text to slug"""
        return re.sub(r'[^\w\s-]', '', text).strip().lower().replace(' ', '_')[:30]
    
    def _extract_hooks(self, content: str) -> List[str]:
        """Extract potential hooks from content"""
        hooks = []
        lines = content.split('\n')
        
        # First non-empty line is usually the hook
        for line in lines:
            line = line.strip()
            if line and len(line) > 20 and len(line) < 280:
                hooks.append(line)
                break
        
        return hooks
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from content"""
        return re.findall(r'#\w+', content)
    
    def _format_thread_body(self, posts: List[Dict]) -> str:
        """Format thread posts into a single body string"""
        return "\n\n---\n\n".join([
            f"[{p['number']}/{p['total']}]\n{p['content']}"
            for p in posts
        ])
    
    def apply_template(self, draft_id: str, template_name: str) -> ContentDraft:
        """Apply a template to enhance a draft"""
        if draft_id not in self.drafts:
            raise ValueError(f"Draft {draft_id} not found")
        
        draft = self.drafts[draft_id]
        template = self.templates.get(template_name)
        
        if not template:
            print(f"[PIPELINE] Template {template_name} not found")
            return draft
        
        # Enhance draft with template
        if not draft.hooks and template.get("hooks"):
            draft.hooks = template["hooks"]
        
        if not draft.hashtags and template.get("hashtags"):
            draft.hashtags = template["hashtags"]
        
        print(f"[PIPELINE] Applied template '{template_name}' to {draft_id}")
        return draft
    
    def prepare_for_review(self, draft_id: str) -> Dict:
        """
        Prepare draft for human review
        Returns formatted review package
        """
        if draft_id not in self.drafts:
            raise ValueError(f"Draft {draft_id} not found")
        
        draft = self.drafts[draft_id]
        
        review_package = {
            "id": draft.id,
            "title": draft.title,
            "type": draft.content_type,
            "platform": draft.platform,
            "character_count": draft.character_count,
            "hooks": draft.hooks[:3],  # Top 3 hooks
            "preview": draft.body[:500] + "..." if len(draft.body) > 500 else draft.body,
            "hashtags": draft.hashtags,
            "media_required": len(draft.media) == 0,
            "ready_for_scheduling": draft.status == "draft"
        }
        
        return review_package
    
    def save_draft(self, draft: ContentDraft):
        """Save draft to file"""
        draft_file = self.drafts_dir / f"{draft.id}.json"
        
        with open(draft_file, 'w', encoding='utf-8') as f:
            json.dump({
                "id": draft.id,
                "title": draft.title,
                "content_type": draft.content_type,
                "platform": draft.platform,
                "body": draft.body,
                "hooks": draft.hooks,
                "hashtags": draft.hashtags,
                "character_count": draft.character_count,
                "media": draft.media,
                "source_file": draft.source_file,
                "created_at": draft.created_at,
                "status": draft.status,
                "scheduled_time": draft.scheduled_time
            }, f, indent=2, ensure_ascii=False)
        
        print(f"[PIPELINE] Saved draft: {draft_file}")
    
    def queue_for_approval(self, draft_id: str) -> Dict:
        """Queue draft for approval via orchestrator"""
        if draft_id not in self.drafts:
            raise ValueError(f"Draft {draft_id} not found")
        
        draft = self.drafts[draft_id]
        draft.status = "ready"
        
        # Save to queue
        queue = []
        if self.queue_file.exists():
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                queue = json.load(f)
        
        queue.append({
            "id": draft.id,
            "title": draft.title,
            "type": draft.content_type,
            "status": "awaiting_approval",
            "submitted_at": datetime.now().isoformat()
        })
        
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        
        # Save draft file
        self.save_draft(draft)
        
        review = self.prepare_for_review(draft_id)
        print(f"[PIPELINE] Draft {draft_id} queued for approval")
        
        return review
    
    def get_ready_drafts(self) -> List[ContentDraft]:
        """Get all drafts ready for review"""
        return [d for d in self.drafts.values() if d.status == "draft"]
    
    def list_queue(self) -> List[Dict]:
        """List all items in approval queue"""
        if not self.queue_file.exists():
            return []
        
        with open(self.queue_file, 'r', encoding='utf-8') as f:
            return json.load(f)

# Integration with orchestrator
def create_content_task(draft_id: str, orchestrator=None) -> str:
    """
    Create an orchestrator task for content approval
    Returns task ID
    """
    if orchestrator is None:
        # Import here to avoid circular dependency
        from social_media_orchestrator import get_orchestrator, Platform, WorkflowType
        orchestrator = get_orchestrator()
    
    task = orchestrator.workflow_content_ops(
        platform=Platform.X,
        content_type="thread",
        draft_path=f"drafts/{draft_id}.json"
    )
    
    return task.id

if __name__ == "__main__":
    # Test pipeline
    pipeline = ContentPipeline("C:\\Users\\quent\\OneDrive\\Mission Control")
    
    # Parse thread drafts
    threads = pipeline.parse_thread_drafts()
    
    if threads:
        # Prepare first thread for review
        thread = threads[0]
        review = pipeline.queue_for_approval(thread.id)
        
        print("\n" + "="*60)
        print("CONTENT REVIEW PACKAGE")
        print("="*60)
        print(f"Title: {review['title']}")
        print(f"Type: {review['type']}")
        print(f"Characters: {review['character_count']}")
        print(f"\nHooks:")
        for i, hook in enumerate(review['hooks'], 1):
            print(f"  {i}. {hook[:80]}...")
        print(f"\nPreview:\n{review['preview'][:300]}...")
        print("="*60)
        print("\nStatus: AWAITING APPROVAL")
        print("Action: Review and approve to queue for posting")
