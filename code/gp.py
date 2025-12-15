import random
import matplotlib.pyplot as plt
import numpy as np
from joblib import delayed, Parallel

# This is the machine on which programs are executed
# The output is the value on top of the pile. 
class CPU:
    def __init__(self):
        self.stack=[]
    def reset(self):
        while len(self.stack)>0:self.stack.pop()

# These are the instructions
def AND(cpu, data):
    try:
        x1 = cpu.stack.pop()
        x2 = cpu.stack.pop()
        cpu.stack.append(x1 and x2)
    except IndexError:
        pass

def OR(cpu, data):
    try:
        x1 = cpu.stack.pop()
        x2 = cpu.stack.pop()
        cpu.stack.append(x1 or x2)
    except IndexError:
        pass

def XOR(cpu, data):
    try:
        x1 = cpu.stack.pop()
        x2 = cpu.stack.pop()
        cpu.stack.append(x1 ^ x2)
    except IndexError:
        pass

def NOT(cpu, data):
    try:
        x = cpu.stack.pop()
        cpu.stack.append(not x)
    except IndexError:
        pass  
    
# Push values of variables on the stack.      
def X1(cpu, data):
    cpu.stack.append(data[0])
def X2(cpu, data):
    cpu.stack.append(data[1])
def X3(cpu, data):
    cpu.stack.append(data[2])
def X4(cpu, data):
    cpu.stack.append(data[3])
    
# Execute a program
def execute(program,cpu, data):
    # TO DO
    cpu.reset()
    for i in range(len(program)):
        match program[i]:
            case "X1":
                X1(cpu, data)
            case "X2":
                X2(cpu, data)
            case "X3":
                X3(cpu, data)
            case "X4":
                X4(cpu, data)
            case "AND":
                AND(cpu, data)
            case "OR":
                OR(cpu, data)
            case "XOR":
                XOR(cpu, data)
            case "NOT":
                NOT(cpu, data)
    try:
        return cpu.stack.pop()
    # Case empty program
    except IndexError:
        return None



# Generate a random program
def randomProg(length,functionSet,terminalSet):
    rand = random.random()
    threshold = int(length * 1/3)
    operators = random.choices(functionSet, k=threshold)
    terminals = random.choices(terminalSet, k=(length - threshold))
    prog = operators + terminals
    random.shuffle(prog)
    return prog

# Computes the fitness of a program. 
# The fitness counts how many instances of data in dataSet are correctly computed by the program
def computeFitness(prog,cpu,dataSet):
    if execute(prog, cpu, dataSet[0]) == None:
        # invalid program
        return 0
    fitness = 0
    for data in dataSet:
        res = execute(prog, cpu, data)
        if res == data[-1]:
            fitness += 1
    return fitness



def k_tournament(gen: list, listOfFitness: list, k: int = 5) -> list:
    gen = np.array(gen)
    listOfFitness = np.array(listOfFitness)
    fitness = listOfFitness[:, 1]
    index = listOfFitness[:, 0]
    N = len(gen)
    newPopulation = [gen[index[np.argmax(fitness)]]]
    for i in range(1, N):
        selection = np.random.choice(N, size=k)
        selected = index[selection[np.argmax(fitness[selection])]]
        newPopulation.append(gen[selected])
    return newPopulation
        


    
# Selection using 2-tournament.
def selection(Population,cpu,dataSet):
    listOfFitness=[]
    for i in range(len(Population)):
        prog=Population[i]
        f=computeFitness(prog,cpu,dataSet)
        listOfFitness.append( (i,f) )
    newPopulation=k_tournament(Population, listOfFitness)
    return newPopulation

def crossover(Population,p_c):
    newPopulation=[]
    n=len(Population)
    i=0
    while(i<n):
        p1=list(Population[i])
        p2=list(Population[(i+1)%n])
        m=len(p1)
        if random.random()<p_c:  # crossover
            k=random.randint(1,m-1)
            newP1=p1[0:k]+p2[k:m]
            newP2=p2[0:k]+p1[k:m]
            p1=newP1
            p2=newP2
        newPopulation.append(p1)
        newPopulation.append(p2)
        i+=2
    return newPopulation

def mutation(Population,p_m,terminalSet,functionSet):
    newPopulation=[]
    nT=len(terminalSet)-1
    nF=len(functionSet)-1
    for p in Population:
        for i in range(len(p)):
            if random.random()>p_m:continue
            if random.random()<0.5: 
                p[i]=terminalSet[random.randint(0,nT)]
            else:
                p[i]=functionSet[random.randint(0,nF)]
        newPopulation.append(p)
    return newPopulation

#-------------------------------------

# LOOK-UP TABLE YOU HAVE TO REPRODUCE.
nbVar = 4
dataSet=[[0,0,0,0,0],[0,0,0,1,1],[0,0,1,0,0],[0,0,1,1,0],[0,1,0,0,0],[0,1,0,1,0],[0,1,1,0,0],[0,1,1,1,1],[1,0,0,0,0],[1,0,0,1,1],[1,0,1,0,0],[1,0,1,1,0],[1,1,0,0,0],[1,1,0,1,0],[1,1,1,0,0],[1,1,1,1,0]]
print(dataSet)

cpu=CPU()

# Function and terminal sets.
functionSet=["AND", "OR", "NOT", "XOR"]
terminalSet=["X1", "X2","X3", "X4"]

# Example of program.
prog=["X1", "X2", "AND", "X3", "OR"]
progLength = 5
prog=randomProg(progLength,functionSet,terminalSet)
print(prog)

# Execute a program on one row of the data set.
data = dataSet[0]
output=execute(prog,cpu,data)
print(output)
print("-------------")

# Parameters
progLength = 20
popSize = 100
p_c = 0.6
p_m = 0.1

# Generate the initial population
gen = [randomProg(progLength, functionSet, terminalSet) for _ in range(popSize)]

def best_fitness(gen: list, cpu: CPU, dataSet: list) -> int:
    fitness_list = [computeFitness(i, cpu, dataSet) for i in gen]
    return max(fitness_list), np.mean(fitness_list)

def ga(gen: list, cpu: CPU, dataSet: list) -> tuple:
    best = [best_fitness(gen, cpu, dataSet)[0]]
    mean = [best_fitness(gen, cpu, dataSet)[1]]
    for _ in range(200):
        gen = selection(gen, cpu, dataSet)
        gen = crossover(gen, p_c)
        gen = mutation(gen, p_m, terminalSet, functionSet)
        best.append(best_fitness(gen, cpu, dataSet)[0])
        mean.append(best_fitness(gen, cpu, dataSet)[1])
    return best, mean

# Evolution. Loop on the creation of population at generation i+1 from population at generation i, through selection, crossover and mutation.

results = Parallel(n_jobs=-1)(delayed(ga)(gen, cpu, dataSet) for _ in range(10))

results = np.array(results)
print(results)
print(type(results))

best = np.mean(results[:, 0], axis=0)
mean = np.mean(results[:, 1], axis=0)
best_overall = np.max(results[:, 0], axis=0)

plt.figure()

plt.plot(np.arange(len(best_overall)), best_overall, label="Best fitness overall")
plt.plot(np.arange(len(best)), best, label="Best fitness")
plt.plot(np.arange(len(mean)), mean, label="Mean fitness")
plt.title("Evolution of fitness")
plt.xlabel("iterations")
plt.ylabel("fitness")
plt.legend()
plt.show()

# Pourcentage de fitness qui ont atteint le max....