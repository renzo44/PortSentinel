import argparse

from ports import TOP_PORTS

from utils import (
    mostrar_banner,
    pedir_ip,
    pedir_puerto_inicial,
    pedir_puerto_final,
)

from network import scan_ports


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
        help="Port range (example: 1-1000 or 22,80,443)"
    )

    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=100,
        help="Number of concurrent threads (default: 100)"
    )

    parser.add_argument(
        "--top-ports",
        nargs="?",
        const=100,
        type=int,
        help="Scan the most common ports"
    )

    args = parser.parse_args()

    # Validate thread count
    if args.threads <= 0:
        parser.error("Thread count must be greater than zero.")

    mostrar_banner()

    if args.target:
        ip = args.target

        if args.top_ports:
            ports = TOP_PORTS[:args.top_ports]

        elif args.ports:

            try:

                if "-" in args.ports:

                    puerto_inicial, puerto_final = map(
                        int,
                        args.ports.split("-")
                    )

                    if puerto_inicial > puerto_final:
                        parser.error("Invalid port range.")

                    ports = list(
                        range(puerto_inicial, puerto_final + 1)
                    )

                else:

                    ports = sorted(
                        set(
                            int(port.strip())
                            for port in args.ports.split(",")
                        )
                    )

            except ValueError:
                parser.error(
                    "Invalid port specification. Use formats like 1-1000 or 22,80,443."
                )

        else:
            ports = list(range(1, 1001))

    else:
        ip = pedir_ip()
        puerto_inicial = pedir_puerto_inicial()
        puerto_final = pedir_puerto_final()

        ports = list(range(puerto_inicial, puerto_final + 1))

    # Validate ports
    if not ports:
        parser.error("No ports specified.")

    if any(port < 1 or port > 65535 for port in ports):
        parser.error("Port numbers must be between 1 and 65535.")

    print("\nEscaneando...\n")

    scan_ports(
        ip,
        ports,
        args.threads
    )


if __name__ == "__main__":
    main()