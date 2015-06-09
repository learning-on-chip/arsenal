ifndef SNIPER_ROOT
	$(error SNIPER_ROOT should be defined)
endif
ifndef BENCHMARKS_ROOT
	$(error BENCHMARKS_ROOT should be defined)
endif
ifndef BULLET_ROOT
	$(error BULLET_ROOT should be defined)
endif

apps = blackscholes bodytrack facesim ferret freqmine raytrace swaptions fluidanimate vips x264
kernels = canneal dedup streamcluster

benchmarks := ${apps} ${kernels}

root := $(shell pwd)
sniper := ${BENCHMARKS_ROOT}/run-sniper

options := -i small
options += -n 16
options += -c gainestown
options += -c --general/total_cores=1
options += -s ${root}/scripts/bullet.py

export TOOLS_ROOT = ${root}/tools
export RESULTS_ROOT = ${root}/results

all: $(benchmarks)

$(benchmarks): %: results/%/.done

results/%/.done:
	@mkdir -p results/$*
	@echo "Running $*..."
	@(cd results/$* && BENCHMARK_NAME=$* ${sniper} -p parsec-$* ${options} -c --general/output_dir=${root}/results/$*)
	@echo "Done with $*."
	@touch $@

setup:
	@redis-server configs/redis.conf

reset:
	@redis-cli flushall > /dev/null

kill:
	@killall -q -KILL -- pinbin mcpat.py bullet || echo -n
	@killall -q -KILL -- blackscholes x264 ferret || echo -n

clean:
	@rm -rf $(addprefix results/,$(benchmarks)) results/*.sqlite3

.PHONY: all $(benchmarks) server flush clean
