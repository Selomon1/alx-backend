#!/usr/bin/env python3
"""
Simple helper function for pagination.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Return a tuple of start and end index for pagination.
    Args:
        page (int): the current page.
        page_size (int): the number of items per page.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index
