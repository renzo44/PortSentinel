import socket

from services import get_service


def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    resultado = s.connect_ex((ip, port))

    s.close()

    return resultado == 0


def get_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((ip, port))

        banner = s.recv(1024).decode(errors="ignore")

        s.close()

        return banner.strip()

    except:
        return "N/A"

def scan_range(ip, puerto_inicial, puerto_final):

    print("PORT     STATUS   SERVICE     BANNER")
    print("-" * 50)

    for puerto in range(puerto_inicial, puerto_final + 1):

        if scan_port(ip, puerto):
            service = get_service(puerto)
            banner = get_banner(ip, puerto)

            print(f"{puerto:<8} OPEN     {service:<10} {banner}")