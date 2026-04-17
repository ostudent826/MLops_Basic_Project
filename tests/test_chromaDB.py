"""
Unit tests for StoreDB (ChromaDB wrapper).
Validates collection initialization, empty input handling, and semantic search functionality.
"""

from ai_platform.rag.rag_db import StoreDB
import pytest


def test_storeDB_collection_input_blank(tmp_path):
    """Ensures a ValueError is raised when adding an empty chunk list."""
    with pytest.raises(ValueError):
        store = StoreDB(db_path=str(tmp_path))
        store.add_data_collection([])


def test_storeDB_query_input_blank(tmp_path):
    """Ensures a ValueError is raised when querying with an empty string."""
    with pytest.raises(ValueError):
        store = StoreDB(db_path=str(tmp_path))
        store.query_data_collection("", 2)


def test_storeDB_functionalty(tmp_path):
    """Tests the full flow of adding documents and retrieving relevant results."""
    store = StoreDB(db_path=str(tmp_path))
    store.add_data_collection(
        [
            "How to configure F5 virtual servers",
            "Python error handling with try except",
            "Network load balancer health checks",
            "Making API calls with FastAPI",
            "Troubleshooting VPN connection timeouts",
            "looking for mr cohen",
            "looking for a brasilo de bryune",
        ]
    )
    results = store.query_data_collection("give me somehting is about name", 2)
    assert "looking for mr cohen" in results["documents"][0]
    assert "looking for a brasilo de bryune" in results["documents"][0]
