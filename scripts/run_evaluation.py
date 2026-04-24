from ai_platform.rag.evaluation import evaluate
from ai_platform.rag.test_set import TEST_SET

if __name__ == "__main__":
    result = evaluate(TEST_SET, 1)
    print("RAG Evaluation Results")
    print("=" * 30)
    print(f"Total tests: {result.total}")
    print(f"Passed:      {result.passed}")
    print(f"Failed:      {result.failed}")
    print(f"Recall@{result.n_results}:    {result.recall_at_n * 100:.1f}%")
    print()
    print("Failed tests:")
    id_to_test_case = {tc.id: tc for tc in TEST_SET}
    if result.failures:
        for f in result.failures:
            print(f'  - {f.test_id}: "{f.question}"')
            print(f"       Expected: {f.expected_source}")
            print(f"       Got:      {f.retrieved_sources}")
    else:
        print("  (none)")
