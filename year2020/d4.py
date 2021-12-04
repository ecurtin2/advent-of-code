import re
from typing import List

from utils import split


def part1(inp: List[str]) -> int:
    fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
    ignore = {"cid"}
    required = fields - ignore
    n_valid = 0
    for chunk in split(inp, lambda s: s.strip() == ""):
        missing = required - set(dict(kv.split(":") for kv in " ".join(chunk).split()))
        if not missing:
            n_valid += 1
    return n_valid


def validate_hgt(x):
    match = re.match(r"(\d+)(in|cm)", x)
    if match:
        val, unit = match.groups()
        if unit == "cm":
            if 150 <= int(val) <= 193:
                return True
        elif unit == "in":
            if 59 <= int(val) <= 76:
                return True
    return False


def validate(raw: dict, validators: dict) -> List[str]:
    errors = []
    for field, validator in validators.items():
        try:
            if not validator(raw[field]):
                errors.append(f"Invalid field: {field}")
        except Exception as e:
            errors.append(f"Exception on field: {field}, {e}")
    return errors


def part2(inp: List[str]) -> int:
    validators = {
        "byr": lambda x: (len(x) == 4) and (1920 <= int(x) <= 2002),
        "iyr": lambda x: (len(x) == 4) and (2010 <= int(x) <= 2020),
        "eyr": lambda x: (len(x) == 4) and (2020 <= int(x) <= 2030),
        "hgt": validate_hgt,
        "hcl": lambda s: (re.match(r"#[\da-f]{6}", s) is not None) and len(s) == 7,
        "ecl": lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
        "pid": lambda s: (re.match(r"[0-9]{9}", s) is not None) and len(s) == 9,
    }
    valid = 0
    for chunk in split(inp, lambda s: s.strip() == ""):
        raw = dict(kv.split(":") for kv in " ".join(chunk).split())
        errs = validate(raw, validators)
        if not errs:
            valid += 1
    return valid


def test_part1():
    inp = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""
    assert part1(inp.splitlines()) == 2


def test_part2_invalid():
    invalid = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""
    assert part2(invalid.splitlines()) == 0


def test_part2_valid():
    valid = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
    """
    assert part2(valid.splitlines()) == 4
