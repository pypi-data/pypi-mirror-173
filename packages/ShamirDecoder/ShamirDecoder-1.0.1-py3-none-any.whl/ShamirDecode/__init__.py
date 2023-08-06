class ShamirDecoder:
    def __init__(self, shares, prime):
        self.shares = shares
        self.prime = prime

    def _extended_gcd(self, a, b):
        x = 0
        last_x = 1
        y = 1
        last_y = 0
        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y - quot * y, y
        return last_x, last_y

    def _modinv(self, num, den, p):
        inv, _ = self._extended_gcd(den, p)
        return inv * num

    def _lagrange_interpolation(self, x, x_s, y_s, p):
        k = len(x_s)
        assert k == len(set(x_s))

        def PI(vals):
            accumulate = 1
            for v in vals:
                accumulate *= v
            return accumulate
        nums = []
        dens = []
        for i in range(k):
            others = list(x_s)
            cur = others.pop(i)
            nums.append(PI(x-o for o in others))
            dens.append(PI(cur-o for o in others))
        den = PI(dens)
        num = sum([self._modinv(nums[i] * den * y_s[i] % p, dens[i], p)
                   for i in range(k)])
        return (self._modinv(num, den, p)+p) % p

    def _reconstruct_secret(self, shares, prime):
        x_s, y_s = zip(*shares)
        return self._lagrange_interpolation(0, x_s, y_s, prime)

    def decode(self):
        return self._reconstruct_secret(self.shares, self.prime)
