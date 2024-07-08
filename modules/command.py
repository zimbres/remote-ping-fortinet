#!/usr/bin/env python3
import json
import statistics

from netmiko import ConnectHandler

env = json.load(open('env.json'))


def ping(host, target, source, port, vdom=None):
    device = {
        "device_type": "fortinet",
        "host": f"{host}",
        "port": f"{port}",
        "username": f"{env['USER']}",
        "password": f"{env['PASSWORD']}"
    }

    try:
        with ConnectHandler(**device, allow_auto_change=True) as net_connect:
            if vdom is not None:
                net_connect.send_command('config vdom', expect_string=r"\ \(\w+\)\ [#$]")
                net_connect.send_command(f'edit {vdom}', expect_string=r"\ \(\w+\)\ [#$]")
                net_connect.send_command(f'exec ping-options source {source}', expect_string=r"\ \(\w+\)\ [#$]")
                multi_lines = net_connect.send_command(f'execute ping {target}', read_timeout=60, expect_string=r"\ \(\w+\)\ [#$]")
            else:
                net_connect.send_command(f'exec ping-options source {source}')
                multi_lines = net_connect.send_command(f'execute ping {target}', read_timeout=60)

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
        print(e)
        return "fail"


if __name__ == "__main__":
    ping("192.168.100.31", "192.168.100.30", "192.168.100.50", 22)
