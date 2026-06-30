import socket


def mostrar_banner():
    print("=" * 35)
    print("         RenScan v1.0")
    print("=" * 35)


def pedir_ip():
    ip = input("Ingrese la IP: ")
    return ip

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(1)

    resultado = s.connect_ex((ip, port))

    s.close()

    return resultado == 0

def main():

    mostrar_banner()

    ip = pedir_ip()

    puerto = 80

    print("\nEscaneando...\n")

    if scan_port(ip, puerto):
        print(f"Puerto {puerto}: OPEN")
    else:
        print(f"Puerto {puerto}: CLOSED")

if __name__ == "__main__":
    main()
    
 

