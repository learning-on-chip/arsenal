include ../suite.mk

names := \
	blackscholes bodytrack canneal dedup facesim ferret fluidanimate freqmine \
	raytrace streamcluster swaptions vips x264

inputs := small medium large

programs := $(foreach input,$(inputs),$(addsuffix -$(input),$(names)))

$(eval $(call declare_suite,parsec,$(programs)))
