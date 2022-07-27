"""Hash Chunker helper to provide hash ranges for distributed data processing."""
import math
from typing import List, Tuple


class HashChunker(object):
    """Main module class."""

    hex_base = 16
    hex_zero = "0"
    hex_f = "f"
    hex_format = "x"

    def __init__(
        self,
        chunk_hash_length: int = 10,
        hash_ranges_accuracy: int = 5,
        hash_max_length: int = 32,
    ):
        """
        Init HashChunker.

        :param chunk_hash_length: length of results chunks hashes
        :param hash_ranges_accuracy: accuracy for chunks calculation
        :param hash_max_length: hash string length in data
        """
        self.chunk_hash_length = chunk_hash_length
        self.hash_ranges_accuracy = hash_ranges_accuracy
        self.hash_max_length = hash_max_length

    def get_chunks(
        self,
        chunk_size: int,
        all_items_count: int,
    ) -> List[Tuple[str, str]]:
        """
        Return hash ranges.

        :param chunk_size: chunk elements limit
        :param all_items_count: count aff all data elements
        :return: list of chunks
        """
        if all_items_count == 0 or chunk_size == 0:
            return []
        (
            all_items_count,
            chunk_size,
            current_position,
            previous_position,
        ) = self._get_positions(all_items_count, chunk_size)
        return self._add_ranges(
            all_items_count,
            chunk_size,
            current_position,
            previous_position,
        )

    def _add_ranges(
        self,
        all_items_count: int,
        batch: int,
        current_position: int,
        previous_position: int,
    ) -> List[Tuple[str, str]]:
        ranges = []
        while current_position < all_items_count:
            start = self._position_to_hex(previous_position)
            stop = self._position_to_hex(current_position)
            ranges.append(
                (
                    start[: self.chunk_hash_length],
                    stop[: self.chunk_hash_length],
                ),
            )
            previous_position = current_position
            current_position += batch
        start = self._position_to_hex(previous_position)
        stop = self.hex_f * self.hash_max_length
        ranges.append(
            (start[: self.chunk_hash_length], stop[: self.chunk_hash_length]),
        )
        return ranges

    def _get_positions(
        self,
        all_items_count: int,
        batch_limit: int,
    ) -> Tuple[int, int, int, int]:
        scale = self.hex_base**self.hash_ranges_accuracy / all_items_count
        batch_limit = math.ceil(batch_limit * scale)
        all_items_count *= scale
        previous_position = 0
        current_position = batch_limit
        return (
            all_items_count,
            batch_limit,
            current_position,
            previous_position,
        )

    def _position_to_hex(self, position: int) -> str:
        hexed = format(position, self.hex_format)
        if len(hexed) < self.hash_ranges_accuracy:
            zeros_count = self.hash_ranges_accuracy - len(hexed)
            hexed = self.hex_zero * zeros_count + hexed
        hexed += self.hex_zero * (self.hash_max_length - len(hexed))
        return hexed
