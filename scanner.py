import argparse

from utils import (
    mostrar_banner,
    pedir_ip,
    pedir_puerto_inicial,
    pedir_puerto_final,
)

from network import scan_range


def main():

    parser = argparse.ArgumentParser(
        description="PortSentinel - TCP Port Scanner"
    )

    parser.add_argument(
        "target",
        nargs="?",
        help="Target IP address or domain"
    )

    parser.add_argument(
        "-p",
        "--ports",
        default=None,
        help="Port range (example: 1-1000)"
    )

    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=100,
        help="Number of concurrent threads (default: 100)"
    )

    args = parser.parse_args()

    mostrar_banner()

    if args.target:
        ip = args.target

        if args.ports:
            puerto_inicial, puerto_final = map(int, args.ports.split("-"))
        else:
            puerto_inicial = 1
            puerto_final = 1000

    else:
        ip = pedir_ip()
        puerto_inicial = pedir_puerto_inicial()
        puerto_final = pedir_puerto_final()

    print("\nEscaneando...\n")

    scan_range(
        ip,
        puerto_inicial,
        puerto_final,
        args.threads
    )


if __name__ == "__main__":
    main()