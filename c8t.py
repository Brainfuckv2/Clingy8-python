#!/usr/bin/env python

import argparse
import re
import os

def process_text(text):
    # Удаляем все пробелы
    text = text.replace(' ', '')
    
    # Разбиваем на строки и обрезаем каждую до первого |
    lines = text.split('\n')
    processed_lines = [line.split('|', 1)[0] for line in lines]
    text = '\n'.join(processed_lines)
    
    # Удаляем все переносы строк
    text = text.replace('\n', '')
    
    # Добавляем пробелы перед указанными символами
    chars_to_space = r'([+\-~\.\[!?@$&:\]])'
    text = re.sub(chars_to_space, r'\1 ', text)
    
    # Добавляем пробелы перед hex-парами (00-FF)
    text = re.sub(r'([0-9A-Fa-f]{2})', r'\1 ', text)
    
    return text

def main():
    parser = argparse.ArgumentParser(description='Токенизация Clingy8 Asm')
    parser.add_argument('-i', required=True, help='Входная строка или путь к файлу')
    parser.add_argument('-o', help='Путь к выходному файлу (если не указано - вывод в stdout)')
    args = parser.parse_args()
    
    if os.path.isfile(args.i):
        with open(args.i, 'r', encoding='utf-8') as f:
            input_text = f.read()
    else:
        input_text = args.i
    
    processed_text = process_text(input_text)
    
    if args.o:
        with open(args.o, 'w', encoding='utf-8') as f:
            f.write(processed_text)
    else:
        print(processed_text)

if __name__ == "__main__":
    main()