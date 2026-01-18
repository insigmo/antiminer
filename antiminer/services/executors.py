import os
from concurrent.futures import ProcessPoolExecutor

class ExecutorManager:
    _cpu_executor: ProcessPoolExecutor = None

    @classmethod
    def get_cpu_executor(cls) -> ProcessPoolExecutor:
        if cls._cpu_executor is None:
            max_workers = max(1, (os.cpu_count() or 1) - 1)
            cls._cpu_executor = ProcessPoolExecutor(max_workers=max_workers)
        return cls._cpu_executor

    @classmethod
    def shutdown(cls):
        if cls._cpu_executor:
            cls._cpu_executor.shutdown(wait=True)
            cls._cpu_executor = None
