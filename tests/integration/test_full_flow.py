import pytest
import asyncio
from antiminer.app.state.app_state import AppState
from antiminer.app.services.scheduler import Scheduler
from antiminer.app.logic.analyzer import Analyzer
from antiminer.app.logic.fixer import Fixer
from antiminer.app.constants import IssueStatus

@pytest.mark.asyncio
async def test_full_flow():
    state = AppState()
    scheduler = Scheduler()
    analyzer = Analyzer(scheduler, state)
    fixer = Fixer(scheduler, state)
    
    # 1. Run Analysis
    targets = ["test1.exe", "test2.exe"]
    await analyzer.run_analysis(targets)
    
    assert state.processed_count == 2
    assert len(state.issues) > 0
    
    # 2. Run Fix
    await fixer.fix_issues()
    
    # Assert status transitions
    for issue in state.issues:
        assert issue.status in [IssueStatus.FIXED, IssueStatus.FAILED]
    
    assert state.progress == 1.0
