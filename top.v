module top (
clk,
in0,
in1,
out0,
out1
);

input clk;
input [1:0] in0;
input in1;
output out0;
output out1;

wire [7:0] w0;
wire w1;
m0 i0 (.clk(clk), .in0(w0[7:0]),.in1(in0[1:0]), .out0(out0),.out1(w1));
m1 #(77) i1 (
.clk(clk), .in0(w1),.in1(in1), .out0(out1),.out1(w0[7:0])
);
endmodule
