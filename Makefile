export STUDIO_ROOT := $(shell pwd)

ifndef OUTPUT_ROOT
export OUTPUT_ROOT = $(STUDIO_ROOT)/results
endif

usage:
	@echo 'Usage: make run-{PROGRAM SUITE}-{PROGRAM NAME}'

run-%:
	@$(MAKE) -C programs $*

clean:
	@$(MAKE) -C programs $@

kill:
	@$(MAKE) -C programs $@

setup:
	@redis-server configs/redis.conf

.PHONY: all clean kill run-% setup
