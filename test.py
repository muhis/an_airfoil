from converters import wing_from_data as wfd
from equity import equate
def test():
    input_file = input('Please input file name: ')
    f = open(input_file, 'r').read().split('\n')
    return wfd(f)
def test2():
    f = open('test_sample/lednicer.txt').read().split('\n')
    return wfd(f)
def test3():
    f = open('test_sample/bng.txt').read().split('\n')
    return wfd(f)
wing1 = test2()
wing2 = test3()
def test4():
    equate(wing1, wing2)
