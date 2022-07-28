# Hash Chunker

Generator that yields hash chunks for distributed data processing.

### TLDR

```
pip install hash-chunker
```

```
from hash_chunker import HashChunker 

chunks = list(HashChunker().get_chunks(chunk_size=1000, all_items_count=2000))

assert chunks == [("", "8000000000"), ("8000000000", "ffffffffff")]

# use chunks as tasks for multiprocessing 
query_part = "hash > :from_hash AND hash <= :to_hash"
params = {"from_hash": chunk[0], "to_hash": chunk[1]}

```
 
### Description

Imagine a situation when you need to process huge amount data rows in parallel.
Each data row has a hash field and the task is to use it for chunking.

Possible reasons for using hash field and not int id field:
- No auto increment id field.
- Id field has many blank lines (1,2,3, 100500, 100501, 1000000).
- Chunking by id will break data that must be in one chunk to different chunks
(in user behavioral analytics id can be autoincrement for all users actions and
user_session hash is linked to concrete user, so if we chunk by id one user session may
not be in one chunk).
