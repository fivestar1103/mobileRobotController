from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Hazard import Hazard


class VoiceInputHandler:
    def receive_voice_input(self):
        print("[Voice Input Handler]: 🎙️Voice recognition successful...")
        newPoints = [
            Hazard(1, 5, True),
            Hazard(0, 4, True),
            ColorBlob(0, 6, True),
            ColorBlob(5, 1, True),
        ]
        return newPoints

    def process_voice_command(self):
        pass