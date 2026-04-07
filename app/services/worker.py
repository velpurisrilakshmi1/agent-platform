"""Worker agent for executing tasks."""

from typing import Any

from app.models import Task, TaskResult, TaskStatus, TaskType
from app.storage.task_store import TaskStore
from app.services.mcp_client import get_mcp_client
from app.services.rai import get_rai_service


class WorkerAgent:
    """Executes individual tasks and returns results."""
    
    def __init__(self, task_store: TaskStore, use_mcp: bool = True):
        self.task_store = task_store
        self.use_mcp = use_mcp
        self._context: dict[str, Any] = {}  # Shared context between tasks
    
    def execute(self, task: Task) -> TaskResult:
        """
        Execute a task and return the result.
        
        Routes to the appropriate handler based on task type.
        """
        # Update task status to running
        self.task_store.update_task_status(task.id, TaskStatus.RUNNING)
        
        try:
            # Route to appropriate handler
            match task.type:
                case TaskType.FETCH_CONTEXT:
                    result = self._handle_fetch_context(task)
                case TaskType.PROCESS:
                    result = self._handle_process(task)
                case TaskType.VALIDATE:
                    result = self._handle_validate(task)
                case _:
                    result = TaskResult(
                        task_id=task.id,
                        success=False,
                        error=f"Unknown task type: {task.type}"
                    )
            
            # Update task with result
            if result.success:
                task.status = TaskStatus.COMPLETED
                task.output = result.output
            else:
                task.status = TaskStatus.FAILED
                task.error = result.error
            
            self.task_store.update_task(task)
            return result
            
        except Exception as e:
            # Handle unexpected errors
            result = TaskResult(
                task_id=task.id,
                success=False,
                error=str(e)
            )
            task.status = TaskStatus.FAILED
            task.error = str(e)
            self.task_store.update_task(task)
            return result
    
    def _handle_fetch_context(self, task: Task) -> TaskResult:
        """
        Fetch context for the job.
        
        Uses MCP server when available, falls back to mock data.
        """
        query = task.input.get("query", "")
        
        if self.use_mcp:
            try:
                # Fetch context from MCP server
                mcp_client = get_mcp_client()
                context = mcp_client.get_context_sync(query)
                context["source"] = "mcp"
            except Exception as e:
                # Fall back to mock if MCP fails
                context = {
                    "query": query,
                    "context": f"Mock context for query: {query}",
                    "source": "mock_fallback",
                    "mcp_error": str(e)
                }
        else:
            # Mock context data
            context = {
                "query": query,
                "context": f"Mock context for query: {query}",
                "source": "mock"
            }
        
        # Store context for subsequent tasks
        self._context["fetched"] = context
        
        return TaskResult(
            task_id=task.id,
            success=True,
            output=context
        )
    
    def _handle_process(self, task: Task) -> TaskResult:
        """
        Process the input using fetched context.
        
        MVP: Returns mock processed output.
        Later: Could use LLM or other processing.
        """
        context = self._context.get("fetched", {})
        query = context.get("query", "unknown")
        
        # Mock processing
        processed = {
            "result": f"Processed result for: {query}",
            "input_context": context.get("context", ""),
            "processing_status": "completed"
        }
        
        # Store for validation
        self._context["processed"] = processed
        
        return TaskResult(
            task_id=task.id,
            success=True,
            output=processed
        )
    
    def _handle_validate(self, task: Task) -> TaskResult:
        """
        Validate the processed output.
        
        MVP: Returns mock validation result.
        Later: Will call RAI service.
        """
        processed = self._context.get("processed", {})
        
        # Mock validation (always passes for now)
        validation = {
            "validated": True,
            "validation_notes": "Mock validation passed",
            "final_output": processed.get("result", ""),
        }
        
        self._context["validated"] = validation
        
        return TaskResult(
            task_id=task.id,
            success=True,
            output=validation
        )
    
    def execute_all(self, tasks: list[Task]) -> list[TaskResult]:
        """Execute a list of tasks in sequence."""
        results = []
        for task in tasks:
            result = self.execute(task)
            results.append(result)
            
            # Stop execution if a task fails
            if not result.success:
                break
        
        return results
    
    def get_final_output(self) -> dict[str, Any]:
        """Get the final validated output."""
        return self._context.get("validated", {})
