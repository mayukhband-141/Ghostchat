import curses
import queue

class ChatUI:
    def __init__(self, username):
        self.username = username
        self.messages = []
        self.incoming = queue.Queue()
        self.running = True

    def add_message(self, sender, message):
        self.incoming.put((sender, message))

    def run(self, stdscr, send_callback):
        curses.curs_set(1)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.scrollok(False)

        curses.start_color()
        curses.use_default_colors()

        # Color pairs
        curses.init_pair(1, curses.COLOR_GREEN, -1)   # self
        curses.init_pair(2, curses.COLOR_CYAN, -1)    # peer
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # system
        curses.init_pair(4, curses.COLOR_WHITE, -1)   # input

        stdscr.nodelay(True)

        input_buffer = ""

        while self.running:
            height, width = stdscr.getmaxyx()

            # Drain incoming queue
            while not self.incoming.empty():
                self.messages.append(self.incoming.get())

            # Clear screen safely
            for y in range(height):
                stdscr.move(y, 0)
                stdscr.clrtoeol()

            # Render chat history
            max_lines = height - 2
            start = max(0, len(self.messages) - max_lines)

            y = 0
            for sender, msg in self.messages[start:]:
                if sender == "SYSTEM":
                    color = curses.color_pair(5)
                elif sender == self.username:
                    color = curses.color_pair(1)
                else:
                    color = curses.color_pair(2)

                line = f"[{sender}] {msg}"
                stdscr.addnstr(y, 0, line, width - 1, color)
                y += 1

            # Draw input line (fixed position)
            stdscr.addnstr(height - 1, 0, "> " + input_buffer, width - 1, curses.color_pair(4))
            stdscr.move(height - 1, min(2 + len(input_buffer), width - 1))

            stdscr.refresh()

            try:
                ch = stdscr.getch()
                if ch == -1:
                    continue
                elif ch in (10, 13):  # Enter
                    if input_buffer.strip():
                        send_callback(input_buffer)
                    input_buffer = ""
                elif ch in (8, 127, curses.KEY_BACKSPACE):
                    input_buffer = input_buffer[:-1]
                elif 32 <= ch <= 126:
                    input_buffer += chr(ch)
            except curses.error:
                pass
