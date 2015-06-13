suites := cpu2006 parsec

define declare
$(1)-%:
	@$$(MAKE) -C $(1) $$*
endef

$(foreach suite,$(suites),$(eval $(call declare,$(suite))))

clean: $(addsuffix -clean,$(suites))

kill: $(addsuffix -kill,$(suites))

.PHONY: clean kill
