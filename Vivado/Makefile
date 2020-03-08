.PHONY: clean run mult_cost run_script

mult_cost:	
	vivado -mode batch -source scripts/script_mult_cost.tcl

run:
	vivado -mode batch -source script.tcl

clean:
	rm -rf project* vivado*

run_script:
	vivado -mode batch -source $(script)	
