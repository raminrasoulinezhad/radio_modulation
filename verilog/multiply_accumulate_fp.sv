`timescale 1ns / 1ps

module multiply_accumulate_fp
#(
	parameter LOG2_NO_VECS = 2,

	parameter BW_IN = 16,
	parameter BW_OUT = 16,
	parameter BW_W = 2,
	
	// Check: R_SHIFT+BW_OUT < PACC_OUT_BW
	// for full-precision: "R_SHIFT = BW_W + BW_IN + $clog2(NUM_CYC) + LOG2_NO_VECS - BW_OUT"
	parameter R_SHIFT = 0,
	
	parameter DEBUG_FLAG = 0,
	parameter USE_UNSIGNED_DATA = 0,
	parameter NUM_CYC = 32
) (
	input clk,

	input new_sum,

	input [(1<<LOG2_NO_VECS)-1 : 0][BW_IN-1:0] data_in,
	input [(1<<LOG2_NO_VECS)-1 : 0][BW_W-1:0] w_vec,
	
	output [BW_OUT-1:0] data_out
);
	
	localparam NO_VECS = 1 << LOG2_NO_VECS;

	localparam LOG2_NUM_CYC = $clog2(NUM_CYC);
	localparam PACC_IN_BW = BW_W + BW_IN;
	//localparam BW_E = ( R_SHIFT > BW_W ) ? R_SHIFT : BW_W;
	//localparam PACC_OUT_BW = BW_E + BW_OUT;							//old
	localparam PACC_OUT_BW = PACC_IN_BW + LOG2_NUM_CYC + LOG2_NO_VECS;	//ideal
	
	reg signed [NO_VECS-1:0][PACC_IN_BW-1:0] mult_res;
	genvar i;
	generate
		for (i = 0; i < NO_VECS; i = i + 1) begin
			always @( posedge clk ) begin
				if ( USE_UNSIGNED_DATA ) begin
					mult_res[i] <= $signed( w_vec[i] * data_in[i] );
				end else begin
					mult_res[i] <= $signed( w_vec[i] ) * $signed( data_in[i] );
				end
			end
		end
	endgenerate

	reg new_sum_reg;
	always @( posedge clk ) begin
		new_sum_reg <= new_sum;
	end
	
	wire [PACC_OUT_BW-1:0] shift_res;
	pipelined_accumulator
	#(
		.IN_BITWIDTH(PACC_IN_BW),
		.OUT_BITWIDTH(PACC_OUT_BW),
		.LOG2_NO_IN(LOG2_NO_VECS)
	) accum (
		.clk(clk),
		.new_sum(new_sum_reg),
		.data_in(mult_res),
		.data_out(shift_res)
	);
	
	assign data_out = shift_res[R_SHIFT+BW_OUT-1 : R_SHIFT];

	always @( posedge clk ) begin
		if ( DEBUG_FLAG ) begin
			$display( "new_sum = %x, shift_res = %x", new_sum_reg, shift_res );
		end
	end

endmodule
