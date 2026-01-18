import asyncio
from typing import List, Callable
from antiminer.logic.models import Issue, AppState
from antiminer.constants import TaskType, IssueStatus
from antiminer.logic.cpu_tasks import analyze_file_content
from antiminer.services.scheduler import Scheduler

class Analyzer:
    def __init__(self, scheduler: Scheduler, update_state: Callable):
        self.scheduler = scheduler
        self.update_state = update_state

    async def run_analysis(self, targets: List[str]):
        self.update_state(lambda s: s.with_update(
            is_running=True,
            total_count=len(targets),
            processed_count=0,
            issues=[],
            progress=0.0
        ))
        
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
                self.update_state(lambda s: s.with_update(issues=s.issues + [issue]))
            
            self.update_state(lambda s: s.with_update(
                processed_count=s.processed_count + 1,
                progress=(s.processed_count + 1) / s.total_count
            ))
            
        self.update_state(lambda s: s.with_update(is_running=False))
