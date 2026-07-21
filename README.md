# PortSentinel

A fast, multithreaded TCP port scanner written in Python.

PortSentinel is a lightweight network reconnaissance tool capable of scanning TCP ports, identifying common services, grabbing banners, and exporting results in multiple formats.

---

## Features

- Multithreaded TCP port scanning
- Service identification
- TCP banner grabbing
- HTTP banner grabbing
- HTTPS banner grabbing
- Scan custom port ranges
- Scan custom port lists
- Scan top common ports
- Configurable thread count
- Colored terminal output
- Progress bar
- TXT report export
- CSV report export
- JSON report export
- Scan execution summary
- Command-line interface (CLI)

---

## Project Structure

```text
PortSentinel/
│
├── scanner.py
├── network.py
├── services.py
├── ports.py
├── exporter.py
├── utils.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/renzo44/PortSentinel.git
cd PortSentinel
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Interactive mode

```bash
python scanner.py
```

---

### Scan the first 1000 ports

```bash
python scanner.py google.com
```

---

### Scan a port range

```bash
python scanner.py google.com -p 20-100
```

---

### Scan specific ports

```bash
python scanner.py google.com -p 22,80,443
```

---

### Scan top common ports

Top 10:

```bash
python scanner.py google.com --top-ports 10
```

Top 100:

```bash
python scanner.py google.com --top-ports
```

---

### Configure threads

```bash
python scanner.py google.com -p 1-1000 -t 250
```

---

## Example Output

```text
===================================
        PortSentinel v0.5
===================================

PORT     STATUS   SERVICE     BANNER
--------------------------------------------------
80       OPEN     HTTP        gws
443      OPEN     HTTPS       gws

==================================================
SCAN SUMMARY
==================================================
Target         : google.com
Ports scanned  : 1000
Open ports     : 2
Closed ports   : 998
Threads        : 250
Duration       : 4.10 seconds
==================================================
```

---

## Exported Reports

After each scan, PortSentinel automatically generates:

- results.txt
- results.csv
- results.json

---

## Technologies

- Python 3
- socket
- concurrent.futures
- argparse
- tqdm
- colorama

---

## Roadmap

### Version 1.0

- [x] Multithreaded scanner
- [x] Banner grabbing
- [x] Service detection
- [x] Progress bar
- [x] Colored output
- [x] Export reports
- [x] CLI
- [x] Custom thread count
- [x] Custom port lists
- [x] Top ports
- [x] Argument validation
- [ ] Unit tests
- [ ] MIT License
- [ ] Version 1.0 Release

---

## Disclaimer

This software is intended for educational purposes and authorized security testing only.

Always obtain permission before scanning systems you do not own.

---

## License


This project is licensed under the MIT License. See the LICENSE file for details.