root := $(dir $(shell pwd))
export ARSENAL_ROOT = ${root}

options := -c gainestown
options += -s ${root}/scripts/recorder.py
export SNIPER_OPTIONS = ${options}

suites := cpu2006 cpu2006pinballs parsec

define declare_suite
$(1)-%:
	@$$(MAKE) -C $(1) $$*

clean: $(1)-clean

kill: $(1)-kill
endef

$(foreach suite,$(suites),$(eval $(call declare_suite,$(suite))))

kill:
	@killall -q -KILL -- pinbin mcpat.py recorder || true

.PHONY: clean kill
