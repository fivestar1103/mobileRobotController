class OperatorInterface:
    def __init__(self):
        self._voiceInput = None

    def get_voice_input(self):
        return self._voiceInput

    def set_voice_input(self, value):
        self._voiceInput = value

    def input_map_data(self):
        pass

    def capture_voice_input(self):
        pass