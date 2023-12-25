requirements:
	pip install -r target/ubuntu/requirements-ubuntu.txt

train: requireements
	cd models; \
	python train.py small_lstm; \
	python train.py medium_cnn; \
	python train.py large_tcnn;