# Use the Ubuntu base image
FROM ubuntu:latest

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y haproxy && \
    rm -rf /var/lib/apt/lists/*

# Set the environment variables
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Copy the haproxy.cfg file from the host to the container's current working directory
COPY haproxy.cfg /etc/haproxy/haproxy.cfg

# Expose any necessary ports (assuming you have defined them in haproxy.cfg)
# EXPOSE <port_number>

# Start haproxy in the background
CMD ["/usr/sbin/haproxy", "-f", "/etc/haproxy/haproxy.cfg", "-db"]