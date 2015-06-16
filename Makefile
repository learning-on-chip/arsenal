ifndef SNIPER_ROOT
	$(error SNIPER_ROOT should be defined)
endif
ifndef SQUIRE_ROOT
	$(error SQUIRE_ROOT should be defined)
endif

root := $(shell pwd)

options := -c gainestown
options += -s ${root}/scripts/squire.py

export SNIPER_OPTIONS = ${options}
export TOOLS_ROOT = ${root}/tools
export RESULTS_ROOT = ${root}/results

all:
	@echo 'Usage: make run-{BENCHMARK SUITE}-{BENCHMARK NAME}'

run-%:
	@$(MAKE) -C results $*

clean:
	@$(MAKE) -C results clean

kill:
	@killall -q -KILL -- pinbin mcpat.py squire || echo -n
	@$(MAKE) -C results kill

setup:
	@redis-server configs/redis.conf

install:
	@$(MAKE) -C vendor

.PHONY: all run-% reset setup clean kill
