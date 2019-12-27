`timescale 1ns / 1ps
// 	This module windows the data It assumes that after a vld_in signal, the entire image will 
//	be sent for 2^(LOG2_IMG_SIZE) cycles This windower is used to produce multiple convolutional 
//	windows depending on the THROUGHPUT 

module windower
#(
	parameter NO_CH = 2,
	parameter LOG2_IMG_SIZE = 10,
	parameter THROUGHPUT = 1, // must be a power of 2
	parameter WINDOW = 3,
	parameter PADDDING = 1 // Ture = 1, No=0
	// throughput = 1 => 3, 3
	// throughput = 2 => 5, 4
	// throughput = 4 => 9, 6
	// throughput = 8 => 17, 10
) (
	input clk,
	input rst,
	
	input vld_in,
	input [NO_CH-1:0] data_in [THROUGHPUT-1:0],

	output logic vld_out,
	output logic [NO_CH-1:0] data_out [WINDOW-1:0]
);
	localparam NO_MEM = 2 * THROUGHPUT;
	localparam L2_TPUT = $clog2(THROUGHPUT);
	localparam PAD = (PADDDING) ? (WINDOW-1)/2 : 0;
	localparam L2_PAD = $clog2(PAD);
	localparam CNTR_MAX = 2**(LOG2_IMG_SIZE - L2_TPUT);

	localparam state_wait = 2'b00;
	localparam state_run = 2'b01;
	localparam state_autorun = 2'b10;
	
	integer i;
	integer j;

	reg [NO_CH-1:0] window_mem [WINDOW-1:0];
	reg [LOG2_IMG_SIZE-L2_TPUT-1:0] cntr;
	reg [L2_PAD:0] remaining;
	reg [1:0] state;

	// implement padding
	reg [NO_CH-1:0] zero [THROUGHPUT-1:0];
	always_comb begin
		for (j = 0; j < THROUGHPUT; j = j + 1) begin
			zero[j] = 0;
		end
	end

	always @( posedge clk ) begin
		if (rst) begin
			for (i = 0; i < WINDOW; i = i + 1) begin
				window_mem[i] <= 0;
			end
		end else if (vld_in && ((state == state_wait)|| (state == state_run))) begin
			window_mem[THROUGHPUT-1:0] <= data_in[THROUGHPUT-1:0];
			window_mem[WINDOW-1:THROUGHPUT] <= window_mem[WINDOW-1-THROUGHPUT:0];
		end else if (state == state_autorun) begin
			if (remaining != 0) begin
				window_mem[THROUGHPUT-1:0] <= zero[THROUGHPUT-1:0];
				window_mem[WINDOW-1:THROUGHPUT] <= window_mem[WINDOW-1-THROUGHPUT:0];		
			end else if (vld_in) begin  
				window_mem[THROUGHPUT-1:0] <= data_in[THROUGHPUT-1:0];
				window_mem[WINDOW-1:THROUGHPUT] <= window_mem[WINDOW-1-THROUGHPUT:0];
			end
		end
	end

	assign data_out = window_mem[WINDOW-1:0];

	always @(posedge clk) begin
		if (rst) begin
			cntr <= 0;			
			state <= state_wait;
			remaining <= PAD;
			vld_out <= 0;
		end
		else begin
			if (state == state_run) begin
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
			end else begin
				// it should be as same as reset
				cntr <= 0;			
				state <= state_wait;
				remaining <= PAD;
				vld_out <= 0;
			end

		end
	end

endmodule
