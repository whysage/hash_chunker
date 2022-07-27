"""Tests."""
from typing import List, Tuple

import pytest

from hash_chunker import HashChunker


@pytest.mark.parametrize(
    "chunk_size, all_items_count, expected",
    [
        (1, 2, [("0000000000", "8000000000"), ("8000000000", "ffffffffff")]),
    ],
)
def test_default_usage(
    chunk_size: int,
    all_items_count: int,
    expected: List[Tuple[str, str]],
) -> None:
    """
    Simple test.

    :param chunk_size: chunk elements limit
    :param all_items_count: count aff all data elements
    :param expected: expected chunks
    """
    assert HashChunker().get_chunks(chunk_size, all_items_count) == expected


@pytest.mark.parametrize(
    "chunk_size, all_items_count, chunk_hash_length, expected",
    [
        (1, 2, 5, [("00000", "80000"), ("80000", "fffff")]),
    ],
)
def test_hash_length(
    chunk_size: int,
    all_items_count: int,
    chunk_hash_length: int,
    expected: List[Tuple[str, str]],
) -> None:
    """
    Simple test.

    :param chunk_size: chunk elements limit
    :param all_items_count: count aff all data elements
    :param chunk_hash_length: chunks hash length
    :param expected: expected chunks
    """
    hash_chunker = HashChunker(chunk_hash_length=chunk_hash_length)
    assert hash_chunker.get_chunks(chunk_size, all_items_count) == expected
