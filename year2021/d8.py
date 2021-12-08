from collections import Counter
import pytest


def p1(inputs: str) -> int:
    in_out = [l.split("|") for l in inputs.splitlines()]
    outs = [x.strip() for l in in_out for x in l[1].split()]
    counts = Counter(len(o) for o in outs)
    return counts[2] + counts[3] + counts[4] + counts[7]


def p2(inputs: str) -> int:
    in_out = [l.split("|") for l in inputs.splitlines()]
    all_outputs = []
    for inputs, outputs in in_out:
        glyphs = [set(g) for g in inputs.split()]
        glyph_mapper = dict()
        for g in glyphs:
            l = len(g)
            if l == 2:
                glyph_mapper[1] = g
            elif l == 4:
                glyph_mapper[4] = g
            elif l == 3:
                glyph_mapper[7] = g
            elif l == 7:
                glyph_mapper[8] = g

        for g in glyphs:
            l = len(g)
            if l == 6:  # 6, 9, 0
                if not glyph_mapper[7].issubset(g):
                    glyph_mapper[6] = g
                if glyph_mapper[4].issubset(g):
                    glyph_mapper[9] = g
                if glyph_mapper[7].issubset(g) and not glyph_mapper[4].issubset(g):
                    glyph_mapper[0] = g
            if l == 5:  # 2, 3, 5
                if glyph_mapper[7].issubset(g):
                    glyph_mapper[3] = g
                if len(g - glyph_mapper[4]) == 3:
                    glyph_mapper[2] = g
                if len(g - glyph_mapper[4]) == 2 and not glyph_mapper[7].issubset(g):
                    glyph_mapper[5] = g

        def decode(s: str) -> int:
            for k, v in glyph_mapper.items():
                if set(s) == v:
                    return k
            raise KeyError(s)

        output_nums = [decode(g.strip()) for g in outputs.split()]
        output_num = int("".join(str(n) for n in output_nums))
        all_outputs.append(output_num)

    return sum(all_outputs)


@pytest.fixture()
def example():
    return """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def test_p1(example):
    assert p1(example) == 26


def test_p2_1():
    assert p2("""acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf""") == 5353


def test_p2(example):
    assert p2(example) == 61229
