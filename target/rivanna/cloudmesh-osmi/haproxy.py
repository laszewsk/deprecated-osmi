"""
Manage HAProxy operations.

Usage:
    haproxy_manager.py start <config_file>
    haproxy_manager.py stop
    haproxy_manager.py status
    haproxy_manager.py wait <config_file> [--timeout=<timeout>] [--interval=<interval>]

Options:
    <config_file>    Path to HAProxy configuration file.
    --timeout=<timeout>   Maximum time to wait for HAProxy to start [default: 60].
    --interval=<interval> Time interval between status checks [default: 5].
"""

import subprocess
import time
from docopt import docopt

class HAProxyManager:
    def __init__(self, haproxy_executable="/usr/sbin/haproxy"):
        self.haproxy_executable = haproxy_executable

    def start(self, config_file):
        try:
            subprocess.run([self.haproxy_executable, "-f", config_file, "-D"], check=True)
            print("HAProxy started.")
        except subprocess.CalledProcessError:
            print("Error starting HAProxy.")

    def stop(self):
        try:
            subprocess.run([self.haproxy_executable, "-D", "-sf", " $(pgrep haproxy)"], shell=True, check=True)
            print("HAProxy stopped.")
        except subprocess.CalledProcessError:
            print("Error stopping HAProxy.")

    def status(self):
        try:
            output = subprocess.run([self.haproxy_executable, "-c"], capture_output=True, text=True)
            if output.returncode == 0:
                print("HAProxy is running and configuration is valid.")
                return True
            else:
                print("HAProxy is not running or configuration is invalid.")
                return False
        except subprocess.CalledProcessError:
            print("Error checking HAProxy status.")
            return False

    def wait_for_start(self, config_file, timeout=60, interval=5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.status():
                print("HAProxy is up and running.")
                return
            time.sleep(interval)
        print("Timeout reached. HAProxy did not start within the specified timeout.")

if __name__ == "__main__":
    arguments = docopt(__doc__)

    haproxy_manager = HAProxyManager()

    if arguments["start"]:
        haproxy_manager.start(arguments["<config_file>"])
    elif arguments["stop"]:
        haproxy_manager.stop()
    elif arguments["status"]:
        haproxy_manager.status()
    elif arguments["wait"]:
        haproxy_manager.wait_for_start(arguments["<config_file>"],
                                       timeout=int(arguments["--timeout"]),
                                       interval=int(arguments["--interval"]))
