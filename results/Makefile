root := $(dir $(shell pwd))
export ARSENAL_ROOT = ${root}

options := -c gainestown
options += -s ${root}/scripts/squire.py
export SNIPER_OPTIONS = ${options}

suites := cpu2006 parsec

define declare_suite
$(1)-%:
	@$$(MAKE) -C $(1) $$*
endef

$(foreach suite,$(suites),$(eval $(call declare_suite,$(suite))))

clean: $(addsuffix -clean,$(suites))

kill: $(addsuffix -kill,$(suites))
	@killall -q -KILL -- pinbin mcpat.py squire || true

.PHONY: clean kill
