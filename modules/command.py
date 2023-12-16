#!/usr/bin/env python3
import json
import statistics

from netmiko import ConnectHandler

env = json.load(open('env.json'))


def ping(host, target, source, port):
    print(f"Pinging {target} from {source} for {host} and {port}" )
    device = {
        "device_type": "fortinet",
        "host": f"{host}",
        "port": f"{port}",
        "username": f"{env['USER']}",
        "password": f"{env['PASSWORD']}",
    }

    try:
        with ConnectHandler(**device, allow_auto_change=True) as net_connect:
            pre_command = f'exec ping-options source {source}'
            net_connect.send_command(pre_command)
            command = f'execute ping {target}'

            multi_lines = ""f'{net_connect.send_command(command)}'""
            lines = multi_lines.splitlines()
            ping_median = []

            if " 0% packet loss" not in multi_lines:
                return "fail"

            for line in lines:
                if "icmp_seq" in line:
                    ping_time = line.split()[-2].split('=')[-1]
                    ping_median.append(float(ping_time))

            return round(statistics.median(ping_median), 0)

    except Exception as e:
        return "fail"


if __name__ == "__main__":
    ping("192.168.100.31", "192.168.100.30", "192.168.100.50", 22)
