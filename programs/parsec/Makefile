include ../suite.mk

ifndef BENCHMARKS_ROOT
$(error BENCHMARKS_ROOT should be defined)
endif
export SNIPER_BIN := ${BENCHMARKS_ROOT}/run-sniper

programs := blackscholes bodytrack facesim ferret freqmine raytrace swaptions
programs += fluidanimate vips x264 canneal dedup streamcluster

all: $(programs)

$(eval $(call declare_suite,parsec,$(programs)))
