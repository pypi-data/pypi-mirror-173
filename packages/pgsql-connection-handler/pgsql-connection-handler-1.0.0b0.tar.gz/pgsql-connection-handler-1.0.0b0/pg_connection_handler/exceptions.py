
class ConnectionDoesNotExist(Exception):
    """
    Raised when a database does not exist in the db registry.
    """
    def __init__(self, db_alias):
        self.message = (
            f"Database with alias '{db_alias}' does not exist in registry."
        )
        super().__init__(self.message)



class ImproperlyConfigured(Exception):
    """
    Raised when something is misconfigured.
    """
    pass
