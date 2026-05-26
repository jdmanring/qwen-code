import json
import os
import socket

SOCKET_PATH = os.path.join(
    os.path.expanduser("~"), ".local/share/megalonyx/sockets/megalonyx_memory.sock"
)


def test_socket():
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(SOCKET_PATH)

            # JSON-RPC initialize request
            request = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}

            client.sendall((json.dumps(request) + "\n").encode("utf-8"))

            response_data = client.recv(4096).decode("utf-8")
            print(f"Response: {response_data}")

            response = json.loads(response_data)
            if response.get("result"):
                print("SUCCESS: Received valid initialization response.")
            else:
                print("FAILURE: Invalid response.")

    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    test_socket()
