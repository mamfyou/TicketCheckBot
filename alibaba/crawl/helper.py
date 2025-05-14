import os
import platform


class Notifier:
    @staticmethod
    def beep(frequency=700, duration=1000):
        system = platform.system()

        if system == 'Windows':
            import winsound
            winsound.Beep(frequency, duration)
        elif system == 'Darwin':  # macOS
            os.system(f"osascript -e 'beep {frequency}'")
        elif system == 'Linux':
            os.system(f"beep -f {frequency} -l {duration}")
        else:
            print("Unsupported platform")
