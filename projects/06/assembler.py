"""
Hack Assembler – translates Hack assembly (.asm) into machine code (.hack).

Process:
  1. First pass: scan for labels, build symbol table.
  2. Second pass: translate instructions into 16-bit binary.
  3. Write the binary output to a .hack file.
"""

import sys
import re

class HackAssembler:
    # ---------- Lookup tables for C-instructions ----------
    dest_table = {
        'null': '000',
        'M':    '001',
        'D':    '010',
        'MD':   '011',
        'A':    '100',
        'AM':   '101',
        'AD':   '110',
        'AMD':  '111',
    }

    jump_table = {
        'null': '000',
        'JGT':  '001',
        'JEQ':  '010',
        'JGE':  '011',
        'JLT':  '100',
        'JNE':  '101',
        'JLE':  '110',
        'JMP':  '111',
    }

    # Comp table: 6-bit ALU control (a-bit is handled separately)
    comp_table = {
        '0':   '101010',
        '1':   '111111',
        '-1':  '111010',
        'D':   '001100',
        'A':   '110000',
        '!D':  '001101',
        '!A':  '110001',
        '-D':  '001111',
        '-A':  '110011',
        'D+1': '011111',
        'A+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D-A': '010011',
        'A-D': '000111',
        'D&A': '000000',
        'D|A': '010101',
    }

    def __init__(self):
        # Predefined symbols (RAM addresses)
        self.symbols = {
            'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3,
            'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
            'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
            'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
            'SCREEN': 16384,
            'KBD': 24576,
            'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4
        }
        # Next available RAM address for new variables (starts at 16)
        self.next_var_address = 16

    def first_pass(self, lines):
        """Scan for labels and build the symbol table. Remove label lines."""
        clean_lines = []
        line_num = 0
        for line in lines:
            line = line.split('//')[0].strip()   # remove comments, trim whitespace
            if not line:
                continue
            # Debug print (can be removed)
            print(type(line), repr(line))
            if line.startswith('('):
                # Label definition – store its ROM address
                label = line[1:-1]
                self.symbols[label] = line_num
            else:
                clean_lines.append(line)
                line_num += 1
        return clean_lines

    def second_pass(self, clean_lines):
        """Translate clean assembly lines into 16‑bit binary strings."""
        binary_output = []

        for line in clean_lines:
            if line.startswith('@'):
                # ---------- A-instruction ----------
                symbol = line[1:]
                if symbol.isdigit():
                    value = int(symbol)
                else:
                    # If symbol not in table, assign next free RAM address
                    if symbol not in self.symbols:
                        self.symbols[symbol] = self.next_var_address
                        self.next_var_address += 1
                    value = self.symbols[symbol]
                # 0 followed by 15‑bit address
                binary = '0' + format(value, '015b')
                binary_output.append(binary)

            else:
                # ---------- C-instruction ----------
                # Split off jump field
                if ';' in line:
                    rest, jump = line.split(';')
                else:
                    rest, jump = line, 'null'

                # Split off dest field
                if '=' in rest:
                    dest, comp = rest.split('=')
                else:
                    dest, comp = 'null', rest

                # Handle the a‑bit: when 'M' appears, replace with 'A' for lookup
                if 'M' in comp:
                    comp = comp.replace('M', 'A')
                    a_bit = '1'
                else:
                    a_bit = '0'

                comp_bits = a_bit + self.comp_table[comp]
                dest_bits = self.dest_table[dest]
                jump_bits = self.jump_table[jump]

                # C-instruction format: 111 + comp + dest + jump
                binary = '111' + comp_bits + dest_bits + jump_bits
                binary_output.append(binary)

        return binary_output

    def assemble(self, input_file, output_file):
        """Main assembly routine: read, process, write."""
        with open(input_file, 'r') as f:
            lines = f.readlines()

        clean_lines = self.first_pass(lines)
        binary_output = self.second_pass(clean_lines)

        with open(output_file, 'w') as f:
            for binary_line in binary_output:
                f.write(binary_line + '\n')


# ---------- Run the assembler ----------
if __name__ == '__main__':
    # Optionally take input file from command line
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'Add.asm'
    output_file = input_file.replace('.asm', '.hack')
    assembler = HackAssembler()
    assembler.assemble(input_file, output_file)

    # Batch assembly for common test programs (adjust paths as needed)
    assembler.assemble('Add.asm', 'Add.hack')
    assembler.assemble('Max.asm', 'Max.hack')
    assembler.assemble('Rect.asm', 'Rect.hack')
    assembler.assemble('Pong.asm', 'Pong.hack')
