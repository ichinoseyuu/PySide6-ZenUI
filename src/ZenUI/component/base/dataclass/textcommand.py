class ZTextCommand:
    def __init__(self, old_text: str, new_text: str, old_pos: int, new_pos: int):
        self.old_text = old_text
        self.new_text = new_text
        self.old_pos = old_pos
        self.new_pos = new_pos