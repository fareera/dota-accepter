import signal
import sys
import time
from config import load_config
from detector import Detector
from clicker import Clicker
from notifier import WeChatNotifier


def main():
    config = load_config()

    detector = Detector(
        template_path="templates/accept_button.png",
        threshold=config["match_threshold"],
    )
    clicker = Clicker(cooldown_seconds=config["cooldown_seconds"])
    notifier = WeChatNotifier(
        app_id=config["wechat"]["app_id"],
        app_secret=config["wechat"]["app_secret"],
        template_id=config["wechat"]["template_id"],
        user_openid=config["wechat"]["user_openid"],
    )

    running = True

    def on_exit(sig, frame):
        nonlocal running
        print("\nShutting down...")
        running = False

    signal.signal(signal.SIGINT, on_exit)

    print("Dota 2 Auto Accept started. Press Ctrl+C to stop.")

    while running:
        if clicker.is_cooling_down():
            time.sleep(1)
            continue

        detected, x, y = detector.detect()

        if detected:
            print(f"[{time.strftime('%H:%M:%S')}] Match found! Clicking accept at ({x}, {y})...")
            clicked = clicker.click(x, y)
            if clicked:
                print(f"[{time.strftime('%H:%M:%S')}] Accepted! Sending notification...")
                sent = notifier.send("Dota 2 match has been auto-accepted")
                if sent:
                    print(f"[{time.strftime('%H:%M:%S')}] WeChat notification sent.")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] WeChat notification failed (match still accepted).")
                print(f"[{time.strftime('%H:%M:%S')}] Cooldown {config['cooldown_seconds']}s...")
        else:
            time.sleep(config["scan_interval"])


if __name__ == "__main__":
    main()
