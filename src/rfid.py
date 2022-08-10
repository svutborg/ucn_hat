from typing import Tuple
from mfrc522 import SimpleMFRC522, MFRC522

class Rfid(SimpleMFRC522):

    def __init__(self, device: int = 0) -> None:
        self.READER = MFRC522(device = device)

    def read_tag(self) -> Tuple:
        id = None
        text = None 
        try:
            id, text = self.read()
        finally:
            return (id, text)

    def write_tag(self, text: str = ""):
        self.write(text)


if __name__ == "__main__":
    reader = Rfid(device = 1)
    reader.write_tag("Test")
    print(reader.read_tag())
