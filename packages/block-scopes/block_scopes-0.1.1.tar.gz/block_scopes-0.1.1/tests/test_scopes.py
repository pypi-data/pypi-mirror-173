"""
Does block scoping work correctly?
"""


def test_scoping():
    """Does block scoping work correctly?"""
    from scopes import scope

    A = "A"

    def B():
        return "B"

    C = __builtins__

    with scope("D"):
        D = True
        E = False

    A
    B
    C
    D

    try:
        E
    except NameError:
        pass
