# Time:  ctor:    O(n)
#        gather:  O(logn)
#        scatter: O(logn), amortized
# Space: O(n)

# Template:
# https://github.com/kamyu104/LeetCode-Solutions/blob/master/Python/longest-substring-of-one-repeating-character.py
class SegmentTree(object):
    def __init__(self, N,
                 build_fn=lambda _: None,
                 query_fn=lambda x, y: y if x is None else x if y is None else [max(x[0], y[0]), x[1]+y[1]],
                 update_fn=lambda x, y: y if x is None else [x[0]+y[0], x[1]+y[1]]):
        self.tree = [None]*(2*2**((N-1).bit_length()))
        self.base = len(self.tree)//2
        self.query_fn = query_fn
        self.update_fn = update_fn
        for i in xrange(self.base, self.base+N):
            self.tree[i] = build_fn(i-self.base)
        for i in reversed(xrange(1, self.base)):
            self.tree[i] = query_fn(self.tree[2*i], self.tree[2*i+1])

    def update(self, i, h):
        x = self.base+i
        self.tree[x] = self.update_fn(self.tree[x], h)
        while x > 1:
            x //= 2
            self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])

    def query(self, L, R):
        if L > R:
            return None
        L += self.base
        R += self.base
        left = right = None
        while L <= R:
            if L & 1:
                left = self.query_fn(left, self.tree[L])
                L += 1
            if R & 1 == 0:
                right = self.query_fn(self.tree[R], right)
                R -= 1
            L //= 2
            R //= 2
        return self.query_fn(left, right)


# design, segment tree
class BookMyShow(object):

    def __init__(self, n, m):
        """
        :type n: int
        :type m: int
        """
        self.__st = SegmentTree(n, build_fn=lambda _: [m]*2)
        self.__m = m
        self.__i = 0

    def gather(self, k, maxRow):
        """
        :type k: int
        :type maxRow: int
        :rtype: List[int]
        """
        i = 1
        if k > self.__st.tree[i][0]:
            return []
        while i < self.__st.base:
            i = 2*i+int(self.__st.tree[2*i][0] < k)
        if i-self.__st.base > maxRow:
            return []
        cnt = self.__m-self.__st.tree[i][0]
        i -= self.__st.base
        self.__st.update(i, [-k]*2)
        return [i, cnt]

    def scatter(self, k, maxRow):
        """
        :type k: int
        :type maxRow: int
        :rtype: bool
        """
        if k > self.__st.query(0, maxRow)[1]:
            return False
        for i in xrange(self.__i, maxRow+1):
            cnt = self.__st.tree[self.__st.base+i][1]
            c = min(cnt, k)
            self.__st.update(i, [-c]*2)
            cnt -= c
            if not cnt:
                self.__i += 1
            k -= c
            if not k:
                break
        return True
