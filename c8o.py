import re

def tokenize_code(code: str):
    # Tokenizes the input assembly-like code into a list of meaningful tokens.
    lines = [re.split(r'\s*\|', line.strip())[0] for line in code.splitlines() if line.strip()]
    tokens = []
    for line in lines:
        tokens.extend(re.findall(r'[@$&:]|\d{2}|[+\-!?~.:\[\]]', line))
    return tokens

# Example usage
code = """ 
@01          | Переключаемся на ленту 1
:00 ?$04     | Инициализируем счетчик
:01 ?$00     | "Нечетное" число Фибоначчи
:02 ?$01     | "Четное" число Фибоначчи
:00 [        | Начинаем цикл
    :01 +:02 | Считаем "нечетное"
    :02 +:01 | Считаем "четное"
    :00 -$01 | Уменьшаем счетчик
]            | Когда :00 на значении 00, выходим из цикла
:02 !&01     | Записываем результат в регистр
@02          | Переключаемся на ленту 2
:00 ?&01     | Передаем результат в IO интерфейс (лента 2)
.            | Завершаем программу
"""

tokens = tokenize_code(code)
print(tokens)
