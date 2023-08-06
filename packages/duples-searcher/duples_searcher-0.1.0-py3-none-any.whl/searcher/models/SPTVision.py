from searcher.enums.Code import Code
from searcher.models.ITechnialVision import ITechnicalVision
from typing import List
import csv

class SPTVision(ITechnicalVision):
    """SPTVision technical vision class

    Args:
        ITechnicalVision (class): Technical vision super class
    """    

    def _csv_parser(self, file: str):
        """Parser for txt file

        Args:
            file (str): file to parse

        Returns:
            List[Code]: parsed_codes
        """
        data: List[Code] = []
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for i, row in enumerate(reader):
                transformed_row = row
                if transformed_row[4] != '':
                    code = Code(code=transformed_row[4],
                                date=transformed_row[0],
                                time=transformed_row[1],
                                id=transformed_row[2])
                    data.append(code)
        return data
    
    def _txt_parser(self, file):        
        raise NotImplementedError("Not implemented")