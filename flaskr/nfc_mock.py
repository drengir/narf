import time

class Nfc():

    def __init__(self):
        self.is_empty = True

    def get_id(self):
        """ Toggles between mock and empty id """
        time.sleep(5.0)
        self.is_empty = not self.is_empty

        if self.is_empty:
            return None
        return 'mock_id'
