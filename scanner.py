import socket


def mostrar_banner():
    print("=" * 35)
    print("         RenScan v1.0")
    print("=" * 35)


def pedir_ip():
    ip = input("Ingrese la IP: ")
    return ip

def pedir_puerto_inicial():
    return int(input("Puerto inicial: "))


def pedir_puerto_final():
    return int(input("Puerto final: "))


def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    resultado = s.connect_ex((ip, port))

    s.close()

    return resultado == 0

def main():

    mostrar_banner()

    ip = pedir_ip()
    puerto_inicial = pedir_puerto_inicial()
    puerto_final = pedir_puerto_final()

    print("\nEscaneando...\n")

    for puerto in range(puerto_inicial, puerto_final + 1):

        if scan_port(ip, puerto):
            print(f"Puerto {puerto}: OPEN")


if __name__ == "__main__":
    main()
 

