class do:
    """
    do-while for Python

    :yield: args should evaluate as True to loop again
    :rtype: callable

    >>> o = ord('A')
    >>> for While in do():
    ...    print(chr(o), end = '')
    ...    o += 1
    ...
    ...    While(o <= ord('Z'))
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    c = True
    def __iter__(self):
        while self.c: yield self
    def __call__(self, *args):
        self.c = all(args)