include ../suite.mk

ifndef BENCHMARKS_ROOT
$(error BENCHMARKS_ROOT should be defined)
endif
export SNIPER_BIN := ${BENCHMARKS_ROOT}/run-sniper

benchmarks := blackscholes bodytrack facesim ferret freqmine raytrace swaptions
benchmarks += fluidanimate vips x264 canneal dedup streamcluster
benchmarks += facesim_facesim freqmine_freqmine freqmine_x264 x264_x264

all: $(benchmarks)

$(eval $(call declare_suite,parsec,$(benchmarks)))
