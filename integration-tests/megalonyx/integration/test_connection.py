import socket
import sys


def test_connection(host: str, port: int) -> bool:
    print(f"Attempting to connect to {host}:{port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        print(f"Successfully connected to {host}:{port}")
        s.close()
        return True
    except OSError as e:
        print(f"Failed to connect to {host}:{port}: {e}")
        return False


if __name__ == "__main__":
    success = True
    success &= test_connection("127.0.0.1", 6333)
    success &= test_connection("0.0.0.0", 6333)
    success &= test_connection("192.168.1.104", 6333)

    if success:
        print("All connection attempts succeeded.")
        sys.exit(0)
    else:
        print("Some connection attempts failed.")
        sys.exit(1)
