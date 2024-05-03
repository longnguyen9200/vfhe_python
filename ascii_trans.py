def string_to_ascii_array(input_string):
    ascii_array = [ord(char) for char in input_string]
    return ascii_array

def ascii_array_to_string(ascii_array):
    result_string = ''.join(chr(char) for char in ascii_array)
    return result_string