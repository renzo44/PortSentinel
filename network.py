import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from exporter import (
    export_txt,
    export_csv,
    export_json,
)

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
                return line.split(":", 1)[1].strip()

        return response.splitlines()[0].strip()

    except Exception:
        return "N/A"

def get_banner(ip, port):

    if port in (80, 8000, 8080):
        return get_http_banner(ip, port)

    return get_generic_banner(ip, port)


def identify_service(service, banner):
    if service != "Unknown":
        return service

    banner = banner.lower()

    if "http" in banner:
        return "HTTP"

    if "openssh" in banner:
        return "SSH"

    if "smtp" in banner:
        return "SMTP"

    if "ftp" in banner:
        return "FTP"

    return service


def scan_single_port(ip, puerto):

    if scan_port(ip, puerto):
        service = get_service(puerto)
        banner = get_banner(ip, puerto)

        service = identify_service(service, banner)

        return (puerto, service, banner)

    return None


def scan_range(ip, puerto_inicial, puerto_final):

    print("PORT     STATUS   SERVICE     BANNER")
    print("-" * 50)

    results = []

    total_ports = puerto_final - puerto_inicial + 1

    with ThreadPoolExecutor(max_workers=100) as executor:

        futures = []

        for puerto in range(puerto_inicial, puerto_final + 1):
            future = executor.submit(scan_single_port, ip, puerto)
            futures.append(future)

        progress_bar = tqdm(
            total=total_ports,
            desc="Scanning",
            ncols=75,
            unit="ports",
            colour="green",
)


        for future in as_completed(futures):

            result = future.result()

            progress_bar.update(1)

            if result:
                results.append(result)

        progress_bar.close()

    print()

    results.sort(key=lambda result: result[0])

    for puerto, service, banner in results:
        print(f"{puerto:<8} OPEN     {service:<10} {banner}")

    export_txt(results)
    export_csv(results)
    export_json(results)