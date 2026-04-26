def crossover(par1, par2, rng=default_rng): #two chromosomes as inputs
        """Peforms single point crossover."""
        min_len = min(len(par1), len(par2))
        crossover_point = rng.integers(1, max(2, min_len))

        c1 = par1[:crossover_point] + par2[crossover_point:]
        c2 = par2[:crossover_point] + par1[crossover_point:]

        return c1, c2 #returns the chromosome

def mutate(self, rng=default_rng):
    """Applies mutation to each gene in the chromosome."""
    for i in range(0,len(self.chromosome)):
        for j in range(0,len(self.chromosome[i])):
            if rng.random() <= self.mut_rate: #mutation rate for each component of gene
                if j==0: #change gate type
                    self.chromosome[i][j] = rng.choice(Individual.gates) #set unneeded stuff to None
                elif j==1 or j==2: #target qubit + first control
                    if self.no_qu == 2: #swap target and control
                        self.chromosome[i][1], self.chromosome[i][2] = self.chromosome[i][2], self.chromosome[i][1]
                    else:
                        valid_gates = [k for k in range(0,Individual.no_qu) if (k != self.chromosome[i][1] and k != self.chromosome[i][2])]
                        self.chromosome[i][j] = rng.choice(valid_gates)
                elif j==3: #second control
                    if self.no_qu == 2: #or unneeded for this gate
                        pass
                    else: #don't even have a second control bit atm
                        self.chromosome[i][j] = rng.integers(0,Individual.no_qu)
                else: #change parameter by a small amount
                    self.chromosome[i][j] = (self.chromosome[i][j] + rng.normal(0,0.3)) % (2 * np.pi)