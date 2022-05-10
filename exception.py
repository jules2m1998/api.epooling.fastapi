class NotFound404(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        salary -- input salary which caused the error
        message -- explanation of the error
    """

    def __init__(self, message="404 element not found !"):
        self.message = message
        super().__init__(self.message)