"""
Canonical RAG evaluation test set.

Each test case pairs a user-style question with the document whose content
should be retrieved. Questions are intentionally phrased without keywords
from the target document — they test semantic retrieval, not keyword matching.

Used by ai_platform.rag.evaluation to compute baseline retrieval metrics.
"""

from ai_platform.rag.schemas import TestCase


TEST_SET: list[TestCase] = [
    TestCase(
        id="q1",
        question="My load balancer started throwing errors after about a year with no config changes — what should I check first?",
        expected_source="ssl_certificate_expiry",
    ),
    TestCase(
        id="q2",
        question="Where do I set up an entry point so clients can reach my backend pool through the load balancer UI?",
        expected_source="f5_virtual_servers",
    ),
    TestCase(
        id="q3",
        question="A single client is hammering my API with thousands of calls per minute. How do I throttle them at the API gateway layer?",
        expected_source="apigee_rate_limiting",
    ),
    TestCase(
        id="q4",
        question="My application is only reachable from within the cluster but not from outside — what type of resource do I need to change?",
        expected_source="k8s_services",
    ),
    TestCase(
        id="q5",
        question="What's the recommended way to store the output of infrastructure-as-code tools when multiple engineers work on the same project?",
        expected_source="terraform_state",
    ),
    TestCase(
        id="q6",
        question="I installed a Python library and it broke another project on my machine. How do I prevent this?",
        expected_source="python_venvs",
    ),
    TestCase(
        id="q7",
        question="I'm building a web API that calls an AI model taking 10 seconds per response. How do I prevent slow calls from blocking other users?",
        expected_source="fastapi_async",
    ),
    TestCase(
        id="q8",
        question="I'm seeing high latency on our load balancer and need to diagnose whether it's a traffic spike issue or a backend problem. What dashboard metrics should I check?",
        expected_source="netscaler_latency",
    ),
    TestCase(
        id="q9",
        question="I'm seeing 502 errors intermittently from my proxy layer — what's a common cause I should check before digging deeper?",
        expected_source="ssl_certificate_expiry",
    ),
]
