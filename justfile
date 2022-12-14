@test DAY='*' parts='' tb='native':
    python -m pytest year2022/d{{DAY}}.py -k test_p{{parts}} --tb={{tb}}

@run day='0' part='0' hide='--hide-answers' reps='5':
    python cli.py run --year=2022 --day={{day}} --part={{part}} {{hide}} --reps={{reps}}

@add day:
    python cli.py add {{day}}