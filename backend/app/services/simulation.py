from netra import Netra
from netra.simulation import BaseTask, TaskResult
from typing import Optional
from uuid import uuid4
from agent import get_response

class LoanAgentTask(BaseTask):
    
    def run(self, message: str, session_id: Optional[str] = None) -> TaskResult:
        thread_id = uuid4().hex if not session_id else session_id
    
        Netra.set_session_id(thread_id)

        # Get response from the agent
        try:
            response = get_response(message, thread_id)
            final_message = response
        except Exception as e:
            
            final_message = f"Error: {str(e)}"

        return TaskResult(
            message=final_message,
            session_id=thread_id
        )
    
def run_simulation(dataset_id: str) -> dict | None:
    return Netra.simulation.run_simulation( #type: ignore
        name="Loan Agent Simulation",
        dataset_id=dataset_id,
        task=LoanAgentTask()
    )