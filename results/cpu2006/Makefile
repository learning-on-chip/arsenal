include ../suite.mk

ifndef BENCHMARKS_ROOT
$(error BENCHMARKS_ROOT should be defined)
endif
export SNIPER_BIN := ${BENCHMARKS_ROOT}/run-sniper

benchmarks := perlbench bzip2 gcc bwaves gamess mcf milc zeusmp gromacs
benchmarks += cactusADM leslie3d namd gobmk dealII soplex povray calculix hmmer
benchmarks += sjeng GemsFDTD libquantum h264ref tonto lbm omnetpp astar wrf
benchmarks += sphinx3 xalancbmk

all: $(benchmarks)

$(eval $(call declare_suite,cpu2006,$(benchmarks)))
