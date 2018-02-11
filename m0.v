module m0(
clk,
in0,
in1,
out0,
out1
);

input clk;
input [7:0] in0;
input [1:0] in1;
output out0;
output out1;

m1 #(1) i1 (.clk(clk), .in0(clk),.in1(1'h0), .out0(out0),.out1());
endmodule
