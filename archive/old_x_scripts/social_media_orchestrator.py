"""
Social Media Operations System - Master Orchestrator
Phase 1: Core Infrastructure

This module provides:
- Workflow routing and dispatch
- Task queuing with approval gates
- Logging to memory
- Multi-agent coordination hooks
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

sys.stdout.reconfigure(encoding='utf-8')

class WorkflowType(Enum):
    CONTENT_OPS = "content_ops"
    MONITORING = "monitoring"
    ENGAGEMENT = "engagement"
    ANALYTICS = "analytics"
    REPURPOSING = "repurposing"

class Platform(Enum):
    X = "x"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    MULTI = "multi"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    EXECUTED = "executed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    id: str
    workflow: WorkflowType
    platform: Platform
    action: str
    payload: Dict
    status: TaskStatus
    created_at: str
    updated_at: str
    approved_by: Optional[str] = None
    executed_at: Optional[str] = None
    result: Optional[Dict] = None
    notes: List[str] = None
    
    def __post_init__(self):
        if self.notes is None:
            self.notes = []

class SocialMediaOrchestrator:
    """Central orchestrator for all social media operations"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace = Path(workspace_path) if workspace_path else Path(__file__).parent.parent
        self.queue_file = self.workspace / "operations" / "task_queue.json"
        self.memory_file = self.workspace / "operations" / "workflow_memory.json"
        
        # Ensure directories exist
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load or init queue
        self.tasks: Dict[str, Task] = {}
        self._load_queue()
    
    def _load_queue(self):
        """Load task queue from disk"""
        if self.queue_file.exists():
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for task_id, task_data in data.items():
                    task_data['workflow'] = WorkflowType(task_data['workflow'])
                    task_data['platform'] = Platform(task_data['platform'])
                    task_data['status'] = TaskStatus(task_data['status'])
                    self.tasks[task_id] = Task(**task_data)
    
    def _save_queue(self):
        """Save task queue to disk"""
        data = {}
        for task_id, task in self.tasks.items():
            task_dict = asdict(task)
            task_dict['workflow'] = task.workflow.value
            task_dict['platform'] = task.platform.value
            task_dict['status'] = task.status.value
            data[task_id] = task_dict
        
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_task(self, workflow: WorkflowType, platform: Platform, 
                    action: str, payload: Dict, task_id: str = None) -> Task:
        """Create a new task in the queue"""
        now = datetime.now().isoformat()
        task_id = task_id or f"{workflow.value}_{platform.value}_{int(datetime.now().timestamp())}"
        
        task = Task(
            id=task_id,
            workflow=workflow,
            platform=platform,
            action=action,
            payload=payload,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now
        )
        
        self.tasks[task_id] = task
        self._save_queue()
        
        self._log_event(f"Task created: {task_id} [{workflow.value}] [{action}]")
        return task
    
    def request_approval(self, task_id: str, reason: str = None) -> Task:
        """Move task to awaiting approval state"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        task.status = TaskStatus.AWAITING_APPROVAL
        task.updated_at = datetime.now().isoformat()
        task.notes.append(f"Approval requested: {reason or 'Manual review required'}")
        
        self._save_queue()
        self._log_event(f"Task awaiting approval: {task_id}")
        
        return task
    
    def approve_task(self, task_id: str, approved_by: str = "human") -> Task:
        """Approve a task for execution"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        task.status = TaskStatus.APPROVED
        task.approved_by = approved_by
        task.updated_at = datetime.now().isoformat()
        task.notes.append(f"Approved by: {approved_by}")
        
        self._save_queue()
        self._log_event(f"Task approved: {task_id} by {approved_by}")
        
        return task
    
    def execute_task(self, task_id: str, executor_func: Callable = None) -> Task:
        """Execute an approved task"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        
        if task.status != TaskStatus.APPROVED:
            raise ValueError(f"Task {task_id} not approved. Current status: {task.status.value}")
        
        task.status = TaskStatus.IN_PROGRESS
        task.updated_at = datetime.now().isoformat()
        self._save_queue()
        
        try:
            # Call executor if provided
            if executor_func:
                result = executor_func(task)
                task.result = result
            else:
                task.result = {"status": "executed", "message": "No executor provided, manual execution assumed"}
            
            task.status = TaskStatus.EXECUTED
            task.executed_at = datetime.now().isoformat()
            task.notes.append(f"Executed successfully at {task.executed_at}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = {"error": str(e)}
            task.notes.append(f"Execution failed: {str(e)}")
            self._log_event(f"Task failed: {task_id} - {str(e)}")
        
        self._save_queue()
        return task
    
    def get_pending_approvals(self) -> List[Task]:
        """Get all tasks awaiting approval"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.AWAITING_APPROVAL]
    
    def get_ready_to_execute(self) -> List[Task]:
        """Get all approved tasks ready to execute"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.APPROVED]
    
    def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get status of a specific task"""
        return self.tasks.get(task_id)
    
    def list_tasks(self, status: TaskStatus = None, limit: int = 20) -> List[Task]:
        """List tasks with optional filter"""
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        # Sort by created_at desc
        tasks.sort(key=lambda x: x.created_at, reverse=True)
        return tasks[:limit]
    
    def _log_event(self, message: str):
        """Log event to operations log"""
        log_file = self.workspace / "operations" / "events.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} | {message}\n")
        
        print(f"[ORCHESTRATOR] {message}")
    
    def workflow_content_ops(self, platform: Platform, content_type: str, 
                            draft_path: str = None, schedule_time: str = None) -> Task:
        """
        Workflow: Basic Content Operations
        Creates task for: Research → Draft → Approval → Schedule/Publish
        """
        payload = {
            "content_type": content_type,
            "draft_path": draft_path,
            "schedule_time": schedule_time,
            "steps": ["research", "draft", "approval", "publish"]
        }
        
        task = self.create_task(
            workflow=WorkflowType.CONTENT_OPS,
            platform=platform,
            action="content_pipeline",
            payload=payload
        )
        
        # Auto-request approval for content
        self.request_approval(task.id, f"Content ready for review: {content_type}")
        
        return task
    
    def workflow_engagement(self, platform: Platform, target_handle: str,
                           engagement_type: str = "reply", 
                           context: Dict = None) -> Task:
        """
        Workflow: Engagement
        Creates task for: Monitor → Context → Draft → Approval → Execute
        """
        payload = {
            "target_handle": target_handle,
            "engagement_type": engagement_type,
            "context": context or {},
            "steps": ["monitor", "context", "draft", "approval", "execute"]
        }
        
        task = self.create_task(
            workflow=WorkflowType.ENGAGEMENT,
            platform=platform,
            action=f"{engagement_type}_to_{target_handle}",
            payload=payload
        )
        
        self.request_approval(task.id, f"Engagement draft ready: {engagement_type} to {target_handle}")
        
        return task
    
    def workflow_monitoring(self, platform: Platform, 
                           monitor_type: str = "mentions",
                           targets: List[str] = None,
                           schedule: str = "*/30 * * * *") -> Task:
        """
        Workflow: Monitoring & Data Flow
        Creates scheduled monitoring task
        """
        payload = {
            "monitor_type": monitor_type,
            "targets": targets or [],
            "schedule": schedule,
            "steps": ["collect", "process", "store", "report"]
        }
        
        task = self.create_task(
            workflow=WorkflowType.MONITORING,
            platform=platform,
            action=f"monitor_{monitor_type}",
            payload=payload
        )
        
        return task

# Global orchestrator instance
_orchestrator = None

def get_orchestrator(workspace_path: str = None) -> SocialMediaOrchestrator:
    """Get or create the global orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = SocialMediaOrchestrator(workspace_path)
    return _orchestrator

if __name__ == "__main__":
    # Test/demo
    orch = get_orchestrator("C:\\Users\\quent\\.openclaw\\workspace")
    
    # Create a test task
    task = orch.workflow_content_ops(
        platform=Platform.X,
        content_type="thread",
        draft_path="../Mission Control/Content/threads_draft.md"
    )
    
    print(f"\nTest task created: {task.id}")
    print(f"Status: {task.status.value}")
    print(f"Awaiting approvals: {len(orch.get_pending_approvals())}")
