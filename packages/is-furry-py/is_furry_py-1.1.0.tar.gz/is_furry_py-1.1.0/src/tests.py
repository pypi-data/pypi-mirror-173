import is_furry

tests: list[tuple[str, bool, bool]] = \
    [
        ("hello", False, False),
        ("hello owo", True, False),
        ("hello uwu", True, False),
        ("hello owo uwu", True, False),
        ("hello nowo", True, False),
        ("hello nowo", False, True),
        ("hello owo", True, False),
        ("Hello OwO", True, False),
        ("^w^", False, True),
        ("OwO~ x3", True, False),
    ]

fast_tests: list[tuple[str, bool]] = \
    [
        ("hello", False),
        ("hello owo", True),
        ("hello uwu", True),
        ("hello owouwu", True),
        ("hello o w o", False),
    ]


for test in tests:
    if len(test) > 2:
        result = is_furry.evaluate(test[0], test[2])
    else:
        result = is_furry.evaluate(test[0])

    if result != test[1]:
        print(f"Test failed: {test[0]}")
        print(f"Expected: {test[1]}")
        print(f"Actual: {result}")
        exit(1)
    else:
        print(f"Test passed: {test[0]}")

for test in fast_tests:
    result = is_furry.fast_evaluate(test[0])

    if result != test[1]:
        print(f"Test failed: {test[0]}")
        print(f"Expected: {test[1]}")
        print(f"Actual: {result}")
        exit(1)
    else:
        print(f"Test passed: {test[0]}")