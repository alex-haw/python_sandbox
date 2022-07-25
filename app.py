class do:
    c = True
    def __iter__(self):
        while self.c: yield self
    def __call__(self, *args):
        if not any(args): self.c = False
    While = __call__

o = 65
for do in do():
    
    print(chr(o))
    o += 1
    
    do.While(o < 75)