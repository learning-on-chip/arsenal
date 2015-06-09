ifndef PINBALLS_ROOT
	$(error PINBALLS_ROOT should be defined)
endif

sniper := ${SNIPER_ROOT}/run-sniper

options := ${SNIPER_OPTIONS}

pinballs := $(patsubst cpu2006-%,%,$(notdir $(wildcard ${PINBALLS_ROOT}/cpu2006-*)))

$(pinballs): %: %/.done

%/.done:
	@mkdir -p $*
	@echo "Running cpu2006-$*..."
	@(cd $* && BENCHMARK_NAME=$* ${sniper} ${options} --pinballs=${PINBALLS_ROOT}/cpu2006-$*/pinball)
	@echo "Finished cpu2006-$*."
	@touch $@

clean:
	@rm -rf $(pinballs)

kill:

.PHONY: $(pinballs) clean kill
