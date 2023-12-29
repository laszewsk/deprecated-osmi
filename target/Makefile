
rsync-rivanna:
	mkdir -p ./results/rivanna/train/project
	echo "Rivanna Username:" $(shell ssh rivanna whoami)
	rsync -rav --exclude='models' rivanna:/scratch/$(shell ssh rivanna whoami)/osmi/target/rivanna/train/project/ ./results/rivanna/train/project

rsync-macos:
	mkdir -p ./results/macos/train/project
	rsync -rav --exclude='models' macos/train/project/ ./results/macos/train/project

rsync-ubuntu:
	mkdir -p ./results/ubuntu/train/project
	echo "ubuntu Username:" $(shell ssh white whoami)
	rsync -rav --exclude='models' white:/home/$(shell ssh white whoami)/Desktop/cm/5/osmi/target/ubuntu/train/project/ ./results/ubuntu/train/project
