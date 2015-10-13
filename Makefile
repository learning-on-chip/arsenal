all:
	@echo 'Usage: make run-{PROGRAM SUITE}-{PROGRAM NAME}'

run-%:
	@$(MAKE) -C programs $*

clean:
	@$(MAKE) -C programs clean

kill:
	@$(MAKE) -C programs kill

setup:
	@redis-server configs/redis.conf

.PHONY: all run-% reset setup clean kill
