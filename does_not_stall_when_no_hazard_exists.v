module Stall_Unit_tb;

  // Inputs
  reg MemRead1, MemRead2;
  reg [4:0] Dest_Reg_Num1, Dest_Reg_Num2, Read_Reg_Num1, Read_Reg_Num2;
  reg RegWrite1;
  reg [2:0] ALU_Opcode;

  // Outputs
  wire Cntrsrc, PC_Write, IF_Write;

  // Instantiate the Unit Under Test (UUT)
  Stall_Unit uut (
    .MemRead1(MemRead1),
    .MemRead2(MemRead2),
    .Dest_Reg_Num1(Dest_Reg_Num1),
    .Dest_Reg_Num2(Dest_Reg_Num2),
    .Read_Reg_Num1(Read_Reg_Num1),
    .Read_Reg_Num2(Read_Reg_Num2),
    .RegWrite1(RegWrite1),
    .ALU_Opcode(ALU_Opcode),
    .Cntrsrc(Cntrsrc),
    .PC_Write(PC_Write),
    .IF_Write(IF_Write)
  );

  initial begin
    $monitor("Time=%0t MemRead1=%b MemRead2=%b Dest_Reg_Num1=%d Dest_Reg_Num2=%d Read_Reg_Num1=%d Read_Reg_Num2=%d RegWrite1=%b ALU_Opcode=%b Cntrsrc=%b PC_Write=%b IF_Write=%b",
             $time, MemRead1, MemRead2, Dest_Reg_Num1, Dest_Reg_Num2, Read_Reg_Num1, Read_Reg_Num2, RegWrite1, ALU_Opcode, Cntrsrc, PC_Write, IF_Write);

    // Test case 1: No stall
    MemRead1 = 0; MemRead2 = 0; Dest_Reg_Num1 = 5'd1; Dest_Reg_Num2 = 5'd2; Read_Reg_Num1 = 5'd3; Read_Reg_Num2 = 5'd4; RegWrite1 = 0; ALU_Opcode = 3'b000;
    #10;

    // Test case 2: Memory read stall
    MemRead1 = 1; MemRead2 = 0; Dest_Reg_Num1 = 5'd1; Dest_Reg_Num2 = 5'd2; Read_Reg_Num1 = 5'd3; Read_Reg_Num2 = 5'd4; RegWrite1 = 0; ALU_Opcode = 3'b000;
    #10;

    // Test case 3: Memory read stall with ALU operation
    MemRead1 = 1; MemRead2 = 0; Dest_Reg_Num1 = 5'd1; Dest_Reg_Num2 = 5'd2; Read_Reg_Num1 = 5'd3; Read_Reg_Num2 = 5'd4; RegWrite1 = 0; ALU_Opcode = 3'b110;
    #10;

    // Test case 4: Register write stall
    MemRead1 = 0; MemRead2 = 0; Dest_Reg_Num1 = 5'd1; Dest_Reg_Num2 = 5'd2; Read_Reg_Num1 = 5'd3; Read_Reg_Num2 = 5'd4; RegWrite1 = 1; ALU_Opcode = 3'b110;
    #10;

    // Test case 5: Register write stall with ALU operation
    MemRead1 = 0; MemRead2 = 0; Dest_Reg_Num1 = 5'd1; Dest_Reg_Num2 = 5'd2; Read_Reg_Num1 = 5'd3; Read_Reg_Num2 = 5'd4; RegWrite1 = 1; ALU_Opcode = 3'b110;
    #10;

    $finish;
  end

endmodule