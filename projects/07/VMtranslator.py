import sys
import os

class VMTranslator:
    def __init__(self):
        self.output = []
        self.filename = ""
        self.label_counter = 0  
    
    def translate(self, input_file, output_file):
        self.filename = os.path.basename(input_file).replace('.vm', '')
        
        with open(input_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            # Remove comments and whitespace
            line = line.split('//')[0].strip()
            if not line:
                continue
            
            # Split into command and arguments
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
                self.write_arithmetic('add')
            
            # More commands coming later...
        
        with open(output_file, 'w') as f:
            for line in self.output:
                f.write(line + '\n')
    
    def write_push(self, segment, index):
        if segment == 'constant':
            self.output.append(f'@{index}')
            self.output.append('D=A')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif segment in ['local', 'argument', 'this', 'that']:
            base_map = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
            base = base_map[segment]
            self.output.append(f'@{base}')
            self.output.append('D=M')
            self.output.append(f'@{index}')
            self.output.append('A=D+A')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')
        
        elif segment == 'temp':
            self.output.append(f'@{5 + index}')   # RAM[5+2] = RAM[7]
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif segment == 'pointer':
            base = 3 + index   # pointer 0 = RAM[3] (THIS), pointer 1 = RAM[4] (THAT)
            self.output.append(f'@{base}')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif segment == 'static':
            self.output.append(f'@{self.filename}.{index}')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

    def write_pop(self, segment, index):
        if segment in ['local', 'argument', 'this', 'that']:
            base_map = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
            base = base_map[segment]
            self.output.append(f'@{base}')
            self.output.append('D=M')
            self.output.append(f'@{index}')
            self.output.append('D=D+A')   # D = base + index
            self.output.append('@R13')    # store address temporarily
            self.output.append('M=D')
            # Pop from stack
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            # Store at saved address
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
            self.output.append('D=M-D')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')



        elif command == 'neg':
            self.output.append('@SP')
            self.output.append('M=M-1')   # decrement SP
            self.output.append('A=M')     # go to top value
            self.output.append('D=-M')    # D = -(that value)
            self.output.append('M=D')     # store negated value back
            self.output.append('@SP')
            self.output.append('M=M+1')   # increment SP
        
        elif command == 'eq':
            label = self.label_counter
            self.label_counter += 1
            
            # Pop two values
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M-D')
            
            # If equal, jump to true
            self.output.append(f'@EQ_TRUE_{label}')
            self.output.append('D;JEQ')
            
            # False case
            self.output.append('D=0')
            self.output.append(f'@EQ_DONE_{label}')
            self.output.append('0;JMP')
            
            # True case
            self.output.append(f'(EQ_TRUE_{label})')
            self.output.append('D=-1')
            
            # Done
            self.output.append(f'(EQ_DONE_{label})')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')

        elif command == 'gt':
            label = self.label_counter
            self.label_counter += 1
            
            # Pop two values
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M-D')
            
            # If equal, jump to true
            self.output.append(f'@GT_TRUE_{label}')
            self.output.append('D;JGT')
            
            # False case
            self.output.append('D=0')
            self.output.append(f'@GT_DONE_{label}')
            self.output.append('0;JMP')
            
            # True case
            self.output.append(f'(GT_TRUE_{label})')
            self.output.append('D=-1')
            
            # Done
            self.output.append(f'(GT_DONE_{label})')
            self.output.append('@SP')
            self.output.append('A=M')
            self.output.append('M=D')
            self.output.append('@SP')
            self.output.append('M=M+1')


        elif command == 'lt':
            label = self.label_counter
            self.label_counter += 1
            
            # Pop two values
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M')
            self.output.append('@SP')
            self.output.append('M=M-1')
            self.output.append('A=M')
            self.output.append('D=M-D')
            
            # If equal, jump to true
            self.output.append(f'@LT_TRUE_{label}')
            self.output.append('D;JLT')
            
            # False case
            self.output.append('D=0')
            self.output.append(f'@LT_DONE_{label}')
            self.output.append('0;JMP')
            
            # True case
            self.output.append(f'(LT_TRUE_{label})')
            self.output.append('D=-1')
            
            # Done
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
    translator.translate('PointerTest.vm', 'PointerTest.asm') #change the name to other tests, also while running it make sure to change path to where the file is in cmd