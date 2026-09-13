import random

class DataGenerator:
    """Data generator for priority queue evaluation complying with assessment specs."""

    def gen_element(self):
        """Generates and returns an integer drawn uniformly at random from [0, 10^7]."""
        return random.randint(0, 10**7)

    def gen_push(self):
        """Returns a push operation in the form (1, key)."""
        return (1, self.gen_element())

    def gen_pop(self):
        """Returns a pop operation in the form (2, None)."""
        return (2, None)

    def gen_getTop(self):
        """Returns a getTop operation in the form (3, None)."""
        return (3, None)

    def gen_exp1_sequence(self, L):
        """Generates a push-only sequence of length L."""
        return [self.gen_push() for _ in range(L)]

    def gen_exp2_sequence(self, total_ops=1_000_000, gettop_pct=0.1):
        """Generates sequence sigma containing ONLY push and getTop operations probabilistically."""
        prob_gettop = gettop_pct / 100.0
        script = []
        for _ in range(total_ops):
            if random.random() < prob_gettop:
                script.append(self.gen_getTop())
            else:
                script.append(self.gen_push())
        return script

    def gen_exp3_sequence(self, total_ops=1_000_000, pop_pct=0.1):
        """Generates sequence sigma containing ONLY push and pop operations probabilistically."""
        prob_pop = pop_pct / 100.0
        script = []
        for _ in range(total_ops):
            if random.random() < prob_pop:
                script.append(self.gen_pop())
            else:
                script.append(self.gen_push())
        return script