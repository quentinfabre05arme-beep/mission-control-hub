#!/usr/bin/env python3
"""
Multi-Agent Orchestrator v1.0
A2A protocol-inspired multi-agent system with specialized agents
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Agent role types."""
    RESEARCHER = "researcher"
    CREATOR = "creator"
    CRITIC = "critic"
    DISTRIBUTOR = "distributor"
    COORDINATOR = "coordinator"
    MEMORY = "memory"


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    AWAITING_HUMAN = "awaiting_human"


@dataclass
class AgentMessage:
    """Message between agents (A2A protocol inspired)."""
    sender: str
    recipient: str
    message_type: str
    content: Dict[str, Any]
    timestamp: str
    conversation_id: str
    
    def to_dict(self) -> Dict:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type,
            "content": self.content,
            "timestamp": self.timestamp,
            "conversation_id": self.conversation_id
        }


@dataclass
class Task:
    """Task for agent execution."""
    task_id: str
    task_type: str
    description: str
    assigned_to: Optional[str]
    status: TaskStatus
    priority: str
    dependencies: List[str]
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    created_at: str
    completed_at: Optional[str]
    error_message: Optional[str]


class BaseAgent:
    """Base class for all specialized agents."""
    
    def __init__(self, name: str, role: AgentRole):
        self.name = name
        self.role = role
        self.memory: List[Dict] = []
        self.tools: Dict[str, Callable] = {}
        self.state: Dict[str, Any] = {}
        
    def register_tool(self, tool_name: str, tool_func: Callable):
        """Register a tool for the agent."""
        self.tools[tool_name] = tool_func
        
    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a registered tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not registered")
        return self.tools[tool_name](**kwargs)
    
    def remember(self, key: str, value: Any):
        """Store in agent memory."""
        self.memory.append({
            "key": key,
            "value": value,
            "timestamp": datetime.now().isoformat()
        })
    
    def recall(self, key: str) -> Optional[Any]:
        """Recall from agent memory."""
        for item in reversed(self.memory):
            if item["key"] == key:
                return item["value"]
        return None
    
    def execute(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task - to be implemented by subclasses."""
        raise NotImplementedError
    
    def communicate(self, recipient: str, message_type: str, content: Dict) -> AgentMessage:
        """Create a message to another agent."""
        return AgentMessage(
            sender=self.name,
            recipient=recipient,
            message_type=message_type,
            content=content,
            timestamp=datetime.now().isoformat(),
            conversation_id=f"{self.name}_{recipient}_{datetime.now().timestamp()}"
        )


class ResearchAgent(BaseAgent):
    """Agent specialized in research and information gathering."""
    
    def __init__(self):
        super().__init__("ResearchAgent", AgentRole.RESEARCHER)
        self.register_tool("web_search", self._web_search)
        self.register_tool("trend_analysis", self._trend_analysis)
        
    def execute(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research tasks."""
        logger.info(f"[ResearchAgent] Executing: {task.description}")
        
        research_results = {
            "sources": [],
            "findings": [],
            "confidence": 0.0
        }
        
        # Perform web search
        topic = task.input_data.get("topic", "")
        if topic:
            search_results = self.use_tool("web_search", query=topic)
            research_results["findings"].extend(search_results)
        
        # Analyze trends
        trends = self.use_tool("trend_analysis", topic=topic)
        research_results["trends"] = trends
        
        # Calculate confidence
        research_results["confidence"] = self._calculate_confidence(research_results)
        
        return {
            "status": "success",
            "data": research_results,
            "agent": self.name
        }
    
    def _web_search(self, query: str) -> List[Dict]:
        """Simulated web search - would integrate with actual search."""
        return [{"source": f"web_{i}", "content": f"Research on {query}"} 
                for i in range(3)]
    
    def _trend_analysis(self, topic: str) -> Dict:
        """Analyze trends for topic."""
        return {"topic": topic, "trending": True, "momentum": 0.75}
    
    def _calculate_confidence(self, results: Dict) -> float:
        """Calculate confidence score."""
        base = 0.5
        if results.get("findings"):
            base += 0.2 * min(len(results["findings"]) / 5, 0.3)
        if results.get("trends"):
            base += 0.2
        return round(min(1.0, base), 2)


class CreatorAgent(BaseAgent):
    """Agent specialized in content creation."""
    
    def __init__(self):
        super().__init__("CreatorAgent", AgentRole.CREATOR)
        self.register_tool("generate_text", self._generate_text)
        self.register_tool("create_hook", self._create_hook)
        
    def execute(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute content creation tasks."""
        logger.info(f"[CreatorAgent] Creating: {task.description}")
        
        # Get research from context
        research = context.get("research_results", {})
        
        content_type = task.input_data.get("content_type", "tweet")
        
        # Generate content
        if content_type == "tweet":
            content = self._create_tweet(research, task.input_data)
        elif content_type == "thread":
            content = self._create_thread(research, task.input_data)
        else:
            content = self.use_tool("generate_text", prompt=task.description)
        
        return {
            "status": "success",
            "data": {
                "content": content,
                "content_type": content_type,
                "variations": self._generate_variations(content)
            },
            "agent": self.name
        }
    
    def _create_tweet(self, research: Dict, params: Dict) -> str:
        """Create a tweet based on research."""
        topic = params.get("topic", "")
        angle = params.get("angle", "insight")
        
        # Create hook
        hook = self.use_tool("create_hook", topic=topic, angle=angle)
        
        tweet = f"{hook}\n\n"
        
        # Add key finding
        findings = research.get("findings", [])
        if findings:
            tweet += f"Key insight: {findings[0].get('content', '')[:100]}\n\n"
        
        # Add reply hook
        tweet += "What do you think?"
        
        return tweet
    
    def _create_thread(self, research: Dict, params: Dict) -> List[str]:
        """Create a thread based on research."""
        topic = params.get("topic", "")
        
        tweets = []
        
        # Hook tweet
        hook_tweet = self.use_tool("create_hook", topic=topic, angle="thread")
        tweets.append(f"{hook_tweet}\n\n(Thread 🧵)")
        
        # Body tweets
        findings = research.get("findings", [])
        for i, finding in enumerate(findings[:5], 1):
            tweets.append(f"{i}/ {finding.get('content', '')}")
        
        # CTA tweet
        tweets.append("That's the key takeaway.\n\nWhat would you add?\n\nFollow for more insights.")
        
        return tweets
    
    def _generate_text(self, prompt: str) -> str:
        """Generate text content."""
        return f"Generated content for: {prompt}"
    
    def _create_hook(self, topic: str, angle: str) -> str:
        """Create an engaging hook."""
        hooks = {
            "insight": f"The real reason {topic} matters:",
            "contrarian": f"Everyone is wrong about {topic}.",
            "data": f"New data reveals {topic}:",
            "thread": f"I spent 100 hours studying {topic}."
        }
        return hooks.get(angle, hooks["insight"])
    
    def _generate_variations(self, content: str, num: int = 3) -> List[str]:
        """Generate content variations."""
        return [f"Variation {i}: {content[:50]}..." for i in range(1, num+1)]


class CriticAgent(BaseAgent):
    """Agent specialized in quality review and improvement."""
    
    def __init__(self):
        super().__init__("CriticAgent", AgentRole.CRITIC)
        self.register_tool("evaluate_quality", self._evaluate_quality)
        
    def execute(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute critique tasks."""
        logger.info(f"[CriticAgent] Reviewing: {task.description}")
        
        content = task.input_data.get("content", "")
        content_type = task.input_data.get("content_type", "tweet")
        
        # Evaluate quality
        evaluation = self.use_tool("evaluate_quality", content=content, content_type=content_type)
        
        # Generate improvements
        improvements = self._suggest_improvements(evaluation)
        
        return {
            "status": "success",
            "data": {
                "evaluation": evaluation,
                "passed": evaluation["overall_score"] >= 0.75,
                "improvements": improvements,
                "revised_content": self._revise_content(content, improvements) if improvements else content
            },
            "agent": self.name
        }
    
    def _evaluate_quality(self, content: str, content_type: str) -> Dict:
        """Evaluate content quality across multiple dimensions."""
        
        dimensions = {
            "factual_accuracy": self._check_factual_accuracy(content),
            "clarity": self._check_clarity(content),
            "engagement_potential": self._check_engagement(content),
            "brand_alignment": self._check_brand_alignment(content),
            "algorithm_optimization": self._check_algorithm_optimization(content),
            "originality": self._check_originality(content)
        }
        
        overall_score = sum(dimensions.values()) / len(dimensions)
        
        return {
            "overall_score": round(overall_score, 2),
            "dimensions": dimensions,
            "content_type": content_type
        }
    
    def _check_factual_accuracy(self, content: str) -> float:
        """Check factual accuracy."""
        # Placeholder - would integrate with fact-checking
        return 0.85
    
    def _check_clarity(self, content: str) -> float:
        """Check clarity."""
        # Simple heuristic: shorter, clearer
        if len(content) < 280:
            return 0.9
        return 0.75
    
    def _check_engagement(self, content: str) -> float:
        """Check engagement potential."""
        score = 0.5
        if "?" in content:
            score += 0.2
        if any(w in content.lower() for w in ["you", "your"]):
            score += 0.15
        return min(1.0, score)
    
    def _check_brand_alignment(self, content: str) -> float:
        """Check brand voice alignment."""
        # Placeholder - would check against brand guidelines
        return 0.8
    
    def _check_algorithm_optimization(self, content: str) -> float:
        """Check X algorithm optimization."""
        score = 0.5
        # No external links
        if "http" not in content:
            score += 0.2
        # Has reply hook
        if "?" in content or "think" in content.lower():
            score += 0.2
        return min(1.0, score)
    
    def _check_originality(self, content: str) -> float:
        """Check content originality."""
        # Placeholder - would check against existing content
        return 0.75
    
    def _suggest_improvements(self, evaluation: Dict) -> List[Dict]:
        """Suggest improvements based on evaluation."""
        improvements = []
        
        for dim, score in evaluation["dimensions"].items():
            if score < 0.7:
                improvements.append({
                    "dimension": dim,
                    "current_score": score,
                    "suggestion": self._get_improvement_suggestion(dim)
                })
        
        return improvements
    
    def _get_improvement_suggestion(self, dimension: str) -> str:
        """Get improvement suggestion for a dimension."""
        suggestions = {
            "factual_accuracy": "Verify all claims with sources",
            "clarity": "Simplify language, use shorter sentences",
            "engagement_potential": "Add question or call-to-action",
            "brand_alignment": "Adjust tone to match brand voice",
            "algorithm_optimization": "Move links to reply, add hook",
            "originality": "Add unique perspective or data"
        }
        return suggestions.get(dimension, "Review and improve")
    
    def _revise_content(self, content: str, improvements: List[Dict]) -> str:
        """Revise content based on improvements."""
        # Placeholder - would use LLM for actual revision
        return f"[Revised] {content[:100]}..."


class DistributionAgent(BaseAgent):
    """Agent specialized in content distribution."""
    
    def __init__(self):
        super().__init__("DistributionAgent", AgentRole.DISTRIBUTOR)
        self.register_tool("schedule_post", self._schedule_post)
        self.register_tool("optimize_timing", self._optimize_timing)
        
    def execute(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute distribution tasks."""
        logger.info(f"[DistributionAgent] Distributing: {task.description}")
        
        content = task.input_data.get("content", "")
        platforms = task.input_data.get("platforms", ["x"])
        
        distribution_plan = []
        
        for platform in platforms:
            # Optimize timing
            timing = self.use_tool("optimize_timing", platform=platform)
            
            # Schedule post
            schedule_info = self.use_tool("schedule_post", 
                                          content=content, 
                                          platform=platform,
                                          optimal_time=timing)
            
            distribution_plan.append({
                "platform": platform,
                "timing": timing,
                "schedule_info": schedule_info
            })
        
        return {
            "status": "success",
            "data": {
                "distribution_plan": distribution_plan,
                "requires_approval": True
            },
            "agent": self.name
        }
    
    def _schedule_post(self, content: str, platform: str, optimal_time: str) -> Dict:
        """Schedule a post."""
        return {
            "platform": platform,
            "status": "scheduled",
            "scheduled_time": optimal_time,
            "content_preview": content[:100]
        }
    
    def _optimize_timing(self, platform: str) -> str:
        """Optimize posting time."""
        from datetime import datetime, timedelta
        
        # Best times: 5PM, 9AM, 12PM, 8PM
        best_hours = [17, 9, 12, 20]
        
        now = datetime.now()
        
        for day_offset in range(7):
            for hour in best_hours:
                candidate = now + timedelta(days=day_offset)
                candidate = candidate.replace(hour=hour, minute=0)
                
                if candidate > now:
                    return candidate.isoformat()
        
        return (now + timedelta(hours=1)).isoformat()


class MultiAgentOrchestrator:
    """
    Orchestrates multiple specialized agents with A2A protocol-inspired communication.
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.tasks: Dict[str, Task] = {}
        self.messages: List[AgentMessage] = []
        self.workflow_history: List[Dict] = []
        
        # Initialize agents
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all specialized agents."""
        self.register_agent(ResearchAgent())
        self.register_agent(CreatorAgent())
        self.register_agent(CriticAgent())
        self.register_agent(DistributionAgent())
        
        # Coordinator is the orchestrator itself
        logger.info(f"[Orchestrator] Initialized {len(self.agents)} agents")
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent."""
        self.agents[agent.name] = agent
    
    def create_task(self, task_type: str, description: str, 
                   assigned_to: str, input_data: Dict,
                   priority: str = "normal", 
                   dependencies: List[str] = None) -> Task:
        """Create a new task."""
        import uuid
        
        task_id = str(uuid.uuid4())[:8]
        
        task = Task(
            task_id=task_id,
            task_type=task_type,
            description=description,
            assigned_to=assigned_to,
            status=TaskStatus.PENDING,
            priority=priority,
            dependencies=dependencies or [],
            input_data=input_data,
            output_data={},
            created_at=datetime.now().isoformat(),
            completed_at=None,
            error_message=None
        )
        
        self.tasks[task_id] = task
        logger.info(f"[Orchestrator] Created task {task_id}: {description}")
        
        return task
    
    def execute_workflow(self, workflow_type: str, input_data: Dict) -> Dict[str, Any]:
        """
        Execute a complete multi-agent workflow.
        """
        logger.info(f"[Orchestrator] Starting workflow: {workflow_type}")
        
        workflow_start = datetime.now()
        context: Dict[str, Any] = {"input": input_data}
        
        if workflow_type == "content_creation":
            return self._content_creation_workflow(input_data, context)
        elif workflow_type == "research":
            return self._research_workflow(input_data, context)
        else:
            return {"error": f"Unknown workflow type: {workflow_type}"}
    
    def _content_creation_workflow(self, input_data: Dict, context: Dict) -> Dict[str, Any]:
        """
        Complete content creation workflow:
        1. ResearchAgent - Gather information
        2. CreatorAgent - Create content
        3. CriticAgent - Review and improve
        4. DistributionAgent - Plan distribution
        """
        results = {
            "workflow": "content_creation",
            "steps": [],
            "status": "success"
        }
        
        # Step 1: Research
        research_task = self.create_task(
            task_type="research",
            description=f"Research topic: {input_data.get('topic', '')}",
            assigned_to="ResearchAgent",
            input_data={"topic": input_data.get("topic", "")},
            priority="high"
        )
        
        research_result = self.agents["ResearchAgent"].execute(research_task, context)
        research_task.status = TaskStatus.COMPLETED
        research_task.output_data = research_result
        context["research_results"] = research_result.get("data", {})
        results["steps"].append({
            "step": 1,
            "agent": "ResearchAgent",
            "status": "completed",
            "result": research_result
        })
        
        # Step 2: Create
        creation_task = self.create_task(
            task_type="content_creation",
            description="Create content based on research",
            assigned_to="CreatorAgent",
            input_data={
                "topic": input_data.get("topic", ""),
                "content_type": input_data.get("content_type", "tweet"),
                "angle": input_data.get("angle", "insight")
            },
            priority="high",
            dependencies=[research_task.task_id]
        )
        
        creation_result = self.agents["CreatorAgent"].execute(creation_task, context)
        creation_task.status = TaskStatus.COMPLETED
        creation_task.output_data = creation_result
        context["created_content"] = creation_result.get("data", {})
        results["steps"].append({
            "step": 2,
            "agent": "CreatorAgent",
            "status": "completed",
            "result": creation_result
        })
        
        # Step 3: Critique
        critique_task = self.create_task(
            task_type="quality_review",
            description="Review content quality",
            assigned_to="CriticAgent",
            input_data=context["created_content"],
            priority="high",
            dependencies=[creation_task.task_id]
        )
        
        critique_result = self.agents["CriticAgent"].execute(critique_task, context)
        critique_task.status = TaskStatus.COMPLETED
        critique_task.output_data = critique_result
        context["critique_results"] = critique_result.get("data", {})
        results["steps"].append({
            "step": 3,
            "agent": "CriticAgent",
            "status": "completed",
            "result": critique_result
        })
        
        # Check if content passed review
        if not critique_result["data"].get("passed", False):
            results["status"] = "needs_revision"
            results["revised_content"] = critique_result["data"].get("revised_content")
            return results
        
        # Step 4: Distribution
        distribution_task = self.create_task(
            task_type="distribution_planning",
            description="Plan content distribution",
            assigned_to="DistributionAgent",
            input_data={
                "content": context["created_content"].get("content"),
                "platforms": input_data.get("platforms", ["x"])
            },
            priority="medium",
            dependencies=[critique_task.task_id]
        )
        
        distribution_result = self.agents["DistributionAgent"].execute(distribution_task, context)
        distribution_task.status = TaskStatus.COMPLETED
        distribution_task.output_data = distribution_result
        context["distribution_plan"] = distribution_result.get("data", {})
        results["steps"].append({
            "step": 4,
            "agent": "DistributionAgent",
            "status": "completed",
            "result": distribution_result
        })
        
        # Final result
        results["final_output"] = {
            "content": context["created_content"],
            "quality_score": critique_result["data"]["evaluation"]["overall_score"],
            "distribution_plan": context["distribution_plan"]
        }
        
        results["duration_seconds"] = (datetime.now() - workflow_start).total_seconds()
        
        return results
    
    def _research_workflow(self, input_data: Dict, context: Dict) -> Dict[str, Any]:
        """Simple research workflow."""
        research_task = self.create_task(
            task_type="research",
            description=f"Deep research on: {input_data.get('topic', '')}",
            assigned_to="ResearchAgent",
            input_data=input_data,
            priority="high"
        )
        
        result = self.agents["ResearchAgent"].execute(research_task, context)
        research_task.status = TaskStatus.COMPLETED
        
        return {
            "workflow": "research",
            "result": result,
            "status": "success"
        }
    
    def save_state(self, path: str = "memory/orchestrator_state.json"):
        """Save orchestrator state."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        state = {
            "tasks": {tid: {
                **asdict(task),
                "status": task.status.value
            } for tid, task in self.tasks.items()},
            "messages": [msg.to_dict() for msg in self.messages],
            "workflow_history": self.workflow_history,
            "saved_at": datetime.now().isoformat()
        }
        
        with open(path, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"[Orchestrator] State saved to {path}")
    
    def load_state(self, path: str = "memory/orchestrator_state.json"):
        """Load orchestrator state."""
        try:
            with open(path, 'r') as f:
                state = json.load(f)
            
            # Restore tasks
            for tid, task_data in state.get("tasks", {}).items():
                self.tasks[tid] = Task(
                    task_id=task_data["task_id"],
                    task_type=task_data["task_type"],
                    description=task_data["description"],
                    assigned_to=task_data["assigned_to"],
                    status=TaskStatus(task_data["status"]),
                    priority=task_data["priority"],
                    dependencies=task_data["dependencies"],
                    input_data=task_data["input_data"],
                    output_data=task_data["output_data"],
                    created_at=task_data["created_at"],
                    completed_at=task_data.get("completed_at"),
                    error_message=task_data.get("error_message")
                )
            
            logger.info(f"[Orchestrator] State loaded from {path}")
        except FileNotFoundError:
            logger.info(f"[Orchestrator] No state file found at {path}")


def main():
    """Example usage of Multi-Agent Orchestrator."""
    orchestrator = MultiAgentOrchestrator()
    
    # Example content creation workflow
    workflow_input = {
        "topic": "AI agents in content creation",
        "content_type": "tweet",
        "angle": "contrarian",
        "platforms": ["x"]
    }
    
    print("=" * 60)
    print("Running Content Creation Workflow")
    print("=" * 60)
    
    result = orchestrator.execute_workflow("content_creation", workflow_input)
    
    print(f"\nWorkflow Status: {result['status']}")
    print(f"Steps Completed: {len(result['steps'])}")
    
    for step in result["steps"]:
        print(f"\nStep {step['step']}: {step['agent']}")
        print(f"  Status: {step['status']}")
    
    if "final_output" in result:
        print("\n" + "=" * 60)
        print("Final Output")
        print("=" * 60)
        print(f"Quality Score: {result['final_output']['quality_score']}")
        print(f"Content Preview:")
        content = result['final_output']['content'].get('content', '')
        print(f"  {content[:200]}..." if len(content) > 200 else f"  {content}")
    
    # Save state
    orchestrator.save_state()


if __name__ == "__main__":
    main()
