import asyncio
import os
from typing import List, Callable

from antiminer.constants import TaskType, IssueStatus
from antiminer.logic.cpu_tasks import analyze_file_content
from antiminer.logic.models import Issue
from antiminer.services.scheduler import Scheduler


class Analyzer:
    def __init__(self, scheduler: Scheduler, update_state: Callable):
        self.scheduler = scheduler
        self.update_state = update_state

    async def run_analysis(self, targets: List[str], mode: str = "Full Scan"):
        self.update_state(lambda s: s.with_update(
            is_running=True,
            total_count=len(targets),
            processed_count=0,
            issues=[],
            progress=0.0,
            analysis_mode=mode
        ))
        
        for i, target in enumerate(targets):
            # Simulate reading file (IO)
            await asyncio.sleep(0.01)
            
            # CPU-bound analysis
            threat_info = await self.scheduler.schedule(
                TaskType.CPU, 
                analyze_file_content, 
                target,
                mode
            )
            
            if threat_info:
                file_name = os.path.basename(target)
                path = os.path.dirname(target)
                issue = Issue(
                    id=f"ISSUE-{i}",
                    file_name=file_name,
                    path=path,
                    vulnerability=threat_info["name"],
                    description=f"{threat_info['mechanism']} | Рекомендуемое действие: {threat_info['mitigation']}",
                    status=IssueStatus.PENDING
                )
                self.update_state(lambda s: s.with_update(issues=s.issues + [issue]))
            
            self.update_state(lambda s: s.with_update(
                processed_count=s.processed_count + 1,
                progress=(s.processed_count + 1) / s.total_count
            ))
            
        self.update_state(lambda s: s.with_update(is_running=False))
