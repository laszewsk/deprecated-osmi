# Use the TensorFlow GPU image from NVIDIA GPU Cloud (NGC)
FROM nvcr.io/nvidia/tensorflow:23.04-tf2-py3

# Update pip and install Python packages
RUN pip install --upgrade pip && \
    pip install numpy matplotlib pandas scikit-learn opencv-python
    pip install git+https://github.com/mlperf/logging.git
    pip install cloudmesh-common cloudmesh-gpu
    pip install tensorflow-serving-api

# Set environment variables if necessary
# ENV VARIABLE_NAME=value

# Optionally, you can expose ports or set other configurations here
# EXPOSE port_number

# Set the working directory if needed
# WORKDIR /app

# Command to run when the container starts (if required)
# CMD ["command", "arg1", "arg2", ...]
