class ValidationError(Exception):
    def __init__(self, errors: list[str]):
        self.message = "\n".join(errors)
        super().__init__(self.message)
