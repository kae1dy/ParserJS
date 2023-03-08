from func import parse_code

if __name__ == '__main__':
    tokens = parse_code()
    print(f"Example list of tokens: {tokens[0]}.\n"
          f"Length of all array of arrays: {len(tokens)}.\n")
