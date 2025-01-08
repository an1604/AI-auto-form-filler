class AppliedSuccessfullyException(Exception):
    def __init__(self, message="Job applied from server!", field_name=None):
        super().__init__(message)

    def __str__(self):
        return self.args[0]
