ifndef SNIPER_ROOT
	$(error SNIPER_ROOT should be defined)
endif
ifndef BULLET_ROOT
	$(error BULLET_ROOT should be defined)
endif

root := $(shell pwd)

options := -c gainestown
options += -s ${root}/scripts/bullet.py

export SNIPER_OPTIONS = ${options}
export TOOLS_ROOT = ${root}/tools
export RESULTS_ROOT = ${root}/results

all:
	@echo 'Usage: make run-{BENCHMARK SUITE}-{BENCHMARK NAME}'

run-%:
	@$(MAKE) -C results $*

clean:
	@$(MAKE) -C results clean

reset:
	@redis-cli flushall > /dev/null

setup:
	@redis-server configs/redis.conf

kill:
	@killall -q -KILL -- pinbin mcpat.py bullet || echo -n
	@$(MAKE) -C results kill

.PHONY: all run-% clean reset setup kill
