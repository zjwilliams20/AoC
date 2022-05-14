# util.py
# Contains various utilities for coding challenges.


class Point(object):
    """Point in 2D."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return str((self.x, self.y))


class Line(object):
    """Line segment in 2D with some number of points."""

    def __init__(self, pts):
        self._pts = pts

    def __getitem__(self, index):
        return self._pts[index]
    
    def __repr__(self):
        return ' -> '.join(map(str, self._pts))


class LineIter(Line):
    """Iterates over a Line object to generate points between pt1 and pt2, inclusive."""

    HORZ = 0
    VERT = 1
    DIAG = 2

    def __init__(self, pts, ignore_diags=True):
        assert len(pts) == 2
        super(LineIter, self).__init__(pts)
        self.ignore_diags = ignore_diags

        if self[0].x == self[1].x:
            self.type = self.VERT
        elif self[0].y == self[1].y:
            self.type = self.HORZ
        else:
            self.type = self.DIAG

    def __iter__(self):
        
        x_step = -1 if self[0].x > self[1].x else 1
        y_step = -1 if self[0].y > self[1].y else 1
        x_iter = iter(range(self[0].x, self[1].x + x_step, x_step))
        y_iter = iter(range(self[0].y, self[1].y + y_step, y_step))

        if self.type == self.VERT:
            for y in y_iter:
                yield (self[0].x, y)
        elif self.type == self.HORZ:
            for x in x_iter:
                yield (x, self[0].y)
        elif not self.ignore_diags:
            assert self.type == self.DIAG
            for x, y in zip(x_iter, y_iter):
                yield (x, y)

                