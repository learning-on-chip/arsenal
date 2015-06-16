all:
	@echo 'Usage: make run-{BENCHMARK SUITE}-{BENCHMARK NAME}'

run-%:
	@$(MAKE) -C results $*

clean:
	@$(MAKE) -C results clean

kill:
	@$(MAKE) -C results kill

setup:
	@redis-server configs/redis.conf

install:
	@$(MAKE) -C vendor

.PHONY: all run-% reset setup clean kill
