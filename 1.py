def task(array):
    rev = array[::-1]
    try:
        rev_one = rev.index("1")
    except ValueError:
        rev_one = len(array)
    return len(array) - rev_one


print(task("1000011110000000000000000"))
print(task("10000000000000000000"))
print(task("100011111110000001110000000000"))