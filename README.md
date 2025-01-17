# SLY compiler
## Authors
- Jakub Ciszewski
- Mateusz Król
## Description
SLY compiler project based on [Sly Lex Yacc](https://sly.readthedocs.io/en/latest/#) Python library with
implemented lexer, parser, AST, type checker and interpreter. Created accoring to the
[course conspect](https://home.agh.edu.pl/~mkuta/tklab/).
## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```
## Testing
```bash
make test-scanner
make test-parser
make test-ast
make test-tc
make test-all
```