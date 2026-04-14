from ai_platform.rag.chunker import chunk_data
import pytest
   
def test_chunk_data():
    result = chunk_data("abcdefghijklmnopqrst",10,2) 
    assert result[0] == "abcdefghij"
    assert result[1] == "ijklmnopqr"
    assert result [2] == "qrst"

def test_chunk_data_input_blank():
    with pytest.raises(ValueError):
        chunk_data("")

def test_chunk_data_overlap_size():
    with pytest.raises(ValueError):
        chunk_data("Hi just testing overlap",50,150)
