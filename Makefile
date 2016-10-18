export STUDIO_ROOT := $(shell pwd)
export TOOLBOX_ROOT := $(STUDIO_ROOT)/toolbox

ifndef OUTPUT_ROOT
	export OUTPUT_ROOT := $(STUDIO_ROOT)/result
endif

all:
	@echo 'Usage: make run-<program suite>-<program name>-<program input>'

clean kill:
	@$(MAKE) -C program $@

install update:
	@$(MAKE) -C toolbox $@

run-%:
	@$(MAKE) -C program $*

setup:
	@redis-server config/redis.conf

.PHONY: all clean install kill run-% setup update
