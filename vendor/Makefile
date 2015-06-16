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

color = $(shell tput setaf 2 || echo)

vendors := $(patsubst ./%,%,$(shell find . -maxdepth 1 ! -path . -type d))

all: $(vendors)
	@echo 'Well done! Now set your environment variables:'
	@echo $(color)'export ARSENAL_ROOT="$(root)"'
	@echo 'export PATH="$$ARSENAL_ROOT/tools/bin:$$PATH"'
	@echo 'export $(libraries)="$$ARSENAL_ROOT/tools/lib:$$$(libraries)"'

$(vendors): %: $(bin)/%

$(bin)/%:
	@echo "Installing $*..."
	@mkdir -p $(bin)
	@mkdir -p $(lib)
	@cd $* && cargo build --release
	@cp $*/target/release/$* $(bin)/
	@find $*/target/release/build -name lib*.$(suffix)* -exec cp {} $(lib)/ \;

clean:
	@rm -rf $(addsuffix /target,$(vendors))
	@rm -rf $(bin) $(lib)

.PHONY: all $(vendors) clean
