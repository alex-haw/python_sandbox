from colorama import Fore, Back, init, deinit
init()

class TUI:
    """
    +--------------+--------------+
    |              |              |
    |              |              |
    |              +--------------+
    |              |              |
    |              +--------------+
    |              |              |
    |              +--------------+
    |              |              |
    +--------------+--------------+
    """
    @classmethod
    def rows(cls): return [r.strip() for r in cls.__doc__.splitlines() if r and not r.isspace()]
    @classmethod
    def cols(cls): return [''.join(c) for c in zip(*cls.rows())]
    @classmethod
    def boxes(cls):
        rtab, ctab = [], []
        for r, row in enumerate(cls.rows()):
            if '+' in row:
                c = 0
                for rl in row.split('+')[:-1]:
                    if rl:
                        rl = rl.strip('|')
                        rtab.append((c+len(rl), r))
                    elif not c:
                        rtab.append((c, r))
                    c += len(rl)
        hlns, vlns = [], []
        for p in rtab:
            for q in [rtab[-1]] + rtab[:-1]:
                if q >= p:
                    if q[0] == p[0]:
                        hlns.append((*p, q[1]-p[1]))
                        if any([i<0 for i in hlns[-1]]): hlns.pop()
                        if hlns[-1][-1] == 0: hlns.pop()
                    if q[1] == p[1]:
                        vlns.append((*p, q[0]-p[0]))
                        if any([i<0 for i in vlns[-1]]): vlns.pop()
                        if vlns[-1][-1] == 0: vlns.pop()
        boxes = []
        for p in hlns:
            for q in vlns:
                if p[:2] == q[:2]:
                    boxes.append((p[2]+1, q[2]+1, p[1], p[0]))
        return boxes
    