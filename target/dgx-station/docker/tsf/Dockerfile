# Use the TensorFlow Serving image from Docker Hub
FROM tensorflow/serving:latest

# Set the environment variables
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Create a directory for your models (adjust the path as needed)
RUN mkdir -p /models
# possibly better to use bind dir: GVL

# Create an entrypoint script
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'if [ -z "$PORT" ]; then' >> /entrypoint.sh && \
    echo '    echo "Please specify the PORT environment variable"' >> /entrypoint.sh && \
    echo '    exit 1' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    echo 'if [ -z "$MODEL_CONFIG_FILE" ]; then' >> /entrypoint.sh && \
    echo '    echo "Please specify the MODEL_CONFIG_FILE environment variable"' >> /entrypoint.sh && \
    echo '    exit 1' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    echo 'tensorflow_model_server --port=$PORT --rest_api_port=8502 --model_config_file=$MODEL_CONFIG_FILE' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Expose ports (adjust as needed)
EXPOSE $PORT 8502

# Set the entrypoint to run your script
ENTRYPOINT ["/entrypoint.sh"]
