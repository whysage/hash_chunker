"""Tests."""
from typing import List, Tuple

import pytest

from hash_chunker import HashChunker


@pytest.mark.parametrize(
    "chunk_size, all_items_count, expected",
    [
        (1000, 2000, [("", "8000000000"), ("8000000000", "ffffffffff")]),
        (
            500,
            1500,
            [
                ("", "5555600000"),
                ("5555600000", "aaaac00000"),
                ("aaaac00000", "ffffffffff"),
            ],
        ),
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
    assert list(HashChunker().get_chunks(chunk_size, all_items_count)) == expected


@pytest.mark.parametrize(
    "chunk_size, all_items_count, chunk_hash_length, expected",
    [
        (1, 2, 5, [("", "80000"), ("80000", "fffff")]),
    ],
)
def test_chunk_hash_length(
    chunk_size: int,
    all_items_count: int,
    chunk_hash_length: int,
    expected: List[Tuple[str, str]],
) -> None:
    """
    Test chunk_hash_length option.

    :param chunk_size: chunk elements limit
    :param all_items_count: count aff all data elements
    :param chunk_hash_length: chunks hash length
    :param expected: expected chunks
    """
    hash_chunker = HashChunker(chunk_hash_length=chunk_hash_length)
    assert list(hash_chunker.get_chunks(chunk_size, all_items_count)) == expected


@pytest.mark.parametrize(
    "chunks_count, expected",
    [
        (2, [("", "8000000000"), ("8000000000", "ffffffffff")]),
        (
            3,
            [
                ("", "5555600000"),
                ("5555600000", "aaaac00000"),
                ("aaaac00000", "ffffffffff"),
            ],
        ),
    ],
)
def test_get_fixed_chunks(
    chunks_count: int,
    expected: List[Tuple[str, str]],
) -> None:
    """
    Simple test.

    :param chunks_count: chunks limit
    :param expected: expected chunks
    """
    assert list(HashChunker().get_fixed_chunks(chunks_count)) == expected


@pytest.mark.parametrize(
    "chunk_size, all_items_count",
    [
        ("1", 1),
        (1, 5.45),
        (0, -2),
        (18, -20),
    ],
)
def test_get_chunks_validate(
    chunk_size: int,
    all_items_count: int,
) -> None:
    """
    Simple test.

    :param chunk_size: chunk elements limit
    :param all_items_count: count aff all data elements
    :raises: ValueError if chunk_size is less than 1
             or all_items_count is less than 0,
             TypeError if chunk_size or all_items_count is not an integer
    """
    with pytest.raises((TypeError, ValueError)):
        list(HashChunker().get_chunks(chunk_size, all_items_count))


@pytest.mark.parametrize(
    "chunks_count",
    [
        ("5",),
        (5.45,),
        (0,),
        (-12,),
    ],
)
def test_get_fixed_chunks_validate(
    chunks_count: int,
) -> None:
    """
    Simple test.

    :param chunks_count: chunks limit
    :raises: ValueError if chunks_count is less than 1
             or TypeError if chunks_count is not an integer
    """
    with pytest.raises((TypeError, ValueError)):
        list(HashChunker().get_fixed_chunks(chunks_count))
