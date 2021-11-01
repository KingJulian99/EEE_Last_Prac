'timescale 1ns / 1ps;

module simple_cpu(
    clk, 
    rst, 
    instruction
);

    parameter DATA_WIDTH = 8; // 8-bit wide data
    parameter ADDR_BITS = 5; // 32 addresses
    parameter INSTR_WIDTH = 20; // 20b instruction

    input clk;
    input rst;
    input [INSTR_WIDTH-1:0] instruction;

    // CU wires
    wire [DATA_WIDTH-1:0] offset_i;
    wire sel1_i, sel3_i;
    wire [DATA_WIDTH-1:0] operand_1_i, operand_2_i;

    // Data memory wires
    wire [ADDR_BITS-1:0] addr_i;
    wire [DATA_WIDTH-1:0] data_in_i, data_out_i, result2_i;
    wire wen_i;

    // ALU wires
    wire [DATA_WIDTH-1:0] operand_a_i, operand_b_i, result1_i;
    wire [3:0] opcode_i;

    // Instantiating the CU, data memory & ALU.
    CU  #(DATA_WIDTH,ADDR_BITS, INSTR_WIDTH) CU1(clk, rst, instruction, result2_i, operand_1_i, operand_2_i, offset_i, opcode_i, sel1_i, sel3_i, wen_i);
    reg_mem  #(DATA_WIDTH,ADDR_BITS) data_memory(addr_i, data_in_i, wen_i, clk, data_out_i);
    alu #(DATA_WIDTH) alu1 (clk, operand_a_i, operand_b_i, opcode_i, result1_i);

    //Connecting the CU to the ALU
    assign operand_a_i = operand_1_i;
    if (sel3_i == 0) begin
      assign operand_b_i = operand_2_i;
    end else if (sel3_i == 1) begin
      assign operand_b_i = offset_i;
    end else begin
      assign operand_b_i = 8'bx;
    end
    
    //Connecting the CU to the Memory
    assign data_in_i = operand_2_i;
    assign addr_i = result1_i; 
    
    //Connecting the datamem to the CU
    if (sel1_i == 0) begin
      assign result2_i = data_out_i;
    end else if (sel1_i == 1) begin
      assign result2_i = result1_i;
    end else begin
      assign result2_i = 8'bx;
    end