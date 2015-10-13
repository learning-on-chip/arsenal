all:
	@echo 'Usage: make run-{BENCHMARK SUITE}-{BENCHMARK NAME}'

run-%:
	@$(MAKE) -C benchmarks $*

clean:
	@$(MAKE) -C benchmarks clean

kill:
	@$(MAKE) -C benchmarks kill

setup:
	@redis-server configs/redis.conf

.PHONY: all run-% reset setup clean kill
