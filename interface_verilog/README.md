# explanation:

	scheduler.v
		Top.v  ==AXI(4*16)==>  scheduler  <==AXI(4*16)==>  FPGA
 					  ||
					 512 bit (the first modulation_class * 16  bits are the results). Limitation: up to 32 classes.
					  ||
					  \/
					 HOST


	src:	
		Top.v: 
			The (i,q)-pair streamer to be used for implementation
		AXILite.v:
		symbols.v: 
			Memories including different modulation signals. 
		Modulators:
			The memories in symbols.v are picked by a mode selecting and used in Top.v to streams their data out.
	tb:
		tb.v:
			testing src/Top.v
	tools:
		symbols_gen.py
			it generates the memories in symbols.v

	Makefile: to synthesize the verilogs into "bin" directory



