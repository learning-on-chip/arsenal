include ../suite.mk

ifndef BENCHMARKS_ROOT
$(error BENCHMARKS_ROOT should be defined)
endif
export SNIPER_BIN := ${BENCHMARKS_ROOT}/run-sniper

programs := perlbench bzip2 gcc bwaves gamess mcf milc zeusmp gromacs
programs += cactusADM leslie3d namd gobmk dealII soplex povray calculix hmmer
programs += sjeng GemsFDTD libquantum h264ref tonto lbm omnetpp astar wrf
programs += sphinx3 xalancbmk

all: $(programs)

$(eval $(call declare_suite,cpu2006,$(programs)))
