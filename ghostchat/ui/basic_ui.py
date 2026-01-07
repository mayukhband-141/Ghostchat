def prompt():
    return input("> ")

def display(sender, message):
    print(f"\n[{sender}] {message}")

def system(msg):
    print(f"\n[SYSTEM] {msg}")

def show_history(messages):
    if not messages:
        return

    print("\n--- Last 24h Messages ---")
    for sender, message in messages:
        print(f"[{sender}] {message}")
    print("--- End of History ---\n")
