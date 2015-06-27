include ../suite.mk

ifndef SNIPER_ROOT
$(error SNIPER_ROOT should be defined)
endif
export SNIPER_BIN := ${SNIPER_ROOT}/run-sniper

ifndef PINBALLS_ROOT
$(error PINBALLS_ROOT should be defined)
endif
benchmarks := $(patsubst cpu2006-%,%,$(notdir $(wildcard ${PINBALLS_ROOT}/cpu2006-*)))

all: $(benchmarks)

$(eval $(call declare_suite,cpu2006pinballs,$(benchmarks)))
