#!/usr/bin/env python

import re
import sys
import argparse

def tokenize_code(code: str):
    lines = [re.split(r'\s*\|', line.strip())[0] for line in code.splitlines() if line.strip()]
    tokens = []
    for line in lines:
        tokens.extend(re.findall(r'[@$&:]|\d{2}|[+\-!?~.:\[\]]', line))
    return tokens

def main():
    parser = argparse.ArgumentParser(description='Tokenize C8 assembly-like code')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('code', nargs='?', help='Direct code input')
    
    args = parser.parse_args()

    if args.input:
        with open(args.input, 'r') as file:
            code = file.read()
    elif args.code:
        code = args.code
    else:
        print("Error: No input provided. Use -i for file input or provide code directly.")
        sys.exit(1)

    tokens = tokenize_code(code)
    
    if args.output:
        with open(args.output, 'w') as file:
            file.write(' '.join(tokens))
        print(f"Tokens written to {args.output}")
    else:
        print(' '.join(tokens))

if __name__ == "__main__":
    raise Exception("Сейчас токенизатор неправильно токенизирует код. Пожалуйста подождите пока мы это исправим.")
    # main()
