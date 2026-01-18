import asyncio
from typing import List

from antiminer.logic.models import Issue, AppState

from antiminer.constants import TaskType, IssueStatus
from antiminer.logic.cpu_tasks import analyze_file_content
from antiminer.services.scheduler import Scheduler


class Analyzer:
    def __init__(self, scheduler: Scheduler, state: AppState):
        self.scheduler = scheduler
        self.state = state

    async def run_analysis(self, targets: List[str]):
        self.state.is_running = True
        self.state.total_count = len(targets)
        self.state.processed_count = 0
        self.state.issues = []
        
        for i, target in enumerate(targets):
            # Simulate reading file (IO)
            await asyncio.sleep(0.05)
            
            # CPU-bound analysis
            is_threat = await self.scheduler.schedule(
                TaskType.CPU, 
                analyze_file_content, 
                f"Content of {target} with some potential miner patterns" if i % 3 == 0 else "Clean content"
            )
            
            if is_threat:
                issue = Issue(
                    id=f"ISSUE-{i}",
                    title=f"Threat in {target}",
                    description=f"Potential malicious pattern detected in {target}",
                    status=IssueStatus.PENDING
                )
                self.state.issues.append(issue)
            
            self.state.processed_count += 1
            self.state.progress = self.state.processed_count / self.state.total_count
            
        self.state.is_running = False
