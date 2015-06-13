suits := cpu2006 parsec

cpu2006-%:
	@$(MAKE) -C cpu2006 $*

parsec-%:
	@$(MAKE) -C parsec $*

clean: $(addsuffix -clean,$(suits))
	@rm -f *.sqlite3

kill: $(addsuffix -kill,$(suits))

.PHONE: clean kill
