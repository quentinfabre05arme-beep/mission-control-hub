"""
Social Media Operations System - Master CLI
Phase 6: Integration & Command Interface

Brings together all pipelines into unified command interface
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add workspace to path for imports
sys.path.insert(0, str(Path(__file__).parent))

sys.stdout.reconfigure(encoding='utf-8')

class SocialMediaCLI:
    """Unified command interface for social media operations"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.operations_dir = self.workspace / "operations"
        self.operations_dir.mkdir(exist_ok=True)
    
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{'='*70}")
        print(f"  {text}")
        print(f"{'='*70}\n")
    
    def print_menu(self):
        """Print main menu"""
        self.print_header("SOCIAL MEDIA OPERATIONS SYSTEM")
        print("Phase 1: Core Infrastructure")
        print("Phase 2: Content Pipeline")
        print("Phase 3: Engagement Pipeline")
        print("Phase 4: Analytics Pipeline")
        print("Phase 5: Repurposing Pipeline")
        print("Phase 6: Integration & CLI")
        print(f"{'='*70}\n")
        
        print("📋 AVAILABLE COMMANDS:")
        print()
        print("  CONTENT OPERATIONS:")
        print("    content parse         - Parse thread drafts from markdown")
        print("    content queue         - Queue content for approval")
        print("    content list          - List content awaiting approval")
        print("    content approve <id>   - Approve content for posting")
        print()
        print("  ENGAGEMENT:")
        print("    engagement discover   - Discover engagement opportunities")
        print("    engagement plan       - Show daily engagement plan")
        print("    engagement queue      - List engagements awaiting approval")
        print("    engagement approve <id> - Approve engagement")
        print()
        print("  ANALYTICS:")
        print("    analytics snapshot    - Record metrics snapshot")
        print("    analytics report      - Generate weekly report")
        print("    analytics insights    - Generate insights")
        print("    analytics dashboard   - Get dashboard metrics")
        print()
        print("  REPURPOSING:")
        print("    repurpose create     - Create multi-platform job")
        print("    repurpose list       - List repurposing jobs")
        print("    repurpose approve    - Approve platform adaptation")
        print()
        print("  SYSTEM:")
        print("    status               - Show system status")
        print("    help                 - Show this menu")
        print()
    
    def status(self):
        """Show system status"""
        self.print_header("SYSTEM STATUS")
        
        # Check operations directory
        ops_files = list(self.operations_dir.glob("*.json")) if self.operations_dir.exists() else []
        
        print(f"Workspace: {self.workspace}")
        print(f"Operations directory: {self.operations_dir}")
        print(f"Operation files: {len(ops_files)}")
        print()
        
        # Check each pipeline
        pipelines = {
            "Content Pipeline": "content_queue.json",
            "Engagement Pipeline": "engagement_opportunities.json",
            "Analytics Pipeline": "analytics_snapshots.json",
            "Repurposing Pipeline": "repurposing_jobs.json",
            "Orchestrator": "task_queue.json"
        }
        
        print("📊 PIPELINE STATUS:")
        for name, filename in pipelines.items():
            filepath = self.operations_dir / filename
            status = "✅ Active" if filepath.exists() else "⚠️  Not initialized"
            count = ""
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        count = f" ({len(data)} items)"
                except:
                    pass
            print(f"  {name:25} {status}{count}")
        
        print()
        print("System ready for operations.")
    
    def content_parse(self):
        """Parse content from markdown files"""
        try:
            from content_pipeline import ContentPipeline
            pipeline = ContentPipeline(str(self.workspace))
            
            self.print_header("CONTENT PARSING")
            
            # Parse thread drafts
            threads = pipeline.parse_thread_drafts()
            print(f"Parsed {len(threads)} thread drafts")
            
            for thread in threads:
                print(f"  ✓ {thread.title} ({thread.character_count} chars)")
            
            print("\nReady to queue for approval.")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def content_queue(self):
        """Queue content for approval"""
        try:
            from content_pipeline import ContentPipeline
            pipeline = ContentPipeline(str(self.workspace))
            
            self.print_header("QUEUE CONTENT FOR APPROVAL")
            
            # Get ready drafts
            drafts = pipeline.get_ready_drafts()
            
            if not drafts:
                print("No drafts ready for queuing.")
                print("Run 'content parse' first.")
                return
            
            for draft in drafts:
                review = pipeline.queue_for_approval(draft.id)
                print(f"✓ Queued: {review['title']}")
                print(f"  Preview: {review['preview'][:100]}...")
                print()
            
            print(f"Total queued: {len(drafts)}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def content_list(self):
        """List content awaiting approval"""
        try:
            queue_file = self.operations_dir / "content_queue.json"
            
            self.print_header("CONTENT QUEUE")
            
            if not queue_file.exists():
                print("No content in queue.")
                return
            
            with open(queue_file, 'r', encoding='utf-8') as f:
                queue = json.load(f)
            
            if not queue:
                print("Queue is empty.")
                return
            
            for item in queue:
                print(f"📄 {item['title']}")
                print(f"   ID: {item['id']}")
                print(f"   Status: {item['status']}")
                print(f"   Submitted: {item['submitted_at'][:10]}")
                print()
            
            print(f"Total items: {len(queue)}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def engagement_plan(self):
        """Show daily engagement plan"""
        try:
            from engagement_pipeline import EngagementPipeline
            pipeline = EngagementPipeline(str(self.workspace))
            
            self.print_header("DAILY ENGAGEMENT PLAN")
            
            recommendations = pipeline.get_daily_engagement_plan()
            
            if not recommendations:
                print("No engagement recommendations available.")
                return
            
            for i, rec in enumerate(recommendations, 1):
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡"
                print(f"{priority_emoji} {i}. {rec['handle']}")
                print(f"   {rec['name']} | Focus: {rec['focus']}")
                print(f"   {rec['reason']}")
                print()
            
        except Exception as e:
            print(f"Error: {e}")
    
    def analytics_dashboard(self):
        """Show dashboard metrics"""
        try:
            from analytics_pipeline import AnalyticsPipeline
            pipeline = AnalyticsPipeline(str(self.workspace))
            
            self.print_header("DASHBOARD METRICS")
            
            metrics = pipeline.get_dashboard_metrics()
            
            if "error" in metrics:
                print(f"Error: {metrics['error']}")
                return
            
            print(f"👥 Followers: {metrics['followers']:,} ({metrics['followers_change']:+})")
            print(f"📊 Engagement Rate: {metrics['engagement_rate']}%")
            print(f"👀 Impressions: {metrics['impressions']:,}")
            print(f"📈 Growth: {metrics['growth_pct']:+.2f}%")
            print(f"🎯 Target Progress: {metrics['target_progress']:.2f}%")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def run_command(self, command, *args):
        """Run a specific command"""
        commands = {
            'status': self.status,
            'help': self.print_menu,
            'content parse': self.content_parse,
            'content queue': self.content_queue,
            'content list': self.content_list,
            'engagement plan': self.engagement_plan,
            'analytics dashboard': self.analytics_dashboard,
        }
        
        if command in commands:
            commands[command]()
        else:
            print(f"Unknown command: {command}")
            print("Run 'help' for available commands.")

def main():
    """Main entry point"""
    cli = SocialMediaCLI()
    
    parser = argparse.ArgumentParser(description='Social Media Operations System')
    parser.add_argument('command', nargs='?', help='Command to run')
    parser.add_argument('subcommand', nargs='?', help='Subcommand')
    parser.add_argument('args', nargs='*', help='Additional arguments')
    
    args = parser.parse_args()
    
    if not args.command:
        cli.print_menu()
        return
    
    # Build full command
    full_command = args.command
    if args.subcommand:
        full_command += f" {args.subcommand}"
    
    cli.run_command(full_command, *args.args)

if __name__ == "__main__":
    main()
