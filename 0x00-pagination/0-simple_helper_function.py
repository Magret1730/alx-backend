#!/usr/bin/env python3
""" Task 0 """
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end indices for items on a given page in
    pagination.

    Args:
        page (int): The current page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index and the end index.
    """
    start_page = (page - 1) * page_size
    end_page = page * page_size

    return (start_page, end_page)
