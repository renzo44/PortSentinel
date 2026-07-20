import socket

from services import get_service


def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    resultado = s.connect_ex((ip, port))

    s.close()

    return resultado == 0

def get_generic_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((ip, port))

        banner = s.recv(1024).decode(errors="ignore")

        s.close()

        return banner.strip()

    except Exception:
        return "N/A"

def get_http_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((ip, port))

        request = (
            f"HEAD / HTTP/1.1\r\n"
            f"Host: {ip}\r\n"
            "Connection: close\r\n\r\n"
        )

        s.send(request.encode())

        response = s.recv(1024).decode(errors="ignore")

        s.close()

        for line in response.splitlines():
            if line.lower().startswith("server:"):
                return line.replace("Server:", "").strip()

        return response.splitlines()[0].strip()

    except Exception:
        return "N/A"

def get_banner(ip, port):

    if port in (80, 8000, 8080):
        return get_http_banner(ip, port)

    return get_generic_banner(ip, port)

def scan_range(ip, puerto_inicial, puerto_final):

    print("PORT     STATUS   SERVICE     BANNER")
    print("-" * 50)

    for puerto in range(puerto_inicial, puerto_final + 1):

        if scan_port(ip, puerto):
            service = get_service(puerto)
            banner = get_banner(ip, puerto)

            print(f"{puerto:<8} OPEN     {service:<10} {banner}")