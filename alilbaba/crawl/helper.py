import winsound


class Notifier:
    @staticmethod
    def beep(frequency=700, duration=1000):
        winsound.Beep(frequency, duration)
