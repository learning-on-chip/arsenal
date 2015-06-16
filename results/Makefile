ifndef SNIPER_ROOT
$(error SNIPER_ROOT should be defined)
endif
ifndef SQUIRE_ROOT
$(error SQUIRE_ROOT should be defined)
endif

options := -c gainestown
options += -s ${root}/scripts/squire.py
export SNIPER_OPTIONS = ${options}

export TOOLS_ROOT = ${root}/tools
export RESULTS_ROOT = ${root}/results

suites := cpu2006 parsec

define declare
$(1)-%:
	@$$(MAKE) -C $(1) $$*
endef

$(foreach suite,$(suites),$(eval $(call declare,$(suite))))

clean: $(addsuffix -clean,$(suites))

kill: $(addsuffix -kill,$(suites))
	@killall -q -KILL -- pinbin mcpat.py squire || true

.PHONY: clean kill
