# LLM-Verilog-BenchGen
This project explores the use of Large Language Models (LLMs) for automatically generating Verilog testbenches for digital hardware design modules. The goal is to reduce manual effort and speed up the verification process by leveraging AI.

# Project Overview
The aim of this project is to use LLMs to generate testbenches for Verilog design modules. In this instance, the selected design is the Stall Unit of a 3-stage pipelined MIPS processor. The testbenches are intended to verify specific behaviors of the Stall Unit.

# Model Used
OriGen: A LoRA fine-tuned adapter on top of DeepSeek Coder 7B. It was the only model that successfully generated complete and clean Verilog testbenches. It demonstrated consistent syntax and structure, though it lacked feature-specific variation in the generated outputs.

# Alternate Models Explored
Several other open-source LLMs were tested before settling on OriGen:
- CodeGen (350M): Incomplete or irrelevant outputs, lacked capability for full testbench synthesis
- Mistral 7B: Required extensive prompt engineering; could only complete testbenches when partially provided
- StarCoder / CodeLlama: Too large to run efficiently on local machines or Colab; high memory and disk usage

These models showed limitations either in size, syntax accuracy, or generation completeness. OriGen proved to be the most accessible and performant option under realistic hardware constraints.

# Stall Unit Features Tested
Testbenches were generated for these verification features:
- Detects Load-Use Hazards Correctly
- Does Not Stall When No Hazard Exists
- Handles Consecutive Dependencies Properly

# Python Script: stallunit_llm_tb.py
This script performs the following:
1. Loads the DeepSeek Coder 7B + OriGen LLM
2. Iterates over predefined Stall Unit features
3. Generates Verilog testbenches based on each feature using the prompt template
4. Saves:
   - .v Verilog testbench files
   - Metadata to testbench_results.csv (tokens, generation time, etc.)

# How to Run Locally (with GPU)
1. Clone this repository
2. Set up a Python environment (preferably with Python 3.10 or 3.11)
```pip install torch transformers peft accelerate```
3. Run the script:
```python stallunit_llm_tb.py```

You must have enough GPU memory (at least 16GB) to run DeepSeek Coder 7B.

# How to Run in Google Colab
1. Upload **stallunit_llm_tb.py** and required folders to your Colab workspace
2. Ensure GPU is enabled under Runtime > Change runtime type
3. Install dependencies:
```!pip install torch transformers peft accelerate```
4. Run the script. Output files can be downloaded from Colab.

# Scope of the Project
- Demonstrate how LLMs can assist in automated testbench generation
- Evaluate performance and usability of multiple LLMs
- Lay the groundwork for expanding to more modules or fine-tuning better models
- Provide insights into prompt design and model behavior

# Known Limitations
- OriGen produced similar testbenches for all features, indicating weak feature differentiation
- Model outputs vary based on prompting quality and token limits

# Future Work
- Fine-tune models specifically on Verilog testbench datasets
- Integrate formal or simulation-based verification
- Expand to other processor units like ALU, forwarding unit, etc.
- Evaluate other LLMs

# Author
Pratheek Motamarri  
M.S. in Electrical Engineering   
Arizona State University  
If you have any questions, feel free to reach out to me at pratheek.motamarri@gmail.com

# License
This project is for educational and academic research purposes only.
