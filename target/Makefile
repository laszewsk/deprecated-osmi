RIVANNA_USER := $(shell ssh rivanna whoami)


rsync-rivanna:
	mkdir -p ./results/rivanna/train
	echo "Rivanna Username:" $(RIVANNA_USER)
	rsync -rav --progress --exclude='models' rivanna:/scratch/${RIVANNA_USER}/osmi/target/rivanna/train/project/ ./results/rivanna/train
