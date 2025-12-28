import cv2
import time
from asciimatics.screen import Screen

# ASCII characters used to represent pixel brightness (dark → bright)
ASCII_CHARS = "@%#*+=-:. "

def frame_to_ascii(frame, term_width, term_height):
    """Convert a single video frame to inverted ASCII art stretched to full terminal size."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Stretch frame to exactly terminal size (width × height)
    resized = cv2.resize(gray, (term_width, term_height))

    ascii_frame = []
    for row in resized:
        line_chars = []
        for pixel in row:
            char = ASCII_CHARS[int(pixel) * len(ASCII_CHARS) // 256]
            # invert: spaces become '@', everything else becomes space
            if char == ' ':
                line_chars.append('@')
            else:
                line_chars.append(' ')
        ascii_frame.append("".join(line_chars))

    return "\n".join(ascii_frame)


def play_video(screen):
    cap = cv2.VideoCapture("black_n_white_animation.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps if fps > 0 else 0.03

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Full terminal fill — stretch frame to terminal width × height
        ascii_art = frame_to_ascii(frame, screen.width, screen.height)
        screen.clear_buffer(7, 0, 0)

        for y, line in enumerate(ascii_art.splitlines()):
            screen.print_at(line, 0, y)

        screen.refresh()
        time.sleep(delay)

    cap.release()


if __name__ == "__main__":
    Screen.wrapper(play_video)
