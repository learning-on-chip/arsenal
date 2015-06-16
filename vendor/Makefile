root := $(dir $(shell pwd))/root
bin := $(root)/bin
lib := $(root)/lib

ifeq ($(shell uname),Darwin)
suffix = dylib
else
suffix = so
endif

vendors := $(patsubst ./%,%,$(shell find . -maxdepth 1 ! -path . -type d))

all: $(vendors)

$(vendors): %: $(bin)/%

$(bin)/%:
	@echo "Installing $*..."
	@mkdir -p $(bin)
	@mkdir -p $(lib)
	@cd $* && cargo build --release
	@cp $*/target/release/$* $(bin)/
	@find $*/target/release/build -name lib*.$(suffix)* -exec cp {} $(lib)/ \;
	@echo "Done."

clean:
	@rm -rf $(addsuffix /target,$(vendors))
	@rm -rf $(bin) $(lib)

.PHONY: all $(vendors) clean
