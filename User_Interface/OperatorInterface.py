class OperatorInterface:
    def __init__(self):
        self._voiceInput = None

    def getVoiceInput(self):
        return self._voiceInput

    def setVoiceInput(self, value):
        self._voiceInput = value

    def inputMapData(self):
        pass

    def captureVoiceInput(self):
        pass