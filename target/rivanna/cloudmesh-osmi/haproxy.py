"""
Manage HAProxy operations.

Usage:
    haproxy_manager.py start CONFIG_FILE
    haproxy_manager.py stop
    haproxy_manager.py status
    haproxy_manager.py wait CONFIG_FILE [--timeout=TIMEOUT] [--interval=INTERVAL]

Options:
    CONFIG_FILE         Path to HAProxy configuration file.
    --timeout=TIMEOUT   Maximum time to wait for HAProxy to start [default: 60].
    --interval=INTERVAL Time interval between status checks [default: 5].
"""

import subprocess
import time
from docopt import docopt

class HAProxyManager:
    """
    A class to manage HAProxy.

    Attributes:
        haproxy_executable (str): The path to the HAProxy executable.

    Methods:
        start(config_file): Start HAProxy with the specified configuration file.
        stop(): Stop HAProxy.
        status(): Check the status of HAProxy.
        wait_for_start(config_file, timeout, interval): Wait for HAProxy to start within the specified timeout.
    """

    def __init__(self, haproxy_executable="/usr/sbin/haproxy"):
        self.haproxy_executable = haproxy_executable

    def start(self, config_file):
        """
        Start HAProxy with the specified configuration file.

        Args:
            config_file (str): The path to the HAProxy configuration file.
        """
        try:
            subprocess.run([self.haproxy_executable, "-f", config_file, "-D"], check=True)
            print("HAProxy started.")
        except subprocess.CalledProcessError:
            print("Error starting HAProxy.")

    def stop(self):
        """
        Stop HAProxy.
        """
        try:
            subprocess.run([self.haproxy_executable, "-D", "-sf", " $(pgrep haproxy)"], shell=True, check=True)
            print("HAProxy stopped.")
        except subprocess.CalledProcessError:
            print("Error stopping HAProxy.")

    def status(self):
        """
        Check the status of HAProxy.

        Returns:
            bool: True if HAProxy is running and the configuration is valid, False otherwise.
        """
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
        """
        Wait for HAProxy to start within the specified timeout.

        Args:
            config_file (str): The path to the HAProxy configuration file.
            timeout (int): The maximum time to wait for HAProxy to start, in seconds. Default is 60 seconds.
            interval (int): The interval between status checks, in seconds. Default is 5 seconds.
        """
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
        haproxy_manager.start(arguments["CONFIG_FILE"])
    elif arguments["stop"]:
        haproxy_manager.stop()
    elif arguments["status"]:
        haproxy_manager.status()
    elif arguments["wait"]:
        haproxy_manager.wait_for_start(arguments["CONFIG_FILE"],
                                       timeout=int(arguments["--timeout"]),
                                       interval=int(arguments["--interval"]))
