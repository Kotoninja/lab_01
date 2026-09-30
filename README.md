# Шаблон репозитория, для успешной сдачи лабораторных работ.

## Введение
Python-пакет `toolkit` с CLI, содержащий **калькулятор** и **конвертер величин**.

## Структура проекта

 <pre>
    .
    ├── lab<# лабораторной работы>             # Кодовая база вашей лабораторной работы
    │   ├── src/                               # Исходный код
    │   │   ├── toolkit/
    │   │   │   ├── сalculator.py              # Калькулятор
    │   │   │   ├── config.py                  # Загрузка конфига
    │   │   │   ├── constans.py                # Константные данные
    │   │   │   ├── converter.py               # Конвертер
    │   │   │   ├── errors.py                  # Ошибки
    │   │   │   ├── main.py                    # Сборка всей логики
    │   │   │   ├── repository.py              # Работа с json
    │   │   ├── config.json                    # Конфиг проекта
    │   ├── tests/                             # Unit тесты
    │   │   ├── calculator/
    │   │   │   ├── test_calculator.py         # Тесты калькулятора
    │   │   │   ├── test_validate.py           # Тесты валидации калькулятора
    │   │   ├── converter/
    │   │   │   ├── test_converter.py          # Тесты конвертера
    │   │   │   ├── test_validate.py           # Тесты валидации конвертера
    │   │   ├── test_parser.py                 # Проверка работы парсера
    │   ├── uv.lock                            # зависимости вашего проекта
    │   ├── report.pdf                         # Отчет
    │   ├── .gitignore                         # git ignore файл
    │   ├── .pre-commit-config.yaml            # Средства автоматизации проверки кодстайла
    │   ├── Makefile                           # Вспомогательные команды
    │   ├── check.sh                           # Проверка всего проекта
    │   ├── pyproject.toml
    │   ├── README.md                          # Описание вашего проекта, с описанием файлов и с титульником о том,
                                               # что и какая задача
</pre>
## Запуск
```bash
uv run python -m toolkit --help
```
## Использование
## Калькулятор
```bash
uv run python -m toolkit calc "EXPRESSION"
```
### Возможности
- целые и вещественные числа;
- бинарные операторы +, -, *, /, //, %;
- унарные + и - перед числом;
- скобки;
### Примеры
```bash
$ uv run python -m toolkit calc "2 + 2"
4

$ uv run python -m toolkit calc "2 + 2 * 2"
6

$ uv run python -m toolkit calc "10 / 4"
2.5

$ uv run python -m toolkit calc "-5 + 3"
-2

$ uv run python -m toolkit calc "1 / 0"
Division by zero.
$ echo $?
2
```

### Дополнительные возможности
// (целочисленное деление) и % (остаток):
```bash
$ uv run python -m toolkit calc "10 // 3"
3

$ uv run python -m toolkit calc "10 % 3"
1
```
скобки (recursive descent + RPN):
```bash
$ uv run python -m toolkit calc "(2 + 2) * 2"
8
```
- вычисления через Decimal с политикой округления по умолчанию (ROUND_HALF_EVEN);
- история успешных вычислений сохраняется в JSON
## Конвертер
```bash
python -m toolkit convert VALUE --from UNIT --to UNIT
```
## Поддерживаемые группы:
<pre>
Группа	        Единицы
Длина	        mm, cm, m, km
Масса	        g, kg
Температура	c, f, k
</pre>
## Правила
- регистр единиц не учитывается (M == m);
- конвертация между разными группами запрещена;
- температура ниже абсолютного нуля запрещена;
- результат — float.
## Примеры
```bash
$ uv run python -m toolkit convert 1 --from m --to mm
1000

$ uv run python -m toolkit convert 1 --from km --to m
1000

$ uv run python -m toolkit convert 1 --from kg --to g
1000

$ uv run python -m toolkit convert 1 --from c --to k
274

$ uv run python -m toolkit convert 1 --from c --to f
33.8
```
## Обработка ошибок
CLI выводит сообщение в stderr и завершается с кодом 2. Успешная команда — код 0.
Ошибки
<pre>
EmptyExpressionError                  пустое выражение
InvalidCharacterError                 недопустимый символ
MissingOperandError                   пропущенный операнд
ConsecutiveOperatorsError             два бинарных оператора подряд
InvalidNumberError                    неверное числовое значение
UnknownUnitError                      неизвестную единицу
IncompatibleUnitsError                несовместимые единицы
DivisionByZeroError                   деление на ноль
TemperaturesBelowAbsoluteZeroError    температура ниже абсолютного нуля
InvalidParenthesesError               неверная скобочная последовательность
</pre>

## Слои
### Калькулятор

    Tokenization — tokenization(expression):
    разбивает строку на токены, распознаёт отрицательные числа,
    проверяет недопустимые символы.

    Validation — validate, validate_tokenization, validate_parentheses:
    проверки на пустое выражение, два подряд идущих числа/оператора,
    корректность скобочной последовательности.

    Calculation — convert_infix_to_postfix + execute_expression:

        инфикс → постфикс (алгоритм сортировочной станции);

        вычисление постфикса стеком;

        арифметика через Decimal.
### Конвертер

    validate(args) — валидация единиц и физических ограничений;

    convert_units(value, flag_from, flag_to) — маршрутизация по группам;

    convert_length / convert_weight / convert_temperature — конкретные формулы;

    get_units_of_measurement(unit) — коэффициент из config.json.

## Тесты
```bash
uv run make test
```
coverage - 97%
