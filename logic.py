class WatchValue:
    def __init__(self, value: any):
        self.value = value

    def check_change(self, value: any):
        if self.value != value:
            return False
        else:
            return True