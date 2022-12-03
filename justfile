@test DAY='*' parts='':
    python -m pytest year2022/d{{DAY}}.py -k test_p{{parts}}

@run day='0' part='0':
    python cli.py --year=2022 --day={{day}} --part={{part}}

@add day:
    python cli.py add {{day}}