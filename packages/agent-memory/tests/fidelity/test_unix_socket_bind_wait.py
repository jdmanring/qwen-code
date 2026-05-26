import os
import socket
import time

path = os.path.join(os.path.expanduser("~"), ".local/share/megalonyx/sockets/megalonyx_memory.sock")
print(f"Attempting to bind to: {os.path.abspath(path)}")

if os.path.exists(path):
    print("Path exists. Removing it.")
    os.remove(path)

try:
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(path)
    print("Bind successful!")
    server.listen(1)
    print("Listen successful! Waiting 10 seconds...")
    time.sleep(10)
    server.close()
    print("Closed.")
except OSError as e:
    print(f"Error: {e}")
