from agent import get_response
from netra import Netra
from uuid import uuid4

def run_evaluation(dataset_id: str) -> dict | None:
    dataset = Netra.evaluation.get_dataset(dataset_id) #type: ignore

    return Netra.evaluation.run_test_suite( #type: ignore
        name="Loan Agent Single Turn",
        data=dataset,
        task=lambda message: get_response(message, thread_id=uuid4().hex)
    )