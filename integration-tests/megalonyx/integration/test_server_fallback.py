import socket


def start_server(port: int) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", port))
            s.listen()
            print(f"Server listening on 0.0.0.0:{port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(b"Hello from dummy server\n")
    except OSError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    start_server(6335)
