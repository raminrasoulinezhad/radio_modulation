`timescale 1ns/1ps
module bn_relu_fp_tb();

	parameter NO_CH = 1;
	parameter BW_IN = 12;
	parameter BW_OUT = 12;
	parameter BW_A = 12;
	parameter BW_B = 12;
	parameter R_SHIFT = 6;
	parameter MAXVAL = -1;
	parameter DEBUG = 0;

	parameter clk_p = 1.0;
	parameter clk_p2= clk_p/2;

	localparam CYC = 4;

	reg clk;
	reg rst;

	reg vld_in;
	reg signed [NO_CH-1:0][BW_IN-1:0] data_in;
	reg signed [NO_CH-1:0][BW_IN-1:0] data_in_f;
	reg signed [NO_CH-1:0][BW_IN-1:0] data_in_1;
	reg signed [NO_CH-1:0][BW_IN-1:0] data_in_2;
	reg signed [NO_CH-1:0][BW_IN-1:0] data_in_3;

	wire vld_out;
	wire signed [NO_CH-1:0][BW_OUT-1:0] data_out;
	wire vld_out_accurate;
	wire signed [NO_CH-1:0][BW_OUT-1:0] data_out_accurate;
	
	reg signed [NO_CH-1:0][BW_A-1:0] a;
	reg signed [NO_CH-1:0][BW_B-1:0] b;

	reg signed [NO_CH-1:0][BW_OUT-1:0] out;
	reg signed [NO_CH-1:0][BW_OUT-1:0] out_1;
	reg signed [NO_CH-1:0][BW_OUT-1:0] out_2;
	reg signed [NO_CH-1:0][BW_OUT-1:0] out_3;
	reg signed [NO_CH-1:0][BW_OUT-1:0] out_4;

	initial begin 
		clk = 0;
		forever begin
			#clk_p2 clk= !clk;
		end
	end 

	integer i;
	initial begin
		for (i = 0; i < NO_CH; i = i + 1) begin
			data_in[i] = 0;
			a[i] = $random;
			b[i] = $random;

			out[i] = 0;
			out_1[i] = 0;
			out_2[i] = 0;
			out_3[i] = 0;
			out_4[i] = 0;
		end 
	end
		
	localparam BITS_MAX = ( R_SHIFT > BW_A ) ? R_SHIFT : BW_A;
	reg signed [BW_IN+BITS_MAX-1:0] temp_mult, temp_bias;
	reg signed [BW_OUT-1:0] temp_shift, temp_relu;
	reg temp_set_max, temp_set_zero;

	integer j, count;
	initial begin
		rst = 1;
		vld_in = 0;

		repeat(4) begin 
			@(posedge clk) begin 
				rst = 0;
			end
		end 

		count = 0;
		repeat (CYC + 10) begin
			@(posedge clk) begin
				#0.2
				for (j = 0; j < NO_CH; j = j + 1) begin
		
					data_in_3[j] = data_in_2[j];
					data_in_2[j] = data_in_1[j];
					data_in_1[j] = data_in_f[j];
					data_in[j] = $random;

					out_4[j] = out_3[j];
					out_3[j] = out_2[j];
					out_2[j] = out_1[j];
					out_1[j] = out[j];

					temp_mult = $signed( a[j] ) * $signed( data_in[j] );
					temp_bias = $signed(temp_mult) + $signed(b[j]);
					temp_set_zero = $signed( temp_bias ) < 0;
					temp_set_max = $signed( temp_bias[BW_IN+BITS_MAX-1:R_SHIFT] ) > MAXVAL;
					temp_shift = temp_bias[BW_OUT+R_SHIFT-1:R_SHIFT];

					if ( temp_set_zero ) begin
						temp_relu = 0;
					end else if ( MAXVAL > 0 & temp_set_max ) begin
						temp_relu = MAXVAL;
					end else begin
						temp_relu = temp_shift;
					end

					out[j] = temp_relu;
				end 
				
				if (count < CYC) begin
					vld_in = 1;
				end else begin 
					vld_in = 0;
				end

				if (vld_out) begin
					if (out_4 != data_out)begin 
						$display("baseline - error");
						$display("############################");
						$display("data_in_f: %f", $itor(data_in_f)/(2**(BW_IN-1)) );
						$display("data_in_1: %f", $itor(data_in_1)/(2**(BW_IN-1)) );
						$display("data_in_2: %f", $itor(data_in_2)/(2**(BW_IN-1)) );
						$display("data_in_3: %f", $itor(data_in_3)/(2**(BW_IN-1)) );

						$display("a: %f", a/(2**(BW_A-1)) );
						$display("b: %f", b/(2**(BW_B-1)) );
						
						$display("out: %f"     , $itor(out     )/(2**(BW_OUT-2)) );
						$display("out_1: %f"   , $itor(out_1   )/(2**(BW_OUT-2)) );
						$display("out_2: %f"   , $itor(out_2   )/(2**(BW_OUT-2)) );
						$display("out_3: %f"   , $itor(out_3   )/(2**(BW_OUT-2)) );
						$display("out_4: %f"   , $itor(out_4   )/(2**(BW_OUT-2)) );
						$display("data_out: %f", $itor(data_out)/(2**(BW_OUT-2)) );
						$display("############################");
					end else begin 
						$display("baseline - OK");
					end 
					
				end
				
				count = count + 1;

			end
		end

		repeat(4) begin 
			@(posedge clk) begin 
				vld_in = 0;
			end
		end 
		$stop;
	end

	bn_relu_fp #(
		NO_CH,
		BW_IN,
		BW_OUT,
		BW_A,
		BW_B,
		R_SHIFT,
		MAXVAL,
		DEBUG
	) bn_relu_fp_inst (
		.clk(clk),
		.rst(rst),

		.vld_in(vld_in),
		.data_in(data_in),

		.a(a),
		.b(b),

		.vld_out(vld_out),
		.data_out(data_out)
	);

	bn_relu_fp_accurate #(
		NO_CH,
		BW_IN,
		BW_OUT,
		BW_A,
		BW_B,
		R_SHIFT,
		MAXVAL,
		DEBUG
	) bn_relu_fp_accurate_inst (
		.clk(clk),
		.rst(rst),

		.vld_in(vld_in),
		.data_in(data_in),

		.a(a),
		.b(b),

		.vld_out(vld_out_accurate),
		.data_out(data_out_accurate)
	);

endmodule 
