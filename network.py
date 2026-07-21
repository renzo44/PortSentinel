import socket
import ssl
import time
from colorama import Fore, Style, init

init(autoreset=True)

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
    

def get_https_banner(ip, port):
    try:
        context = ssl.create_default_context()

        with socket.create_connection((ip, port), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname=ip) as secure_sock:

                request = (
                    f"HEAD / HTTP/1.1\r\n"
                    f"Host: {ip}\r\n"
                    "Connection: close\r\n\r\n"
                )

                secure_sock.send(request.encode())

                response = secure_sock.recv(1024).decode(errors="ignore")

                for line in response.splitlines():
                    if line.lower().startswith("server:"):
                        return line.split(":", 1)[1].strip()

                if response.splitlines():
                    return response.splitlines()[0].strip()

                return "HTTPS"

    except Exception:
        return "N/A"

def get_banner(ip, port):

    if port in (80, 8000, 8080):
        return get_http_banner(ip, port)

    if port in (443, 8443):
        return get_https_banner(ip, port)

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

    start_time = time.perf_counter()

    print(
    f"{Fore.CYAN}"
    "PORT     STATUS   SERVICE     BANNER"
    )
    print(Fore.CYAN + "-" * 50)

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

    end_time = time.perf_counter()
    duration = end_time - start_time

    print()

    results.sort(key=lambda result: result[0])

    for puerto, service, banner in results:
        print(
    f"{puerto:<8} "
    f"{Fore.GREEN}OPEN "
    f"{Fore.CYAN}{service:<10} "
    f"{Fore.YELLOW}{banner}"
    )

    export_txt(results)
    export_csv(results)
    export_json(results)

    print("\n" + "=" * 50)
    print("SCAN SUMMARY")
    print("=" * 50)

    print(f"Target         : {ip}")
    print(f"Ports scanned  : {total_ports}")
    print(f"Open ports     : {len(results)}")
    print(f"Closed ports   : {total_ports - len(results)}")
    print(f"Duration       : {duration:.2f} seconds")

    print("\nReports saved:")
    print("  ✔ results.txt")
    print("  ✔ results.csv")
    print("  ✔ results.json")

    print("=" * 50)
    