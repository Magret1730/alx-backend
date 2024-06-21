#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Retrieve a page of dataset with deletion-resilient pagination.

        Args:
            index (int, optional): Start index of the page (default is None, which defaults to 0).
            page_size (int, optional): Number of items per page (default is 10).

        Returns:
            Dict: Dictionary with keys:
                - 'index': Start index of the returned page.
                - 'next_index': Index of the first item after the last item on the current page.
                - 'page_size': Current page size.
                - 'data': Actual page of the dataset.
        """
        # Ensure index is within valid range or default to 0 if None
        assert index is None or (isinstance(index, int) and 0 <= index < len(self.indexed_dataset())), "Index out of range."

        if index is None:
            index = 0

        # Calculate next index to query
        next_index = index + page_size

        # Retrieve the dataset
        dataset = self.indexed_dataset()

        # Get the data for the current page
        data = [dataset[i] for i in range(index, min(index + page_size, len(dataset)))]

        return {
            'index': index,
            'next_index': next_index,
            'page_size': page_size,
            'data': data
        }

