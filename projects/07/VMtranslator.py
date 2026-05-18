import sys
import os

class VMTranslator:
    def __init__(self):
        self.output = []
        self.filename = ""
    
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

if __name__ == '__main__':
    translator = VMTranslator()
    translator.translate('SimpleAdd.vm', 'SimpleAdd.asm')