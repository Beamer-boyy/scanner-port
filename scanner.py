#!/usr/bin/env python3

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime

def parse_ports(ports_str):
    """Parse strings like '1-1024' or '22,80,443,8000-8100' into a sorted list of ints."""
    ports = set()
    parts = ports_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            a, b = part.split('-', 1)
            try:
                a, b = int(a), int(b)
                if a > b:
                    a, b = b, a
                ports.update(range(max(1, a), min(65535, b) + 1))
            except ValueError:
                continue
        else:
            try:
                p = int(part)
                if 1 <= p <= 65535:
                    ports.add(p)
            except ValueError:
                continue
    return sorted(ports)

def scan_port(host, port, timeout=1.0):
    """Try to connect to (host, port). Return (port, open_bool, banner_or_error)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                # try to read a small banner (non-blocking)
                try:
                    s.settimeout(0.5)
                    banner = s.recv(1024)
                    try:
                        banner = banner.decode(errors='ignore').strip()
                    except:
                        banner = repr(banner)
                    return (port, True, banner)
                except Exception:
                    return (port, True, "")
            else:
                return (port, False, "")
    except Exception as e:
        return (port, False, f"err:{e}")

def run_scan(host, ports, threads=100, timeout=1.0, verbose=True):
    open_ports = []
    start = datetime.utcnow()
    if verbose:
        print(f"[+] Iniciando scan em {host} - {len(ports)} portas - threads={threads} - timeout={timeout}s")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_port = {executor.submit(scan_port, host, p, timeout): p for p in ports}
        for future in as_completed(future_to_port):
            p = future_to_port[future]
            try:
                port, is_open, banner = future.result()
                if is_open:
                    open_ports.append((port, banner))
                    if verbose:
                        print(f"[OPEN] {port}  {banner}")
                else:
                    if verbose and False:
                        print(f"[CLOSED] {port}")
            except Exception as exc:
                if verbose:
                    print(f"[ERROR] port {p} -> {exc}")
    end = datetime.utcnow()
    if verbose:
        print(f"[+] Scan finalizado em {(end - start).total_seconds():.2f}s. {len(open_ports)} portas abertas.")
    return open_ports

def save_csv(host, open_ports, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.writer(fh)
        writer.writerow(['host', 'port', 'banner', 'scanned_at'])
        now = datetime.utcnow().isoformat() + 'Z'
        for port, banner in open_ports:
            writer.writerow([host, port, banner, now])
    print(f"[+] Resultados salvos em {filename}")

def main():
    parser = argparse.ArgumentParser(description="Simple TCP port scanner (educational).")
    parser.add_argument('-H', '--host', required=True, help='IP ou hostname alvo')
    parser.add_argument('-p', '--ports', default='1-1024', help="Portas (ex: 22,80,443 or 1-1024 or combinação)")
    parser.add_argument('-t', '--threads', type=int, default=100, help='Threads concorrentes (padrão 100)')
    parser.add_argument('--timeout', type=float, default=1.0, help='Timeout por conexão em segundos (padrão 1.0)')
    parser.add_argument('-o', '--output', help='Salvar resultado CSV (ex: results.csv)')
    parser.add_argument('--no-verbose', dest='verbose', action='store_false', help='Não mostrar progresso')
    args = parser.parse_args()

    ports = parse_ports(args.ports)
    if not ports:
        print("Nenhuma porta válida informada.")
        return

    # resolve host
    try:
        ip = socket.gethostbyname(args.host)
    except Exception as e:
        print(f"Erro resolvendo host {args.host}: {e}")
        return

    open_ports = run_scan(ip, ports, threads=args.threads, timeout=args.timeout, verbose=args.verbose)
    if args.output:
        save_csv(args.host, open_ports, args.output)

if __name__ == '__main__':
    main()
