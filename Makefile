export STUDIO_ROOT := $(shell pwd)
export TOOLBOX_ROOT := ${STUDIO_ROOT}/toolbox

ifndef OUTPUT_ROOT
export OUTPUT_ROOT := ${STUDIO_ROOT}/result
endif

all:
	@echo 'Usage: make record-<suite name>-<benchmark name>-<input size>'

install update:
	@${MAKE} -C toolbox $@

setup:
	@redis-server config/redis.conf

record-%:
	@${MAKE} -C program $*

clean kill:
	@${MAKE} -C program $@

.PHONY: all clean install kill setup update
