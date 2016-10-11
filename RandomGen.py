import random
import unittest


class RandomGen(object):
    # Values that may be returned by next_num()
    _random_nums = []
    # Probability of the occurence of random_nums
    _probabilities = []

    def __init__(self):
        assert len(self._probabilities) > 0
        assert len(self._probabilities) == len(self._random_nums)
        assert sum(self._probabilities) < 1.0

        # Calculate cummulative probabilities
        self.cum_prob = [0]
        for i in range(1, len(self._probabilities)+1):
            self.cum_prob.append(self.cum_prob[i-1] + self._probabilities[i-1])
        #self.cum_prob.append(1)

    def bisect(self, value):
        left = 0
        right = len(self.cum_prob)-1

        while True:
            mid = left + (right-left)/2
            if self.cum_prob[mid] <= value < self.cum_prob[mid+1]:
                return mid
            if value < self.cum_prob[mid]:
                right = mid
            elif value > self.cum_prob[mid]:
                left = mid

    def next_num(self):
        """
        Returns one of the randomNums. When this method is called
        multiple times over a long period, it should return the
        numbers roughly with the initialized probabilities.
        """
        while True:
            r = random.random()
            # Corner case: repeat if random number if greater than last cummulative prob.
            if r < self.cum_prob[-1]:
                break

        return self._random_nums[self.bisect(r)]


class TestRandomGen(unittest.TestCase):

    def generic_test(self, random_nums, probabilities):
        RandomGen._random_nums = random_nums
        RandomGen._probabilities = probabilities
        rg = RandomGen()

        # Run next_num() minimum 100 times or minium 100 x elements size
        N = max(100, len(random_nums)*100)
        distribution = {}
        for x in range(0, N):
            num = rg.next_num()
            distribution[num] = distribution.get(num, 0) + 1

        # Build expected probabilites map based on input
        expected_prob = {}
        for i in range(0, len(RandomGen._random_nums)):
            expected_prob[RandomGen._random_nums[i]] = RandomGen._probabilities[i]

        # Assert distribution
        for k, v in distribution.items():
            prob = v*1.0/N
            #print "{}: {} times ({})".format(k, v, prob)
            self.assertTrue(abs(expected_prob[k]-prob) < 100.0/N)

    def test0(self):
        with self.assertRaises(AssertionError):
            self.generic_test([], [])

    def test1(self):
        self.generic_test([1], [0.99])

    def test2(self):
        self.generic_test([1, 2], [0.5, 0.49])

    def test5a(self):
        self.generic_test([-1, 0, 1, 2, 3], [0.01, 0.3, 0.58, 0.1, 0.01])

    def test5b(self):
        self.generic_test([-1, 0, 1, 2, 3], [0.01, 0.3, 0.58, 0.1, 0.01])

    def test99(self):
        probs = [0.01] * 99
        nums = range(0, 99)
        self.generic_test(nums, probs)


if __name__ == '__main__':
    unittest.main()
