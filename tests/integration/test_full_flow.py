import pytest
import asyncio
from antiminer.logic.models import AppState
from antiminer.services.scheduler import Scheduler
from antiminer.logic.analyzer import Analyzer
from antiminer.logic.fixer import Fixer
from antiminer.constants import IssueStatus

@pytest.mark.asyncio
async def test_full_flow():
    state = AppState()
    
    def update_state(fn):
        nonlocal state
        state = fn(state)

    scheduler = Scheduler()
    analyzer = Analyzer(scheduler, update_state)
    fixer = Fixer(scheduler, update_state)
    
    # 1. Run Analysis
    targets = ["test1.exe", "test2.exe"]
    await analyzer.run_analysis(targets)
    
    assert state.processed_count == 2
    assert len(state.issues) > 0
    
    # 2. Run Fix
    await fixer.fix_issues(state)
    
    # Assert status transitions
    for issue in state.issues:
        assert issue.status in [IssueStatus.FIXED, IssueStatus.FAILED]
    
    assert state.progress == 1.0
