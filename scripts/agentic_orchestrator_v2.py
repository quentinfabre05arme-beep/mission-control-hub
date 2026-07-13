#!/usr/bin/env python3
"""
agentic_orchestrator_v2.py
A2A Protocol-Inspired Multi-Agent Orchestrator
Based on 2025-2026 AI Agent Best Practices Research

Features:
- Specialized agents with clear responsibilities
- A2A-style communication protocol
- MCP-standardized tool integration
- Long-running autonomous workflows
- Error handling with human escalation
"""

import json
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentRole(Enum):
    RESEARCH = "research"
    CREATIVE = "creative"
    CRITIC = "critic"
    DISTRIBUTION = "distribution"
    COORDINATOR = "coordinator"


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"


@dataclass
class AgentMessage:
    """A2A-style message for inter-agent communication"""
    sender: str
    recipient: str
    message_type: str  # "task_request", "task_response", "tool_call", "escalation"
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    message_id: str = field(default_factory=lambda: datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f"))
    
    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }


@dataclass
class Task:
    """Task definition for agent execution"""
    task_id: str
    description: str
    assigned_agent: str
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None
    error_message: Optional[str] = None


class BaseAgent:
    """Base class for all specialized agents"""
    
    def __init__(self, name: str, role: AgentRole):
        self.name = name
        self.role = role
        self.message_queue: List[AgentMessage] = []
        self.task_history: List[Task] = []
        self.tools: Dict[str, Callable] = {}
        logger.info(f"Initialized {role.value} agent: {name}")
    
    def register_tool(self, tool_name: str, tool_func: Callable):
        """Register a tool for this agent (MCP-style)"""
        self.tools[tool_name] = tool_func
        logger.info(f"Registered tool '{tool_name}' for {self.name}")
    
    def receive_message(self, message: AgentMessage):
        """Receive a message from another agent"""
        self.message_queue.append(message)
        logger.info(f"{self.name} received message from {message.sender}: {message.message_type}")
    
    def process_task(self, task: Task) -> Task:
        """Process a task - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement process_task")
    
    def send_message(self, recipient: str, message_type: str, payload: Dict) -> AgentMessage:
        """Send a message to another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            message_type=message_type,
            payload=payload
        )
        logger.info(f"{self.name} sent {message_type} to {recipient}")
        return message


class ResearchAgent(BaseAgent):
    """Agent specialized in research and data gathering"""
    
    def __init__(self):
        super().__init__("ResearchAgent", AgentRole.RESEARCH)
        self.research_cache = {}
    
    def process_task(self, task: Task) -> Task:
        """Execute research task"""
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            research_topic = task.input_data.get("topic", "")
            research_type = task.input_data.get("type", "general")
            
            logger.info(f"ResearchAgent researching: {research_topic}")
            
            # Simulate research execution
            # In production, this would call web_search, memory_search, etc.
            research_results = {
                "topic": research_topic,
                "type": research_type,
                "sources": [],
                "key_findings": [],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Use registered tools if available
            if "web_search" in self.tools:
                search_results = self.tools["web_search"](research_topic)
                research_results["sources"] = search_results
            
            if "memory_search" in self.tools:
                memory_results = self.tools["memory_search"](research_topic)
                research_results["key_findings"] = memory_results
            
            task.output_data = research_results
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow().isoformat()
            
            self.task_history.append(task)
            logger.info(f"ResearchAgent completed task: {task.task_id}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            logger.error(f"ResearchAgent failed task {task.task_id}: {e}")
        
        return task


class CreativeAgent(BaseAgent):
    """Agent specialized in content creation"""
    
    def __init__(self):
        super().__init__("CreativeAgent", AgentRole.CREATIVE)
        self.content_templates = {}
    
    def process_task(self, task: Task) -> Task:
        """Execute creative task"""
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            content_type = task.input_data.get("content_type", "social_post")
            topic = task.input_data.get("topic", "")
            research_data = task.input_data.get("research_data", {})
            
            logger.info(f"CreativeAgent creating {content_type} about: {topic}")
            
            # Simulate content creation
            # In production, this would generate actual content
            content_variants = []
            angles = ["contrarian", "data_driven", "insight", "reframe"]
            
            for angle in angles:
                variant = {
                    "angle": angle,
                    "hook": f"[{angle.upper()}] Perspective on {topic}",
                    "body": f"Content body for {angle} angle...",
                    "cta": "What do you think?",
                    "variant_id": f"{task.task_id}_{angle}"
                }
                content_variants.append(variant)
            
            task.output_data = {
                "content_type": content_type,
                "topic": topic,
                "variants": content_variants,
                "created_at": datetime.utcnow().isoformat()
            }
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow().isoformat()
            
            self.task_history.append(task)
            logger.info(f"CreativeAgent completed task: {task.task_id}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            logger.error(f"CreativeAgent failed task {task.task_id}: {e}")
        
        return task


class CriticAgent(BaseAgent):
    """Agent specialized in content review and quality assessment"""
    
    def __init__(self):
        super().__init__("CriticAgent", AgentRole.CRITIC)
        self.quality_threshold = 0.75
    
    def process_task(self, task: Task) -> Task:
        """Execute critique task"""
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            content = task.input_data.get("content", {})
            review_type = task.input_data.get("review_type", "full")
            
            logger.info(f"CriticAgent reviewing content: {review_type}")
            
            # 7-dimension quality scoring (from research)
            dimensions = {
                "factual_accuracy": 0.0,
                "clarity": 0.0,
                "engagement_potential": 0.0,
                "brand_alignment": 0.0,
                "algorithm_optimization": 0.0,
                "originality": 0.0,
                "authenticity": 0.0
            }
            
            # Simulate scoring (production would use actual evaluation)
            import random
            for dim in dimensions:
                dimensions[dim] = round(random.uniform(0.6, 0.95), 2)
            
            overall_score = round(sum(dimensions.values()) / len(dimensions), 2)
            
            review_result = {
                "content_id": task.input_data.get("content_id"),
                "overall_score": overall_score,
                "dimensions": dimensions,
                "passed": overall_score >= self.quality_threshold,
                "recommendations": self._generate_recommendations(dimensions),
                "reviewed_at": datetime.utcnow().isoformat()
            }
            
            task.output_data = review_result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow().isoformat()
            
            self.task_history.append(task)
            logger.info(f"CriticAgent completed review: {overall_score}/1.0")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            logger.error(f"CriticAgent failed task {task.task_id}: {e}")
        
        return task
    
    def _generate_recommendations(self, dimensions: Dict) -> List[str]:
        """Generate improvement recommendations based on scores"""
        recommendations = []
        
        if dimensions["factual_accuracy"] < 0.8:
            recommendations.append("Verify facts with additional sources")
        if dimensions["engagement_potential"] < 0.8:
            recommendations.append("Add stronger hook or question")
        if dimensions["algorithm_optimization"] < 0.8:
            recommendations.append("Optimize for platform algorithm (replies, timing)")
        if dimensions["authenticity"] < 0.8:
            recommendations.append("Add personal touch or raw perspective")
        
        return recommendations


class DistributionAgent(BaseAgent):
    """Agent specialized in content distribution and scheduling"""
    
    def __init__(self):
        super().__init__("DistributionAgent", AgentRole.DISTRIBUTION)
        self.platform_configs = {}
    
    def process_task(self, task: Task) -> Task:
        """Execute distribution task"""
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            content = task.input_data.get("content", {})
            platform = task.input_data.get("platform", "x")
            scheduling = task.input_data.get("scheduling", "immediate")
            
            logger.info(f"DistributionAgent preparing content for {platform}")
            
            # Platform-specific optimization
            if platform == "x":
                optimized = self._optimize_for_x(content)
            elif platform == "linkedin":
                optimized = self._optimize_for_linkedin(content)
            else:
                optimized = content
            
            distribution_plan = {
                "content": optimized,
                "platform": platform,
                "schedule": scheduling,
                "requires_approval": True,  # HITL requirement
                "optimized_at": datetime.utcnow().isoformat(),
                "estimated_engagement": task.input_data.get("predicted_score", 0)
            }
            
            task.output_data = distribution_plan
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow().isoformat()
            
            self.task_history.append(task)
            logger.info(f"DistributionAgent completed task: {task.task_id}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            logger.error(f"DistributionAgent failed task {task.task_id}: {e}")
        
        return task
    
    def _optimize_for_x(self, content: Dict) -> Dict:
        """Optimize content for X/Twitter algorithm"""
        optimized = content.copy()
        # Reply-first strategy, link in reply, minimal hashtags
        optimized["strategy"] = "x_native"
        optimized["priority"] = "replies"  # 13.5x weight
        return optimized
    
    def _optimize_for_linkedin(self, content: Dict) -> Dict:
        """Optimize content for LinkedIn algorithm"""
        optimized = content.copy()
        optimized["strategy"] = "linkedin_native"
        optimized["priority"] = "comments"
        return optimized


class AgenticOrchestrator:
    """
    Main orchestrator managing multi-agent workflows
    A2A Protocol-inspired architecture
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.tasks: Dict[str, Task] = {}
        self.message_bus: List[AgentMessage] = []
        self.workflow_log: List[Dict] = []
        self.mcp_registry: Dict[str, Any] = {}
        
        # Initialize core agents
        self._initialize_agents()
        
        logger.info("AgenticOrchestrator v2.0 initialized")
    
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        self.register_agent(ResearchAgent())
        self.register_agent(CreativeAgent())
        self.register_agent(CriticAgent())
        self.register_agent(DistributionAgent())
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")
    
    def register_mcp_tool(self, tool_name: str, tool_config: Dict):
        """Register a tool in MCP format"""
        self.mcp_registry[tool_name] = {
            "name": tool_config.get("name", tool_name),
            "description": tool_config.get("description", ""),
            "input_schema": tool_config.get("input_schema", {}),
            "output_schema": tool_config.get("output_schema", {}),
            "handler": tool_config.get("handler")
        }
        logger.info(f"Registered MCP tool: {tool_name}")
    
    def execute_mcp_tool(self, tool_name: str, params: Dict) -> Any:
        """Execute a registered MCP tool"""
        if tool_name not in self.mcp_registry:
            raise ValueError(f"Tool not registered: {tool_name}")
        
        tool = self.mcp_registry[tool_name]
        handler = tool.get("handler")
        
        if handler:
            return handler(**params)
        return None
    
    def create_task(self, description: str, assigned_agent: str, input_data: Dict) -> Task:
        """Create a new task for an agent"""
        task_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        task = Task(
            task_id=task_id,
            description=description,
            assigned_agent=assigned_agent,
            input_data=input_data
        )
        self.tasks[task_id] = task
        logger.info(f"Created task {task_id} for {assigned_agent}")
        return task
    
    def execute_task(self, task: Task) -> Task:
        """Execute a task through the assigned agent"""
        agent_name = task.assigned_agent
        
        if agent_name not in self.agents:
            task.status = TaskStatus.FAILED
            task.error_message = f"Agent not found: {agent_name}"
            return task
        
        agent = self.agents[agent_name]
        result = agent.process_task(task)
        
        # Log workflow step
        self.workflow_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "task_id": task.task_id,
            "agent": agent_name,
            "status": result.status.value,
            "duration": None  # Could calculate from timestamps
        })
        
        return result
    
    def run_content_pipeline(self, topic: str, platform: str = "x") -> Dict:
        """
        Run the full content creation pipeline
        Research → Creative → Critic → Distribution
        """
        logger.info(f"Starting content pipeline for: {topic}")
        
        # Step 1: Research
        research_task = self.create_task(
            description=f"Research topic: {topic}",
            assigned_agent="ResearchAgent",
            input_data={"topic": topic, "type": "social_content"}
        )
        research_result = self.execute_task(research_task)
        
        if research_result.status != TaskStatus.COMPLETED:
            return {"error": "Research failed", "details": research_result.error_message}
        
        # Step 2: Create Content
        creative_task = self.create_task(
            description=f"Create content about: {topic}",
            assigned_agent="CreativeAgent",
            input_data={
                "topic": topic,
                "content_type": "social_post",
                "research_data": research_result.output_data
            }
        )
        creative_result = self.execute_task(creative_task)
        
        if creative_result.status != TaskStatus.COMPLETED:
            return {"error": "Content creation failed", "details": creative_result.error_message}
        
        # Step 3: Review (Reflection Pattern)
        variants = creative_result.output_data.get("variants", [])
        reviewed_variants = []
        
        for variant in variants:
            critic_task = self.create_task(
                description=f"Review content variant: {variant['variant_id']}",
                assigned_agent="CriticAgent",
                input_data={
                    "content": variant,
                    "content_id": variant["variant_id"],
                    "review_type": "full"
                }
            )
            critic_result = self.execute_task(critic_task)
            
            if critic_result.status == TaskStatus.COMPLETED:
                variant["review"] = critic_result.output_data
                reviewed_variants.append(variant)
        
        # Select best variant
        best_variant = max(
            reviewed_variants,
            key=lambda v: v.get("review", {}).get("overall_score", 0)
        )
        
        # Step 4: Distribution
        distribution_task = self.create_task(
            description=f"Prepare distribution for: {topic}",
            assigned_agent="DistributionAgent",
            input_data={
                "content": best_variant,
                "platform": platform,
                "scheduling": "optimal",
                "predicted_score": best_variant.get("review", {}).get("overall_score", 0)
            }
        )
        distribution_result = self.execute_task(distribution_task)
        
        if distribution_result.status != TaskStatus.COMPLETED:
            return {"error": "Distribution failed", "details": distribution_result.error_message}
        
        # Compile results
        pipeline_result = {
            "status": "completed",
            "topic": topic,
            "platform": platform,
            "best_variant": best_variant,
            "requires_human_approval": True,
            "distribution_plan": distribution_result.output_data,
            "workflow_summary": {
                "research_completed": research_result.status == TaskStatus.COMPLETED,
                "content_created": creative_result.status == TaskStatus.COMPLETED,
                "review_completed": len(reviewed_variants) > 0,
                "distribution_ready": distribution_result.status == TaskStatus.COMPLETED
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info("Content pipeline completed successfully")
        return pipeline_result
    
    def get_workflow_status(self) -> Dict:
        """Get current workflow status"""
        return {
            "agents": list(self.agents.keys()),
            "total_tasks": len(self.tasks),
            "completed_tasks": sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
            "failed_tasks": sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED),
            "mcp_tools": list(self.mcp_registry.keys()),
            "workflow_steps": len(self.workflow_log)
        }
    
    def export_workflow_log(self) -> List[Dict]:
        """Export complete workflow log for audit"""
        return self.workflow_log


# Example usage and testing
if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = AgenticOrchestrator()
    
    # Register MCP tools (example)
    def example_web_search(query: str):
        return [{"title": f"Result for {query}", "url": "https://example.com"}]
    
    orchestrator.register_mcp_tool("web_search", {
        "name": "web_search",
        "description": "Search the web for information",
        "input_schema": {"query": "string"},
        "output_schema": {"results": "array"},
        "handler": example_web_search
    })
    
    # Run a content pipeline
    result = orchestrator.run_content_pipeline(
        topic="AI agent capabilities 2026",
        platform="x"
    )
    
    print(json.dumps(result, indent=2))
    print("\nWorkflow Status:", orchestrator.get_workflow_status())
