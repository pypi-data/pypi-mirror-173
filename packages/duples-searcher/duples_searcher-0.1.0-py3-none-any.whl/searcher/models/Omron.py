from searcher.models.ITechnialVision import ITechnicalVision


class Omron(ITechnicalVision):
    """Omron technical vision class

    Args:
        ITechnicalVision (class): Technical vision super class
    """

    def _csv_parser(self, file):
        """Csv parser for Omron

        Args:
            file (str): file to parse

        Raises:
            NotImplementedError: For not implemented
        """        
        raise NotImplementedError("Not implemented")

    def _txt_parser(self, file):
        raise NotImplementedError("Not implemented")
