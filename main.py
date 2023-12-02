import os
import subprocess
from rich.console import Console
from rich.table import Table

console = Console()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def ping_host(host):
    result = subprocess.run(f"ping -n 1 {host}", capture_output=True, text=True)

    if result.returncode == 0:
        for line in result.stdout.split('\n'):
            if "time=" in line:
                return line.split("time=")[1].split(" ")[0]

    return "N/R"


def read_hosts_from_file(filename):
    with open(filename, "r") as file:
        return [line.strip().split(',') for line in file if len(line.strip().split(',')) == 3]


def main():

    clear()
    print("Loading...")

    hosts = read_hosts_from_file("hosts.txt")
    hosts.sort(
        key=lambda x: (float(ping_host(x[1]).rstrip('ms')) + float(ping_host(x[2]).rstrip('ms'))) / 2
        if all(ping_host(x[i]) != "N/R" for i in [1, 2])
        else float('inf')
    )

    table = Table(title="DNS Jumper")
    table.add_column("DNS Server name", no_wrap=True)
    table.add_column("DNS 1")
    table.add_column("DNS 2")
    table.add_column("Result 1")
    table.add_column("Result 2")

    for host in hosts:
        dns1_latency, dns2_latency = ping_host(host[1]), ping_host(host[2])

        result1_style, result2_style = ("green", "green") if all(latency != "N/R" for latency in [dns1_latency, dns2_latency]) else ("red", "red")

        table.add_row(
            host[0], host[1], host[2],
            f"[{result1_style}]{dns1_latency}[/{result1_style}]",
            f"[{result2_style}]{dns2_latency}[/{result2_style}]"
        )

    clear()
    console.print(table)


if __name__ == "__main__":
    main()
