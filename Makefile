# Makefile for Vesuvius Challenge Ink Detection

.PHONY: dataset train optimisation

dataset:
	python src/data/make_dataset.py

train:
ifdef dry
	python src/models/models.py
else
	python src/models/make_train.py -m $(model)
endif

wandb:
ifdef sweepid
	wandb agent rosia-lab/vesuvius-challenge-ink-detection/$(sweepid)
endif
