ifndef BENCHMARKS_ROOT
$(error BENCHMARKS_ROOT should be defined)
endif

ifndef OUTPUT_ROOT
ifndef OUTPUT_DIR
$(error OUTPUT_ROOT or OUTPUT_DIR should be defined)
endif
endif

ifndef STUDIO_ROOT
$(error STUDIO_ROOT should be defined)
endif

ifndef TOOLBOX_ROOT
$(error TOOLBOX_ROOT should be defined)
endif

export SNIPER_BIN := ${BENCHMARKS_ROOT}/run-sniper

options := -c gainestown
options += --sim-end=last
options += -s ${STUDIO_ROOT}/script/recorder.py

define declare_benchmark
ifdef OUTPUT_DIR
${2}_output := ${OUTPUT_DIR}
else
${2}_output := ${OUTPUT_ROOT}/${1}/${2}
endif

${2}-%: $${${2}_output}/.${2}-%
	@exit 0

$${${2}_output}/.${2}-%:
	@(                                                                       \
	    program="${1}-${2}-$$*";                                             \
	    options="-d $${${2}_output} $$$$(./configure.py $$$${program})";     \
	    mkdir -p $${${2}_output};                                            \
	    cd $${${2}_output};                                                  \
	    echo "Start recording $$$${program}...";                             \
	    PROGRAM_NAME=$$$${program} $${SNIPER_BIN} $${options} $$$${options}; \
	    echo "Finish recording $$$${program}."                               \
	)
	@touch $$@

${2}-clean:
	@rm -rf $${${2}_output}

${2}-kill:
	@killall -q -KILL -- ${2} || true

.PHONY: ${2}-clean ${2}-kill
.PRECIOUS: $${${2}_output}/.${2}-%
endef

define declare_suite
ifdef INPUT_SIZE
all: $(addsuffix -${INPUT_SIZE},${2})
else
all:
	@echo "INPUT_SIZE should be defined"
	@exit 1
endif

$(foreach benchmark,${2},$(eval $(call declare_benchmark,${1},${benchmark})))

clean: $(addsuffix -clean,${2})

kill: $(addsuffix -kill,${2})

.PHONY: all clean kill
endef
