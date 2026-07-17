from utils import (
    mostrar_banner,
    pedir_ip,
    pedir_puerto_inicial,
    pedir_puerto_final,
)

from network import scan_range


def main():

    mostrar_banner()

    ip = pedir_ip()
    puerto_inicial = pedir_puerto_inicial()
    puerto_final = pedir_puerto_final()

    print("\nEscaneando...\n")

    scan_range(ip, puerto_inicial, puerto_final)


if __name__ == "__main__":
    main()