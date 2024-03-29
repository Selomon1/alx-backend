#!/usr/bin/env python3
"""
module containing a Server class for pagination of a dataset.
"""

import csv
import math
from typing import Tuple, List, Union, Optional, Dict


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
        """ Returns the specified page of the dataset """
        assert isinstance(page, int) and page > 0, \
            "page must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0, \
            "page_size must be a positive integer"

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()
        return dataset[start_index:end_index]

    def get_hyper(
        self,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Union[int, List[List[str]], Optional[int]]]:
        """
        Returns hypermedia pagination details.
        Args:
            page (int): the current page number
            page_size (int): the number of items per page
        """
        page_data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            'page_size': len(page_data),
            'page': page,
            'data': page_data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
