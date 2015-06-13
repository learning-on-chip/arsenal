ifndef BENCHMARKS_ROOT
	$(error BENCHMARKS_ROOT should be defined)
endif

sniper := ${BENCHMARKS_ROOT}/run-sniper

options := ${SNIPER_OPTIONS}
options += -i small

apps = blackscholes bodytrack facesim ferret freqmine raytrace swaptions fluidanimate vips x264
kernels = canneal dedup streamcluster
benchmarks := ${apps} ${kernels}

$(benchmarks): %: %/.done

%/.done:
	@mkdir -p $*
	@echo "Running parsec-$* on $(shell ./cores.py $*) core(s)..."
	@(cd $* && BENCHMARK_NAME=$* ${sniper} ${options} -n $(shell ./cores.py $*) -p parsec-$*)
	@echo "Finished parsec-$*."
	@touch $@

clean:
	@rm -rf $(benchmarks)

kill:
	@killall -q -KILL -- blackscholes x264 ferret || echo -n

.PHONY: $(benchmarks) clean kill
