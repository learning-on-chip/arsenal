include ../suite.mk

names := \
	GemsFDTD astar bwaves bzip2 cactusADM calculix dealII gamess gcc gobmk \
	gromacs h264ref hmmer lbm leslie3d libquantum mcf milc namd omnetpp \
	perlbench povray sjeng soplex sphinx3 tonto wrf xalancbmk zeusmp

inputs := large

programs := $(foreach input,$(inputs),$(addsuffix -$(input),$(names)))

$(eval $(call declare_suite,cpu2006,$(programs)))
