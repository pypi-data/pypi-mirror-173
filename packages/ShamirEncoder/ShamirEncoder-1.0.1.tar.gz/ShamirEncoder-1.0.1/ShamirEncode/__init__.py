class ShamirEncoder:
    def __init__(self, prime, secret, number_shares, threshold):
        self.prime = prime
        self.secret = secret
        self.number_shares = number_shares
        self.threshold = threshold

    # Random integer
    def _rint(self):
        import random
        return random.SystemRandom().randint(0, self.prime)

    # Random polynomial
    def _eval_at(self, poly, x, prime):
        accumulate = 0
        for i in reversed(poly):
            accumulate *= x
            accumulate += i
            accumulate %= prime
        return accumulate

    # Generate a random sharing
    def _make_random_shares(self):
        if(self.threshold > self.number_shares):
            raise ValueError("Pool secret would be irrecoverable.")
        poly = [self.secret]+[self._rint()for i in range(self.threshold-1)]
        shares = [(i, self._eval_at(poly, i, self.prime))
                  for i in range(1, self.number_shares+1)]
        return shares, poly

    def encode(self):
        shares, polynomial = self._make_random_shares()
        return shares, polynomial
