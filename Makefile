all:
	@echo 'Usage: make run-{PROGRAM SUITE}-{PROGRAM NAME}'

run-%:
	@$(MAKE) -C programs $*

clean kill:
	@$(MAKE) -C programs $@

setup:
	@redis-server configs/redis.conf

.PHONY: all clean kill run-% setup
