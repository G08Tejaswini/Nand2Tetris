"""
VM Translator (Project 7) – translates VM commands into Hack assembly.
Handles stack arithmetic (add, sub, etc.) and memory access (push/pop)
for the basic segments: constant, local, argument, this, that, temp, pointer, static.
"""

import sys
import os

class VMTranslator:
    def __init__(self):
        self.output = []           # List of assembly instructions
        self.filename = ""          # Current .vm file name (for static segment)
        self.label_counter = 0      # Unique label counter for EQ, GT, LT

    def translate(self, input_file, output_file):
        """Main translation routine: reads a .vm file and writes .asm output."""
        self.filename = os.path.basename(input_file).replace('.vm', '')

        with open(input_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            # Remove comments and whitespace
            line = line.split('//')[0].strip()
            if not line:
                continue

            parts = line.split()
            command = parts[0]

            if command == 'push':
                segment = parts[1]
                index = int(parts[2])
                self.write_push(segment, index)

            elif command == 'pop':
                segment = parts[1]
                index = int(parts[2])
                self.write_pop(segment, index)

            elif command == 'add':
                # For Project 7, only 'add' is dispatched here.
                # In the full implementation, all arithmetic commands would be routed.
                self.write_arithmetic('add')

            # More commands would be added for Project 8 (sub, eq, gt, lt, etc.)

        with open(output_file, 'w') as f:
            for line in self.output:
                f.write(line + '\n')

    def write_push(self, segment, index):
        """Generate assembly to push a value from the given segment onto the stack."""
        if segment == 'constant':
            # Push the constant value itself
            self.output.append(f'@{index}')
            self.output.append('D=A')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif segment in ['local', 'argument', 'this', 'that']:
            # Push value from segment[index] where segment base is in LCL, ARG, THIS, THAT
            base_map = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
            base = base_map[segment]
            self.output.append(f'@{base}')
            self.output.append('D=M')          # D = base address
            self.output.append(f'@{index}')
            self.output.append('A=D+A')        # address = base + index
            self.output.append('D=M')          # D = value at that address
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')          # push D onto stack
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif segment == 'temp':
            # Temp segment fixed at RAM[5..12]
            self.output.append(f'@{5 + index}')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif segment == 'pointer':
            # Pointer 0 = THIS (RAM[3]), Pointer 1 = THAT (RAM[4])
            base = 3 + index
            self.output.append(f'@{base}')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif segment == 'static':
            # Static variables: filename.index
            self.output.append(f'@{self.filename}.{index}')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

    def write_pop(self, segment, index):
        """Generate assembly to pop a value from the stack into the given segment."""
        if segment in ['local', 'argument', 'this', 'that']:
            base_map = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
            base = base_map[segment]
            self.output.append(f'@{base}')
            self.output.append('D=M')
            self.output.append(f'@{index}')
            self.output.append('D=D+A')      # D = target address (base + index)
            self.output.append('@R13')        # temporarily store target address
            self.output.append('M=D')
            # Pop from stack
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')        # D = popped value
            # Store at target address
            self.output.append('@R13')
            self.output.append('A=M')
            self.output.append('M=D')

        elif segment == 'temp':
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append(f'@{5 + index}')
            self.output.append('M=D')

        elif segment == 'pointer':
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            base = 3 + index
            self.output.append(f'@{base}')
            self.output.append('M=D')

        elif segment == 'static':
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append(f'@{self.filename}.{index}')
            self.output.append('M=D')

    def write_arithmetic(self, command):
        """Generate assembly for stack arithmetic and logical operations."""
        if command == 'add':
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=D+M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif command == 'sub':
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M-D')      # Note: second popped - first popped
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif command == 'neg':
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=-M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif command == 'eq':
            label = self.label_counter
            self.label_counter += 1
            # Pop two values, compare
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M-D')
            # If D==0, jump to true
            self.output.append(f'@EQ_TRUE_{label}')
            self.output.append('D;JEQ')
            # False: push 0
            self.output.append('D=0')
            self.output.append(f'@EQ_DONE_{label}')
            self.output.append('0;JMP')
            # True: push -1
            self.output.append(f'(EQ_TRUE_{label})')
            self.output.append('D=-1')
            # End
            self.output.append(f'(EQ_DONE_{label})')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif command == 'gt':
            label = self.label_counter
            self.label_counter += 1
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M-D')
            # If D>0, jump to true
            self.output.append(f'@GT_TRUE_{label}')
            self.output.append('D;JGT')
            self.output.append('D=0')
            self.output.append(f'@GT_DONE_{label}')
            self.output.append('0;JMP')
            self.output.append(f'(GT_TRUE_{label})')
            self.output.append('D=-1')
            self.output.append(f'(GT_DONE_{label})')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif command == 'lt':
            label = self.label_counter
            self.label_counter += 1
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M-D')
            # If D<0, jump to true
            self.output.append(f'@LT_TRUE_{label}')
            self.output.append('D;JLT')
            self.output.append('D=0')
            self.output.append(f'@LT_DONE_{label}')
            self.output.append('0;JMP')
            self.output.append(f'(LT_TRUE_{label})')
            self.output.append('D=-1')
            self.output.append(f'(LT_DONE_{label})')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif command == 'and':
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=D&M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif command == 'or':
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=D|M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif command == 'not':
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=!M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')


if __name__ == '__main__':
    translator = VMTranslator()
    translator.translate('PointerTest.vm', 'PointerTest.asm')
    # To test other files, change the input filename above or pass as command-line argument
