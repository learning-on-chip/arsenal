ifndef BENCHMARKS_ROOT
$(error BENCHMARKS_ROOT should be defined)
endif

sniper := ${BENCHMARKS_ROOT}/run-sniper

apps = blackscholes bodytrack facesim ferret freqmine raytrace swaptions fluidanimate vips x264
kernels = canneal dedup streamcluster
benchmarks := ${apps} ${kernels}

benchmarks += freqmine_x264

all: $(benchmarks)

define declare_benchmark
$(1)_options := $(shell ./configure.py $(1))

$(1): $(1)/.done

$(1)/.done:
	@mkdir -p $(1)
	@echo "Running parsec-$(1)..."
	@echo "Arguments: $${$(1)_options}"
	@(cd $(1) && BENCHMARK_NAME=$(1) $${sniper} $${SNIPER_OPTIONS} $${$(1)_options})
	@echo "Finished parsec-$(1)."
	@touch $$@
endef

$(foreach benchmark,$(benchmarks),$(eval $(call declare_benchmark,$(benchmark))))

%-clean:
	@rm -rf $*

%-kill:
	@killall -q -KILL -- $* || true

clean: $(addsuffix -clean,$(benchmarks))

kill: $(addsuffix -kill,$(benchmarks))

.PHONY: all $(benchmarks) %clean %kill
