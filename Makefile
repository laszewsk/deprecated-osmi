train:
	cd models; \
	python train.py small_lstm; \
	python train.py medium_cnn; \
	python train.py large_tcnn;