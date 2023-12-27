requirements:
	pip install -r target/ubuntu/requirements-ubuntu.txt

train: requireements
	cd models; \
	python train.py small_lstm; \
	python train.py medium_cnn; \
	python train.py large_tcnn;


clean: ## Clean the project
	$(call banner, "CLEAN")
	rm -rf *.egg-info
	rm -rf *.eggs
	rm -rf docs/build
	rm -rf build
	rm -rf dist
	rm -rf .tox
	rm -rf .tmp
	find . -type d -name '__pycache__' -exec rm -rf {} +
	pip uninstall ${package} -y


