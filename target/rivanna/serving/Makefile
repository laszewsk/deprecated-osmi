

PWD := $(shell pwd)
TESTDATA="$(PWD)/tmp/serving/tensorflow_serving/servables/tensorflow/testdata"

get:
	docker pull tensorflow/serving

get-test-server:
	@echo "TESTDATA: $(TESTDATA)"
	mkdir tmp
	cd tmp; git clone https://github.com/tensorflow/serving \
    
run-test-server:
	docker run -t --rm -p 8501:8501 \
    	-v "${TESTDATA}/saved_model_half_plus_two_cpu:/models/half_plus_two" \
    	-e MODEL_NAME=half_plus_two \
    	tensorflow/serving &

run-test:
	curl -d '{"instances": [1.0, 2.0, 5.0]}' \
    	-X POST http://localhost:8501/v1/models/half_plus_two:predict

	# Returns => { "predictions": [2.5, 3.0, 4.5] }

stop-test-server:
	docker stop $$(docker ps -q -f ancestor=tensorflow/serving)
