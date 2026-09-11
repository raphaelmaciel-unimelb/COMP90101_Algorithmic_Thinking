import random

class DataGenerator:
    def gen_element(self):
        """Generates and returns an integer drawn uniformly at random from [0, 10^7]."""
        num = random.randint(0, 10**7)
        return num

    def gen_push(self):
        """Returns a push operation in the form (1, key)."""
        key = self.gen_element()
        return (1, key)

    def gen_pop(self):
        """Returns a pop operation in the form (2)."""
        return (2,) # Using a tuple for consistency with gen_push

    def gen_getTop(self):
        """Returns a getTop operation in the form (3)."""
        return (3,) # Using a tuple for consistency
    
    def gen_exp1_sequence(self, L):
        sequence = []
        for i in range(L):
            sequence.append(self.gen_push())
        return sequence

    # def gen_exp2_sequence(self, L, getTop_percent):
    #     """Generates a sequence of length L with a mix of push and getTop."""
    #     sequence = []
        
    #     for i in range(L):
    #         roll = random.random()  # Roll the decimal die (e.g., 0.423)
            
    #         if roll < getTop_percent:
    #             # This block runs 'getTop_percent' amount of the time
    #             op = self.gen_getTop()
    #         else:
    #             # This block runs the rest of the time
    #             op = self.gen_push()
                
    #         sequence.append(op)
            
    #     return sequence

    def gen_exp2_sequence(self, total_ops=100000, gettop_pct=0):
        """Generates a script of total_ops operations with a specified % of getTop calls."""
        num_gettop = int(total_ops * (gettop_pct / 100.0))
        num_others = total_ops - num_gettop

        script = []
        
        # 60/40 push/pop split for non-read operations
        for _ in range(num_others):
            if random.random() < 0.6:
                script.append((1, random.randint(1, 1_000_000)))  # Push (2 elements)
            else:
                script.append((2, None))                          # Pop (2 elements)

        for _ in range(num_gettop):
            script.append((3, None))                              # getTop (2 elements)

        random.shuffle(script)
        return script

    # def gen_exp3_sequence(self, L, pop_percent):
    #     """Generates a sequence of length L with a mix of push and gen_pop()."""
    #     sequence = []
        
    #     for i in range(L):
    #         roll = random.random()  # Roll the decimal die (e.g., 0.423)
            
    #         if roll < pop_percent:
    #             # This block runs 'pop_percent' amount of the time
    #             op = self.gen_pop()
    #         else:
    #             # This block runs the rest of the time
    #             op = self.gen_push()
                
    #         sequence.append(op)
            
    #     return sequence

    def gen_exp3_sequence(self, total_ops=50000, pop_pct=0, prefill=20000):
        """
        Generates an operation script with a set % of pop() calls.
        Pre-fills initial elements to ensure pop() operations operate on non-empty data.
        """
        script = []
        # Step 1: Pre-fill items
        for _ in range(prefill):
            script.append((1, random.randint(1, 1_000_000)))

        # Step 2: Mix remaining pushes and pops based on percentage
        num_pops = int(total_ops * (pop_pct / 100.0))
        num_pushes = total_ops - num_pops

        workload = [(2, None)] * num_pops + [(1, random.randint(1, 1_000_000)) for _ in range(num_pushes)]
        random.shuffle(workload)

        script.extend(workload)
        return script
    
    def gen_exp4_list(self, N):
        """Generates an unsorted list of N random integers."""
        return [random.randint(1, 1_000_000) for _ in range(N)]