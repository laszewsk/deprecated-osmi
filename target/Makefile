RIVANNA_USER := $(shell ssh rivanna whoami)


rsync-rivanna:
	mkdir -p ./results/rivanna/train/project
	echo "Rivanna Username:" $(RIVANNA_USER)
	rsync -rav --exclude='models' rivanna:/scratch/${RIVANNA_USER}/osmi/target/rivanna/train/project/ ./results/rivanna/train/project
