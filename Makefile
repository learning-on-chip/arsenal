export STUDIO_ROOT := $(shell pwd)

ifndef OUTPUT_ROOT
export OUTPUT_ROOT = $(STUDIO_ROOT)/result
endif

usage:
	@echo 'Usage: make run-{PROGRAM SUITE}-{PROGRAM NAME}'

run-%:
	@$(MAKE) -C program $*

clean:
	@$(MAKE) -C program $@

kill:
	@$(MAKE) -C program $@

setup:
	@redis-server config/redis.conf

.PHONY: all clean kill run-% setup
