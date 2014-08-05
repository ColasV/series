class BetaSeriesError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class BetaSeriesAPIError(Exception):
    pass

class ConnectionError(BetaSeriesError):
    pass


class DownloadingError(BetaSeriesError):
    pass


class ExtractingError(BetaSeriesError):
    pass