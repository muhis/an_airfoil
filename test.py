from wings import Wings, wing_from_data, selig_to_wing
def test():
    input_file = input('Please input file name: ')
    f = open(input_file, 'r').read().split('\n')
    return wing_from_data(f)
def test2():
    f = open('lednicer.txt').read().split('\n')
    return wing_from_data(f)
