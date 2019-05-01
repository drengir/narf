import time

class Nfc():

    def __init__(self):
        self.is_empty = False

    def get_id(self):
        """ Toggles between mock and empty id """
        time.sleep(5.0)

        if self.is_empty:
            self.is_empty = not self.is_empty
            return None
        return 'mock_id'
