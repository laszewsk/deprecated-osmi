FROM nvcr.io/nvidia/tensorflow:23.12-tf2-py3

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update
RUN apt install python3-pip -y
RUN pip --version
RUN	pip install pip -U
RUN	pip install numpy
RUN	pip install matplotlib
RUN	pip install pandas
RUN	pip install scikit-learn
RUN	pip install opencv-python
RUN	pip install git+https://github.com/mlperf/logging.git
RUN	pip install cloudmesh-common==4.3.195
RUN	pip install cloudmesh-gpu==4.3.23
RUN	pip install tensorflow-serving-api

# ENTRYPOINT ["time", "python", "/scratch/osmi/models/train.py", "small_lstm"]


# ------------------------------------  Extras Below  ------------------------------------

# Stop the container (changes are kept)
# docker stop $(docker ps -ql)

# Start the container
# docker start -ai $(docker ps -ql)

# Delete the container
# docker rm $(docker ps -ql)

# Save changes before deleting the container
# docker commit $(docker ps -ql) fastmot:latest
