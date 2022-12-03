# Advent of Code

## Run all days

```
just run
```
```
      Advent of Code 2022 Results      
┏━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Day ┃ Part ┃ Duration (ms) ┃ Answer ┃
┡━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1   │ 1    │  2.15         │ 67027  │
│ 1   │ 2    │  2.50         │ 197291 │
│ 2   │ 1    │  4.63         │ 9177   │
│ 2   │ 2    │  7.31         │ 12111  │
└─────┴──────┴───────────────┴────────┘
```

## Run a specific day
```
just run 1
```
```
      Advent of Code 2022 Results      
┏━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Day ┃ Part ┃ Duration (ms) ┃ Answer ┃
┡━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1   │ 1    │  4.51         │ 67027  │
│ 1   │ 2    │  9.92         │ 197291 │
└─────┴──────┴───────────────┴────────┘
```

## Run a specific day/part
```
just run 1 1
```
```
      Advent of Code 2022 Results      
┏━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Day ┃ Part ┃ Duration (ms) ┃ Answer ┃
┡━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1   │ 1    │  2.21         │ 67027  │
└─────┴──────┴───────────────┴────────┘
```

## Test all days
```
just test
```
```
=================== test session starts=============
platform linux -- Python 3.11.0, pytest-7.2.0, pluggy-1.0.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /advent-of-code, configfile: pytest.ini
collected 4 items        

year2022/d1.py::test_p1 PASSED
year2022/d1.py::test_p2 PASSED
year2022/d2.py::test_p1 PASSED
year2022/d2.py::test_p2 PASSED

================================== 4 passed in 0.02s ===========================
```

## Test one day

```
just test 1
```
```
====================== test session starts =====================================
platform linux -- Python 3.11.0, pytest-7.2.0, pluggy-1.0.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /advent-of-code, configfile: pytest.ini
collected 2 items                

year2022/d1.py::test_p1 PASSED
year2022/d1.py::test_p2 PASSED

================================ 2 passed in 0.01s =============================
```

## Test One day/part

```
just test 1 1
```
```
========================= test session starts ==================================
platform linux -- Python 3.11.0, pytest-7.2.0, pluggy-1.0.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /advent-of-code, configfile: pytest.ini
collected 2 items / 1 deselected / 1 selected     

year2022/d1.py::test_p1 PASSED

========================= 1 passed, 1 deselected in 0.02s =======================
```
