include ../suite.mk

programs := perlbench bzip2 gcc bwaves gamess mcf milc zeusmp gromacs
programs += cactusADM leslie3d namd gobmk dealII soplex povray calculix hmmer
programs += sjeng GemsFDTD libquantum h264ref tonto lbm omnetpp astar wrf
programs += sphinx3 xalancbmk

all: $(programs)

$(eval $(call declare_suite,cpu2006,$(programs)))
