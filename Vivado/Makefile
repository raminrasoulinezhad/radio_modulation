.PHONY: clean test_multiply_accumulate_fp test test2 run mult_cost

test_multiply_accumulate_fp:	
	vivado -mode batch -source scripts/script_multiply_accumulate_fp.tcl

mult_cost:	
	vivado -mode batch -source scripts/script_mult_cost.tcl

run:
	vivado -mode batch -source script.tcl

clean:
	rm -rf project* vivado*

test:	
	vivado -mode batch -source script_test.tcl

test2:	
	vivado -mode batch -source script_test2.tcl
