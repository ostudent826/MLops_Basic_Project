from .schemas import TestCase, EvalResult, FailureDetail
from .pipeline import store_client

"""
RAG evaluation module.

Measures retrieval accuracy by running test cases through the pipeline
and checking whether expected sources appear in the top-N results.
"""


def evaluate(test_set: list[TestCase], n_results: int = 3) -> EvalResult:
    """
    Run every test case through the retrieval pipeline and report how often
    the expected source was retrieved in the top-N results.

    Args:
        test_set: The evaluation test cases to run.
        n_results: How many top chunks to consider for each query (the N in recall@N).

    Returns:
        EvalResult with aggregate counts, recall score, and IDs of failed tests.
    """

    failed = 0
    passed = 0
    failed_test_ids = []

    for test_case in test_set:
        result = store_client.query_data_collection(
            test_case.question, n_results=n_results
        )
        metadatas = result["metadatas"][0]
        retrieved_sources = [chunk["source"] for chunk in metadatas]

        if any(source == test_case.expected_source for source in retrieved_sources):
            passed += 1
        else:
            failed += 1
            failed_test_ids.append(
                FailureDetail(
                    test_id=test_case.id,
                    question=test_case.question,
                    expected_source=test_case.expected_source,
                    retrieved_sources=retrieved_sources,
                )
            )

    return EvalResult(
        total=len(test_set),
        passed=passed,
        failed=failed,
        recall_at_n=passed / len(test_set) if test_set else 0.0,
        n_results=n_results,
        failures=failed_test_ids,
    )
