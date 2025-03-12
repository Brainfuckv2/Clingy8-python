#!/usr/bin/env python

import sys
import time
import argparse
import math

class Clingy8VM:
    def __init__(self, tokens, tape_size=256, debug=False, debug_delay=0.1):
        self.tokens = tokens
        self.debug = debug
        self.debug_delay = debug_delay
        
        # Память
        self.tapes = {
            0: self.tokens.copy(),  # Код программы неизменяем
            1: [0] * tape_size,
            2: [0] * tape_size
        }
        
        # Регистры
        self.registers = {i: 0 for i in range(4)}
        
        # Указатели
        self.LPTR = 0     # Текущая лента
        self.PPTR = 0     # Указатель инструкций
        self.DPTR = 0     # Указатель данных
        self.JPTR = 0     # Указатель цикла
        
    def prettify_tape(self, tape):
        tape_size = len(tape)
        sqrt_size = int(math.sqrt(tape_size))
        formatted_list = []
        
        for i, item in enumerate(tape):
            formatted_list.append(str(item))
            if (i + 1) % sqrt_size == 0:
                formatted_list.append('\n')
        return '\t' + '\t'.join(formatted_list)

    def get_register(self, reg):
        return self.registers.get(int(reg, 16), 0)
    
    def get_value(self, interface, data):
        match interface:
            case '$':
                return int(data, 16)
            case ':':
                return self.tapes[self.LPTR][int(data, 16)]
            case '&':
                return self.registers.get(int(data, 16), 0)
            case _:
                print(f"Ошибка: некорректный аргумент '{interface}{data}'")
                sys.exit(1)
    
    def run(self):
        while self.PPTR < len(self.tokens):
            token = self.tokens[self.PPTR]
            
            # Сбор аргументов для отладки
            debug_args = []
            if token in ['@', ':']:
                if self.PPTR + 1 < len(self.tokens):
                    debug_args.append(self.tokens[self.PPTR + 1])
            elif token in ['+', '-', '!', '?', '~']:
                if self.PPTR + 2 < len(self.tokens):
                    debug_args.extend(self.tokens[self.PPTR + 1:self.PPTR + 3])

            self.execute_token(token)
            
            if self.debug:
                self.print_debug(token, debug_args)
                time.sleep(self.debug_delay)
    
    def execute_token(self, token):
        match token:
            case '@':
                self.PPTR += 1  # Переходим к аргументу
                self.LPTR = int(self.tokens[self.PPTR], 16)
                if self.LPTR not in self.tapes:
                    print(f"Ошибка: несуществующая лента '{self.LPTR}'")
                    sys.exit(1)
                self.PPTR += 1  # Следующая инструкция
                
            case ':':
                self.PPTR += 1  # Переходим к аргументу
                self.DPTR = int(self.tokens[self.PPTR], 16)
                self.PPTR += 1  # Следующая инструкция
                
            case '+' | '-' | '!' | '?' | '~':
                self.handle_operation(token)
                
            case '[':
                if self.tapes[self.LPTR][self.DPTR] != 0:
                    self.JPTR = self.PPTR
                    self.PPTR += 1
                else:
                    # Пропускаем цикл
                    depth = 1
                    self.PPTR += 1
                    while self.PPTR < len(self.tokens) and depth > 0:
                        if self.tokens[self.PPTR] == '[':
                            depth += 1
                        elif self.tokens[self.PPTR] == ']':
                            depth -= 1
                        self.PPTR += 1
                        
            case ']':
                if self.tapes[self.LPTR][self.DPTR] == 0:
                    self.JPTR = 0
                    self.PPTR += 1
                else:
                    self.PPTR = self.JPTR  # Возврат к началу цикла
                    
            case '.':
                print(self.prettify_tape(self.tapes[2]))
                sys.exit(0)
                
            case _:
                print(f"Ошибка: неизвестный токен '{token}'")
                sys.exit(1)
    
    def handle_operation(self, operation):
        interface = self.tokens[self.PPTR + 1]
        data = self.tokens[self.PPTR + 2]
        
        match operation:
            case '+':
                self.tapes[self.LPTR][self.DPTR] += self.get_value(interface, data)
            case '-':
                self.tapes[self.LPTR][self.DPTR] -= self.get_value(interface, data)
            case '!':
                match interface:
                    case ':':
                        addr = int(data, 16)
                        self.tapes[self.LPTR][addr] = self.tapes[self.LPTR][self.DPTR]
                    case '&':
                        reg = int(data, 16)
                        self.registers[reg] = self.tapes[self.LPTR][self.DPTR]
                    case _:
                        print(f"Ошибка: некорректный аргумент '{interface}{data}'")
                        sys.exit(1)
            case '?':
                match interface:
                    case '@':
                        self.tapes[self.LPTR][self.DPTR] = self.LPTR
                    case _:
                        self.tapes[self.LPTR][self.DPTR] = self.get_value(interface, data)
            case '~':
                match interface:
                    case ':':
                        addr = int(data, 16)
                        current = self.tapes[self.LPTR][self.DPTR]
                        target = self.tapes[self.LPTR][addr]
                        self.tapes[self.LPTR][self.DPTR] = target
                        self.tapes[self.LPTR][addr] = current
                    case '&':
                        reg = int(data, 16)
                        current = self.tapes[self.LPTR][self.DPTR]
                        self.tapes[self.LPTR][self.DPTR] = self.registers[reg]
                        self.registers[reg] = current
                    case _:
                        print(f"Ошибка: некорректный аргумент '{interface}{data}'")
                        sys.exit(1)
        
        self.PPTR += 3  # Операция + интерфейс + данные
    
    def print_debug(self, token, args):
        args_str = ' '.join([f'`{arg}`' for arg in args]) if args else ''
        print(f"Token: `{token}` {args_str}".strip())
        print(f"LPTR: {self.LPTR}, PPTR: {self.PPTR}, DPTR: {self.DPTR}, JPTR: {self.JPTR}")
        # print(f"TAPE{self.LPTR}: {self.tapes[self.LPTR]}")
        print(f"TAPE{0}: {self.tapes[0]}")
        print(f"TAPE{1}: {self.tapes[1]}")
        print(f"TAPE{2}: {self.tapes[2]}")
        print(f"Registers: {self.registers}")
        print("---")

def read_tokens_from_file(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return file.read().split()

def main():
    parser = argparse.ArgumentParser(description='Run Clingy8VM with tokenized C8 code')
    parser.add_argument('input', help='Input file path (.c8t)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()

    tokens = read_tokens_from_file(args.input)
    vm = Clingy8VM(tokens, debug=args.debug)

    if args.output:
        original_stdout = sys.stdout
        with open(args.output, 'w') as file:
            sys.stdout = file
            vm.run()
        sys.stdout = original_stdout
        print(f"Output written to {args.output}")
    else:
        vm.run()

if __name__ == "__main__":
    main()