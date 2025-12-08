import random

# This is the machine on which programs are executed
# The output is the value on top of the pile. 
class CPU:
    def __init__(self):
        self.pile=[]
    def reset(self):
        while len(self.pile)>0:self.pile.pop()

# These are the instructions
def AND(cpu, data):
    # TO DO

def OR(cpu, data):
    # TO DO

def XOR(cpu, data):
    # TO DO

def NOT(cpu, data):
    # TO DO    
    
# Push values of variables on the stack.      
def X1(cpu, data):
    # TO DO
def X2(cpu, data):
    # TO DO
def X3(cpu, data):
    # TO DO
def X4(cpu, data):
    # TO DO
    
# Execute a program
def execute(program,cpu, data):
    # TO DO

# Generate a random program
def randomProg(length,functionSet,terminalSet):
    # TO DO

# Computes the fitness of a program. 
# The fitness counts how many instances of data in dataSet are correctly computed by the program
def computeFitness(prog,cpu,dataSet): 
    # TO DO
    
# Selection using 2-tournament.
def selection(Population,cpu,dataSet):
    listOfFitness=[]
    for i in range(len(Population)):
        prog=Population[i]
        f=computeFitness(prog,cpu,dataSet)
        listOfFitness.append( (i,f) )

    newPopulation=[]
    n=len(Population)
    for i in range(n):    
        i1=random.randint(0,n-1)
        i2=random.randint(0,n-1)
        if listOfFitness[i1][1]>listOfFitness[i2][1]:
            newPopulation.append(Population[i1])
        else:
            newPopulation.append(Population[i2])
    return newPopulation

def crossover(Population,p_c):
    newPopulation=[]
    n=len(Population)
    i=0
    while(i<n):
        p1=Population[i]
        p2=Population[(i+1)%n]
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
print dataSet

cpu=CPU()

# Function and terminal sets.
functionSet=["AND", "OR", "NOT", "XOR"]
terminalSet=["X1", "X2","X3", "X4"]

# Example of program.
prog=["X1", "X2", "AND", "X3", "OR"]
progLength = 5
prog=randomProg(progLength,functionSet,terminalSet)
print prog

# Execute a program on one row of the data set.
data = dataSet[0]
output=execute(prog,cpu,data)
print output
print "-------------"

# Parameters
popSize =
p_c =
p_m =

# Generate the initial population 

# Evolution. Loop on the creation of population at generation i+1 from population at generation i, through selection, crossover and mutation.

