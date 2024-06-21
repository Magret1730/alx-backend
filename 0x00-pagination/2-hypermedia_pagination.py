#!/usr/bin/env python3
""" Task 0 """
from typing import List, Tuple, Optional, Union, Dict
import csv
import math


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


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieve a specific page of data from the dataset based on pagination
        parameters.

        Args:
            page (int, optional): The page number to retrieve (default is 1).
            page_size (int, optional): The number of items per page
            (default is 10).

        Returns:
            List[List]: A list of lists containing the rows of data for the
            requested page.

            If the requested page is out of range (beyond the dataset's size),
            an empty list is returned.
        """

        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)

        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        page_data = dataset[start_index:end_index]

        return page_data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Retrieve a dataset page and construct a dictionary containing
        hypermedia pagination information.

        Args:
            page (int, optional): The current page number (default is 1).
            page_size (int, optional): The number of items per page
            (default is 10).

        Returns:
            A dictionary containing:
                - 'page_size': Length of the dataset page returned.
                - 'page': Current page number.
                - 'data': Dataset page retrieved.
                - 'next_page': Number of the next page, or None if no
                    next page.
                - 'prev_page': Number of the previous page, or None if no
                    previous page.
                - 'total_pages': Total number of pages in the dataset.
        """
        # Call get_page to retrieve the dataset page
        dataset_page = self.get_page(page, page_size)

        # Calculate page_size
        page_size_value = len(dataset_page)

        # Determine current page
        current_page = page

        # Calculate total number of pages
        total_rows = len(self.dataset())
        total_pages = math.ceil(total_rows / page_size)

        # Calculate next_page and prev_page
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        # Construct the dictionary to return
        hyper_dict = {
            'page_size': page_size_value,
            'page': current_page,
            'data': dataset_page,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }

        return hyper_dict
