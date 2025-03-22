import torch
import time
import csv
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# === Model Setup ===
base_model = "deepseek-ai/deepseek-coder-7b-instruct-v1.5"
lora_model = "henryen/OriGen"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16,
    device_map="auto"
).to(device)
model = PeftModel.from_pretrained(model, lora_model)
model.eval()

# === Output folders ===
os.makedirs("verilog_outputs", exist_ok=True)
csv_file = "testbench_results.csv"

# === Define Stall Unit Features ===
features = [
    "Detects Load-Use Hazards Correctly",
    "Does Not Stall When No Hazard Exists",
    "Handles Consecutive Dependencies Properly"
]

# === CSV Header ===
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["feature", "num_tokens", "has_always", "gen_time_sec"])

# === Generate for each feature ===
for feature in features:
    print(f"\nGenerating testbench for: {feature}")
    
    prompt = """Instruction:
Please act as a professional Verilog verification engineer.
Write a complete Verilog testbench to verify the following feature of the Stall Unit module:
"{feature}"

Use `$monitor`, `initial` blocks, and representative test cases to verify the behavior.

### Verilog Module:
module Stall_Unit(
    input MemRead1,
    input MemRead2,
    input [4:0] Dest_Reg_Num1,
    input [4:0] Dest_Reg_Num2,
    input [4:0] Read_Reg_Num1,
    input [4:0] Read_Reg_Num2,
    input RegWrite1,
    input [2:0] ALU_Opcode,
    output reg Cntrsrc,
    output reg PC_Write,
    output reg IF_Write
);
always @(MemRead1, MemRead2, ALU_Opcode, Dest_Reg_Num1, Dest_Reg_Num2, RegWrite1, Read_Reg_Num1, Read_Reg_Num2) begin
    if ((MemRead1 == 1) && ((Dest_Reg_Num1 == Read_Reg_Num1) || (Dest_Reg_Num1 == Read_Reg_Num2))) begin
        Cntrsrc = 0;
        PC_Write = 0;
        IF_Write = 0;
    end else if ((MemRead2 == 1) && (ALU_Opcode == 3'b110) && ((Dest_Reg_Num1 == Read_Reg_Num1) || (Dest_Reg_Num1 == Read_Reg_Num2))) begin
        Cntrsrc = 0;
        PC_Write = 0;
        IF_Write = 0;
    end else if ((RegWrite1 == 1) && (ALU_Opcode == 3'b110) && ((Dest_Reg_Num1 == Read_Reg_Num1) || (Dest_Reg_Num1 == Read_Reg_Num2))) begin
        Cntrsrc = 0;
        PC_Write = 0;
        IF_Write = 0;
    end else begin
        Cntrsrc = 1;
        PC_Write = 1;
        IF_Write = 1;
    end
end
endmodule

Requirements for Testbench:
- Instantiate the `Stall_Unit` module
- Apply stimuli to verify the feature
- Use `initial` and `always` blocks
- Use `$monitor` to track outputs
- Include representative test cases
- Output **only the Verilog testbench code**

Response:
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    start_time = time.time()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1500,
            do_sample=False,
            temperature=0,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id
        )
    end_time = time.time()

    gen_time = round(end_time - start_time, 2)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    output_text = decoded.split("Response:")[-1].strip()

    num_tokens = len(tokenizer.tokenize(output_text))
    has_always = "always" in output_text

    # Save to .v file
    filename_safe = feature.replace(" ", "_").replace("-", "").lower()
    with open(f"verilog_outputs/{filename_safe}.v", "w") as f:
        f.write(output_text)

    # Log to CSV
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([feature, num_tokens, has_always, gen_time])

    print("Finished generating the testbenches.")
