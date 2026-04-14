

def chunk_data(input:str,chunk_size:int = 500,chunk_overlap:int = 50) -> list[str]:
    chunk = []
    if len(input) == 0:
        raise ValueError(f"User input is empty string size {input}")
    if chunk_size <= chunk_overlap:
        raise ValueError(f"overlap is greater than chunks chunk size {chunk_size} ,overlap size {chunk_overlap}")

    for i in range(0,len(input),(chunk_size-chunk_overlap)):
        chunk.append(input[i:i+chunk_size])
    return chunk    

            
        
        