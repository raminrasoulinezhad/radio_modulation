`timescale 1ns / 1ps
/* This module windows the data
 It assumes that after a vld_in signal, the entire image will be sent for 2^(LOG2_IMG_SIZE) cycles
 This windower is used to produce multiple convolutional windows depending on the THROUGHPUT
 */
module windower_serial_ramin
#(
	parameter NO_CH = 2,
	parameter LOG2_IMG_SIZE = 10,
	parameter WINDOW_SIZE = 3, 	// only works for 3 currently
	parameter SER_CYC = 1 		// must be a power of 2
) (
	input clk,
	input rst,

	input vld_in,
	input [NO_CH-1:0] data_in,
	
	output logic vld_out,
	output logic [NO_CH-1:0] data_out [WINDOW_SIZE-1:0],
	
	output ser_rst
);

	localparam LOG2_SER = $clog2(SER_CYC);
	localparam LOG2_W_S = $clog2(WINDOW_SIZE);
	localparam CNTR_MAX = 2**(LOG2_IMG_SIZE+LOG2_SER);

	localparam state_wait = 2'b00;
	localparam state_run = 2'b01;
	localparam state_autorun = 2'b10;

	parameter PAD = SER_CYC * ((WINDOW_SIZE-1)/2);

	reg [NO_CH-1:0] window_mem_a;
	reg [NO_CH-1:0] window_mem [WINDOW_SIZE-2:0][SER_CYC-1:0];
	
	reg [LOG2_IMG_SIZE+LOG2_SER-1:0] cntr;
	
	reg running;
	
	//reg [LOG2_SER+LOG2_W_S-1:0] img_fill; // count until window is filled after 2 inputs ( doesn't matter what the throughput is )
	reg [LOG2_SER+LOG2_W_S-1:0] remaining;
		
	wire [NO_CH-1:0] zero;
	assign zero = 0;

	assign ser_rst = (cntr[LOG2_SER-1:0] == 0);

	reg [1:0] state;

	/*
	// implement padding
	reg [WINDOW_SIZE-1:0] data_out_is_zero;
	integer j;
	always @(*) begin
		for (j = 0; j < WINDOW_SIZE; j = j + 1) begin
			if (j < ((WINDOW_SIZE-1)/2)) begin
				data_out_is_zero[j] = ( cntr >= ( 1 << ( LOG2_IMG_SIZE + LOG2_SER ) ) - ((j+1)*SER_CYC) );
			end else if (j == ((WINDOW_SIZE-1)/2)) begin
				data_out_is_zero[j] = 1'b0;
			end else begin
				data_out_is_zero[j] = ( cntr < ((WINDOW_SIZE-j)*SER_CYC) );
			end 
		end	
	end

	integer k;
	always @( posedge clk ) begin
		if ( vld_in || ( ( cntr_nxt == 0 | cntr_filled == 0 ) & !vld_in ) ) begin
			for (k = 0; k < WINDOW_SIZE; k = k + 1) begin
				if (k == 0) begin
					data_out[k] <= data_out_is_zero[k] ? zero : window_mem_a;
				end else begin
					data_out[k] <= data_out_is_zero[k] ? zero : window_mem[k-1][SER_CYC-1];
				end
			end	
		end
	end

	integer i;
	always @( posedge clk ) begin
		if ( vld_in || ( ( cntr_nxt == 0 | cntr_filled == 0 ) & !vld_in ) ) begin
			window_mem_a <= data_in;
			for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
				if (i == 0) begin
					window_mem[i][0] <= window_mem_a;
				end else begin 
					window_mem[i][0] <= window_mem[i-1][SER_CYC-1];
				end
				window_mem[i][SER_CYC-1:1] <= window_mem[i][SER_CYC-2:0];
			end
		end
	end
	*/

	
	integer i, j;
	always @( posedge clk ) begin
		if (rst) begin
			window_mem_a <= 0;
			for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
				for (j = 0; j < SER_CYC; j = j + 1) begin
					window_mem[i][j] <= 0;
				end
			end
		end else if (vld_in && ((state == state_wait)|| (state == state_run))) begin
			window_mem_a <= data_in;
			for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
				if (i == 0) begin
					window_mem[i][0] <= window_mem_a;
				end else begin 
					window_mem[i][0] <= window_mem[i-1][SER_CYC-1];
				end
				window_mem[i][SER_CYC-1:1] <= window_mem[i][SER_CYC-2:0];
			end
		end else if (state == state_autorun) begin
			if (remaining != 0) begin
				window_mem_a <= 0;
				for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
					if (i == 0) begin
						window_mem[i][0] <= window_mem_a;
					end else begin 
						window_mem[i][0] <= window_mem[i-1][SER_CYC-1];
					end
					window_mem[i][SER_CYC-1:1] <= window_mem[i][SER_CYC-2:0];
				end	
			end else if (vld_in) begin  
				window_mem_a <= data_in;
				for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
					if (i == 0) begin
						window_mem[i][0] <= window_mem_a;
					end else begin 
						window_mem[i][0] <= window_mem[i-1][SER_CYC-1];
					end
					window_mem[i][SER_CYC-1:1] <= window_mem[i][SER_CYC-2:0];
				end
			end
		end
	end

	// output manager
	integer k;
	always @(*) begin
		for (k = 0; k < WINDOW_SIZE; k = k + 1) begin
			if (k == 0) begin
				data_out[k] <= window_mem_a;
			end else begin
				data_out[k] <= window_mem[k-1][SER_CYC-1];
			end
		end	
	end

	// State machine 
	always @( posedge clk ) begin
		if ( rst ) begin
			cntr <= 0;
			remaining <= PAD; 
			running <= 0;
			vld_out <= 0;
			state <= 0;
		end else begin
			
			unique if (state == state_run) begin
				if (vld_in)begin
					vld_out <= 1;
					if (cntr == (CNTR_MAX-PAD-2)) begin
						state <= state_autorun;
						remaining = PAD;
					end else begin 
						cntr <= cntr + 1;
					end 
				end else begin
					vld_out <= 0;
				end
			end else if (state == state_autorun) begin
				if (remaining != 0) begin
					remaining <= remaining - 1;
					vld_out <= 1;
				end else begin  
					vld_out <= 0;
					state <= state_wait;
					cntr <= 0;
					if (vld_in) begin
						remaining <= PAD - 1;
					end else begin
						remaining <= PAD;
					end
				end
			end else if (state == state_wait) begin 
				if (vld_in) begin
					if (remaining == 0) begin
						state <= state_run;
						vld_out <= 1;
						cntr <= 0;
					end else begin
						remaining <= remaining - 1;
					end
				end
			end
		end
	end

endmodule
