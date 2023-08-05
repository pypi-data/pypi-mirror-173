class IdentityException(Exception):
    def __init__(self, message):
        super(IdentityException, self).__init__(message)
