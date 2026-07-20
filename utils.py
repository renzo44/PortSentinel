import socket
import ipaddress

def validar_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
    
def mostrar_banner():
    print("=" * 35)
    print("         PortSentinel v0.5")
    print("=" * 35)


def pedir_ip():

    while True:

        entrada = input("Ingrese una IP o dominio: ")

        if validar_ip(entrada):
            return entrada

        try:
            ip = socket.gethostbyname(entrada)

            print(f"Dominio resuelto: {ip}")

            return ip

        except socket.gaierror:
            print("IP o dominio inválido.")
        
def pedir_puerto_inicial():
    return int(input("Puerto inicial: "))


def pedir_puerto_final():
    return int(input("Puerto final: "))