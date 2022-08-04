"""Hash Chunker helper to provide hash ranges for distributed data processing."""
import math
from dataclasses import dataclass
from typing import Generator, Tuple


@dataclass
class HashChunker(object):
    """Main class."""

    chunk_hash_length: int = 10
    hash_ranges_accuracy: int = 5
    hash_max_length: int = 32
    hex_base: int = 16
    hex_zero: str = "0"
    hex_f: str = "f"
    hex_format: str = "x"

    def get_chunks(  # noqa: WPS463
        self,
        chunk_size: int,
        all_items_count: int,
    ) -> Generator[Tuple[str, str], None, None]:
        """
        Return hash chunks.

        :param chunk_size: chunk elements limit
        :param all_items_count: count aff all data elements
        :yield: сhunks
        """
        if all_items_count == 0 or chunk_size == 0:
            return
        (
            all_items_count,
            chunk_size,
            current_position,
            previous_position,
        ) = self._get_positions(all_items_count, chunk_size)
        yield from self._add_ranges(
            all_items_count,
            chunk_size,
            current_position,
            previous_position,
        )

    def _add_ranges(
        self,
        all_items_count: int,
        chunk_size: int,
        current_position: int,
        previous_position: int,
    ) -> Generator[Tuple[str, str], None, None]:
        while current_position < all_items_count:
            if previous_position:
                start = self._position_to_hex(previous_position)
            else:
                start = ""
            stop = self._position_to_hex(current_position)
            yield start, stop
            previous_position = current_position
            current_position += chunk_size
        start = self._position_to_hex(previous_position)
        stop = self.hex_f * self.chunk_hash_length
        yield start, stop

    def _get_positions(
        self,
        all_items_count: int,
        chunk_limit: int,
    ) -> Tuple[int, int, int, int]:
        scale = self.hex_base**self.hash_ranges_accuracy / all_items_count
        chunk_limit = math.ceil(chunk_limit * scale)
        all_items_count *= scale
        previous_position = 0
        current_position = chunk_limit
        return (
            all_items_count,
            chunk_limit,
            current_position,
            previous_position,
        )

    def _position_to_hex(self, position: int) -> str:
        hexed = format(position, self.hex_format)
        if len(hexed) < self.hash_ranges_accuracy:
            zeros_count = self.hash_ranges_accuracy - len(hexed)
            hexed = self.hex_zero * zeros_count + hexed
        hexed += self.hex_zero * (self.hash_max_length - len(hexed))
        return hexed[: self.chunk_hash_length]
