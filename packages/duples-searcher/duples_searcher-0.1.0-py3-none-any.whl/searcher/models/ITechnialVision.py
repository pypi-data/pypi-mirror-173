from searcher.enums.Code import Code
from searcher.enums.Duplicate import Duplicate, DuplicateStatus
from pathlib import Path
from typing import Dict, List
import json


class ITechnicalVision:
    """Technical Vision super class

    """

    def __init__(self):
        self._data_info: List[Code] = []
        self._duplicates: Dict[str, List[Duplicate]] = {}

    def _txt_parser(self, file: str):
        """Txt parser for technial vision

        Args:
            file (str): file to parse

        Returns:
            List[Code]: list of codes
        """
        raise NotImplementedError("Not implemented")

    def _csv_parser(self, file: str):
        """csv parser for technial vision

        Args:
            file (str): file to parse

        Returns:
            List[Code]: list of codes
        """
        raise NotImplementedError("Not implemented")

    def get_data_from_file(self, file: str):
        """Gets data from file and parse it and writes to local variable

        Args:
            file (str): file to read
        """
        self._data_info = self.parse_data(file)

    def parse_data(self, file: str):
        """Parses data from file and returns list of Codes

        Args:
            file (str): file to parse

        Returns:
            List[Code]: parsed codes
        """
        extension = Path(file).suffix
        if extension == '.txt':
            return self._txt_parser(file)
        if extension == '.csv':
            return self._csv_parser(file)
        raise ValueError('File extension not supported')

    def search_duplicates(self):
        """Searchs duplicates through codes list and writes to local variable
        """
        duplicates = {}
        codesMap = {}
        for elem in self._data_info:
            if elem.code in codesMap:
                duplicateModel = Duplicate(code=elem.code,
                                           date=elem.date,
                                           time=elem.time,
                                           id=elem.id,
                                           status=DuplicateStatus.DUPLICATE)
                if elem.code not in duplicates:
                    firstCode = Duplicate(code=elem.code,
                                          date=elem.date,
                                          time=elem.time,
                                          id=elem.id,
                                          status=DuplicateStatus.NOT_DUPLICATE)

                    duplicates[elem.code] = []
                    duplicates[elem.code].append(firstCode.dict())
                    duplicates[elem.code].append(duplicateModel.dict())
                else:
                    duplicates[elem.code].append(duplicateModel.dict())
            else:
                codesMap[elem.code] = elem.id
        self._duplicates = duplicates

    def write_duplicates_to_file(self, file: str):
        """Writes duplicates to files if duplicates exists

        Args:
            file (str): file to write
        """
        if len(self._duplicates) < 1:
            raise Exception("No duplicates found")
        with open(file, 'w') as f:
            f.write(json.dumps(self._duplicates, indent=4, sort_keys=True))

    @property
    def duplicates(self):
        """Returns duplicates that have been founed

        Returns:
            Dict[str, List[Duplicate]]: duplicates info
        """
        return self._duplicates
