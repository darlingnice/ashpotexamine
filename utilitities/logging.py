class LoggingMixin:
    def __init__(self,message) -> None:
        self.message = message
    def log(self):
        print(f"LOG: {self.message}")   