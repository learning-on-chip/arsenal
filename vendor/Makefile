root := $(dir $(shell pwd))
bin := $(root)/tools/bin
lib := $(root)/tools/lib

ifeq ($(shell uname),Darwin)
libraries = DYLD_LIBRARY_PATH
suffix = dylib
else
libraries = LD_LIBRARY_PATH
suffix = so
endif

green := $(shell tput setaf 2 || echo)
white := $(shell tput setaf 15 || echo)

vendors := $(patsubst ./%,%,$(shell find . -maxdepth 1 ! -path . -type d))

all: $(vendors)
	@echo 'Well done! Now set your environment variables:'
	@echo $(green)'export ARSENAL_ROOT="$(root)"'
	@echo 'export PATH="$$ARSENAL_ROOT/tools/bin:$$PATH"'
	@echo 'export $(libraries)="$$ARSENAL_ROOT/tools/lib:$$$(libraries)"'$(white)

$(vendors): %: $(bin)/%

define declare_vendor
$(bin)/$(1): $(shell find $(1)/src -name *.rs)
	@echo "Installing $(1)..."
	@mkdir -p $(bin)
	@mkdir -p $(lib)
	@cd $(1) && cargo build --release
	@cp $(1)/target/release/$(1) $(bin)/
	@find $(1)/target/release/build -name lib*.$(suffix)* -exec cp {} $(lib)/ \;
endef

$(foreach vendor,$(vendors),$(eval $(call declare_vendor,$(vendor))))

clean:
	@rm -rf $(addsuffix /target,$(vendors))
	@rm -rf $(bin) $(lib)

.PHONY: all $(vendors) clean
