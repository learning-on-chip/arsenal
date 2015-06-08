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
libs = glib gsl hooks imagick libxml2 ssl tbblib mesa zlib
tools = cmake libtool yasm

benchmarks := ${apps} ${kernels} ${libs} ${tools}

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

results/%/.done: server
	@mkdir -p results/$*
	@echo "Running $*..."
	@BENCHMARK_NAME=$* ${sniper} -p parsec-$* ${options} -c --general/output_dir=${root}/results/$*
	@echo "Done with $*."
	@touch $@

server:
	redis-server configs/redis.conf

flush:
	redis-cli flushall > /dev/null

clean:
	@rm -rf $(addprefix results/,$(benchmarks))

.PHONY: all $(benchmarks) server flush clean
