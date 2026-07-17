import socket

from services import get_service


def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    resultado = s.connect_ex((ip, port))

    s.close()

    return resultado == 0


def scan_range(ip, puerto_inicial, puerto_final):

    print("PORT     STATUS   SERVICE")
    print("-" * 30)

    for puerto in range(puerto_inicial, puerto_final + 1):

        if scan_port(ip, puerto):
            service = get_service(puerto)
            print(f"{puerto:<8} OPEN     {service}")