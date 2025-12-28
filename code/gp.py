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
    if len(cpu.stack) < 2:
        return
    try:
        x1 = cpu.stack.pop()
        x2 = cpu.stack.pop()
        cpu.stack.append(x1 and x2)
    except IndexError:
        pass

def OR(cpu, data):
    if len(cpu.stack) < 2:
        return
    try:
        x1 = cpu.stack.pop()
        x2 = cpu.stack.pop()
        cpu.stack.append(x1 or x2)
    except IndexError:
        pass

def XOR(cpu, data):
    if len(cpu.stack) < 2:
        return
    try:
        x1 = cpu.stack.pop()
        x2 = cpu.stack.pop()
        cpu.stack.append(x1 ^ x2)
    except IndexError:
        pass

def NOT(cpu, data):
    if len(cpu.stack) < 1:
        return
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
def selection(Population,cpu,dataSet, k: int = 2):
    listOfFitness=[]
    for i in range(len(Population)):
        prog=Population[i]
        f=computeFitness(prog,cpu,dataSet)
        listOfFitness.append( (i,f) )
    newPopulation=k_tournament(Population, listOfFitness, k=k)
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

def evaluate_population(gen: list, cpu: CPU, dataSet: list) -> tuple:
    """Evaluate population and return statistics"""
    fitness_list = [computeFitness(i, cpu, dataSet) for i in gen]
    return max(fitness_list), np.mean(fitness_list), np.std(fitness_list), fitness_list

def ga(gen: list, cpu: CPU, dataSet: list, max_generations: int = 200, k: int = 2, p_c: float = 0.6, p_m: float = 0.1) -> tuple:
    """Enhanced GA with more statistics"""
    best = []
    mean = []
    std = []
    percent_max = []  # Track percentage reaching maximum fitness
    max_possible_fitness = len(dataSet)  # 16 for this problem
    
    for generation in range(max_generations):
        # Get current population stats
        best_fit, mean_fit, std_fit, fitness_list = evaluate_population(gen, cpu, dataSet)
        best.append(best_fit)
        mean.append(mean_fit)
        std.append(std_fit)
        
        # Calculate percentage reaching maximum
        count_max = sum(1 for f in fitness_list if f == max_possible_fitness)
        percent_max.append((count_max / len(gen)) * 100)
        
        # Evolution steps
        gen = selection(gen, cpu, dataSet, k=k)
        gen = crossover(gen, p_c)
        gen = mutation(gen, p_m, terminalSet, functionSet)
    
    return best, mean, std, percent_max

def run_experiments(configurations, num_samples=100, max_generations=100, show_variance=True):
    """Run experiments with configurable number of samples"""
    # Store results for all configurations
    all_results = {}

    for config in configurations:
        print(f"Running {config['name']} with {num_samples} samples...")
        # Use custom parameters
        prog_length = config.get('prog_length', 20)
        pop_size = config.get('pop_size', 100)
        k = config.get('k', 2)
        p_c = config.get('p_c', 0.6)
        p_m = config.get('p_m', 0.1)
        
        # Run multiple samples in parallel
        results = Parallel(n_jobs=-1)(
            delayed(ga)([randomProg(prog_length, functionSet, terminalSet) for _ in range(pop_size)], 
                       CPU(), dataSet, max_generations, k, p_c, p_m) 
            for _ in range(num_samples)
        )
        
        # Extract and process results
        best_results = np.array([r[0] for r in results])
        mean_results = np.array([r[1] for r in results])
        std_results = np.array([r[2] for r in results])
        percent_results = np.array([r[3] for r in results])
        
        all_results[config['name']] = {
            'best_mean': np.mean(best_results, axis=0),
            'best_std': np.std(best_results, axis=0),
            'mean_mean': np.mean(mean_results, axis=0),
            'mean_std': np.std(mean_results, axis=0),
            'percent_mean': np.mean(percent_results, axis=0),
            'percent_std': np.std(percent_results, axis=0),
            'generations': np.arange(len(best_results[0])),
            'config': config,  # Store configuration for plotting
            'num_samples': num_samples  # Store sample count
        }
    
    return all_results

def plot_population_analysis(all_results, show_variance=True):
    """Create focused plots for population size analysis with 6 subplots"""
    plt.figure(figsize=(20, 12))
    
    # Get the number of samples
    sample_count = next(iter(all_results.values()))['num_samples']

    # Plot 1: Population Size Comparison - Best Fitness
    plt.subplot(2, 3, 1)
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    pop_configs = [name for name in all_results.keys() if 'Population' in name and 'tournament' not in name.lower()]
    
    for i, name in enumerate(pop_configs):
        data = all_results[name]
        config = data['config']
        color = colors[i % len(colors)]
        gens = data['generations']
        pop_size = config.get('pop_size', 100)
        label = f"Pop {pop_size}"
        
        plt.plot(gens, data['best_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['best_mean'] - data['best_std'], 
                             data['best_mean'] + data['best_std'], alpha=0.3, color=color)
    plt.title(f"Population Size - Best Fitness (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Population Size Comparison - Mean Fitness (ALWAYS show variance)
    plt.subplot(2, 3, 2)
    for i, name in enumerate(pop_configs):
        data = all_results[name]
        config = data['config']
        color = colors[i % len(colors)]
        gens = data['generations']
        pop_size = config.get('pop_size', 100)
        label = f"Pop {pop_size}"
        
        plt.plot(gens, data['mean_mean'], label=label, color=color, linewidth=2)
        # ALWAYS show variance for mean fitness
        plt.fill_between(gens, data['mean_mean'] - data['mean_std'], 
                         data['mean_mean'] + data['mean_std'], alpha=0.3, color=color)
    plt.title(f"Population Size - Mean Fitness (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Mean Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 3: Population Size Comparison - Convergence
    plt.subplot(2, 3, 3)
    for i, name in enumerate(pop_configs):
        data = all_results[name]
        config = data['config']
        color = colors[i % len(colors)]
        gens = data['generations']
        pop_size = config.get('pop_size', 100)
        label = f"Pop {pop_size}"
        
        plt.plot(gens, data['percent_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['percent_mean'] - data['percent_std'], 
                             data['percent_mean'] + data['percent_std'], alpha=0.3, color=color)
    plt.title(f"Population Size - Convergence (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Percentage of Population")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 4: Crossover Analysis
    plt.subplot(2, 3, 4)
    crossover_configs = [name for name in all_results.keys() if 'Crossover' in name]
    color_map = {0.0: 'red', 0.2: 'orange', 0.4: 'yellow', 0.6: 'green', 0.8: 'blue', 1.0: 'purple'}
    for name in crossover_configs:
        data = all_results[name]
        config = data['config']
        p_c = config.get('p_c', 0.6)
        color = color_map.get(p_c, 'black')
        gens = data['generations']
        label = f"pc={p_c}"
        
        plt.plot(gens, data['best_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['best_mean'] - data['best_std'], 
                             data['best_mean'] + data['best_std'], alpha=0.3, color=color)
    plt.title(f"Crossover Analysis (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 5: Mutation Analysis
    plt.subplot(2, 3, 5)
    mutation_configs = [name for name in all_results.keys() if 'Mutation' in name]
    color_map = {0.01: 'blue', 0.05: 'green', 0.1: 'yellow', 0.3: 'red'}
    for name in mutation_configs:
        data = all_results[name]
        config = data['config']
        p_m = config.get('p_m', 0.1)
        color = color_map.get(p_m, 'black')
        gens = data['generations']
        label = f"pm={p_m}"
        
        plt.plot(gens, data['best_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['best_mean'] - data['best_std'], 
                             data['best_mean'] + data['best_std'], alpha=0.3, color=color)
    plt.title(f"Mutation Analysis (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 6: Selection Analysis (2, 4, 6, 8 tournament)
    plt.subplot(2, 3, 6)
    selection_configs = [name for name in all_results.keys() if any(str(k) + '-tournament' in name for k in [2, 4, 6, 8])]
    color_map = {2: 'red', 4: 'orange', 6: 'yellow', 8: 'green'}
    for name in selection_configs:
        data = all_results[name]
        config = data['config']
        k = config.get('k', 2)
        color = color_map.get(k, 'black')
        gens = data['generations']
        label = f"{k}-tournament"
        
        plt.plot(gens, data['best_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['best_mean'] - data['best_std'], 
                             data['best_mean'] + data['best_std'], alpha=0.3, color=color)
    plt.title(f"Selection Analysis (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def plot_program_length_analysis(all_results, show_variance=True):
    """Create focused plots for program length analysis with 6 subplots"""
    plt.figure(figsize=(20, 12))
    
    # Get the number of samples
    sample_count = next(iter(all_results.values()))['num_samples']

    # Plot 1: Program Length Comparison - Best Fitness
    plt.subplot(2, 3, 1)
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    prog_length_configs = [name for name in all_results.keys() if 'Length' in name]
    
    for i, name in enumerate(prog_length_configs):
        data = all_results[name]
        config = data['config']
        color = colors[i % len(colors)]
        gens = data['generations']
        prog_length = config.get('prog_length', 20)
        label = f"Length {prog_length}"
        
        plt.plot(gens, data['best_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['best_mean'] - data['best_std'], 
                             data['best_mean'] + data['best_std'], alpha=0.3, color=color)
    plt.title(f"Program Length - Best Fitness (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Program Length Comparison - Mean Fitness (ALWAYS show variance)
    plt.subplot(2, 3, 2)
    for i, name in enumerate(prog_length_configs):
        data = all_results[name]
        config = data['config']
        color = colors[i % len(colors)]
        gens = data['generations']
        prog_length = config.get('prog_length', 20)
        label = f"Length {prog_length}"
        
        plt.plot(gens, data['mean_mean'], label=label, color=color, linewidth=2)
        # ALWAYS show variance for mean fitness
        plt.fill_between(gens, data['mean_mean'] - data['mean_std'], 
                         data['mean_mean'] + data['mean_std'], alpha=0.3, color=color)
    plt.title(f"Program Length - Mean Fitness (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Mean Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 3: Program Length Comparison - Convergence
    plt.subplot(2, 3, 3)
    for i, name in enumerate(prog_length_configs):
        data = all_results[name]
        config = data['config']
        color = colors[i % len(colors)]
        gens = data['generations']
        prog_length = config.get('prog_length', 20)
        label = f"Length {prog_length}"
        
        plt.plot(gens, data['percent_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['percent_mean'] - data['percent_std'], 
                             data['percent_mean'] + data['percent_std'], alpha=0.3, color=color)
    plt.title(f"Program Length - Convergence (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Percentage of Population")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 4: Crossover Analysis
    plt.subplot(2, 3, 4)
    crossover_configs = [name for name in all_results.keys() if 'Crossover' in name]
    color_map = {0.0: 'red', 0.2: 'orange', 0.4: 'yellow', 0.6: 'green', 0.8: 'blue', 1.0: 'purple'}
    for name in crossover_configs:
        data = all_results[name]
        config = data['config']
        p_c = config.get('p_c', 0.6)
        color = color_map.get(p_c, 'black')
        gens = data['generations']
        label = f"pc={p_c}"
        
        plt.plot(gens, data['best_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['best_mean'] - data['best_std'], 
                             data['best_mean'] + data['best_std'], alpha=0.3, color=color)
    plt.title(f"Crossover Analysis (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 5: Mutation Analysis
    plt.subplot(2, 3, 5)
    mutation_configs = [name for name in all_results.keys() if 'Mutation' in name]
    color_map = {0.01: 'blue', 0.05: 'green', 0.1: 'yellow', 0.3: 'red'}
    for name in mutation_configs:
        data = all_results[name]
        config = data['config']
        p_m = config.get('p_m', 0.1)
        color = color_map.get(p_m, 'black')
        gens = data['generations']
        label = f"pm={p_m}"
        
        plt.plot(gens, data['best_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['best_mean'] - data['best_std'], 
                             data['best_mean'] + data['best_std'], alpha=0.3, color=color)
    plt.title(f"Mutation Analysis (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 6: Selection Analysis (2, 4, 6, 8 tournament)
    plt.subplot(2, 3, 6)
    selection_configs = [name for name in all_results.keys() if any(str(k) + '-tournament' in name for k in [2, 4, 6, 8])]
    color_map = {2: 'red', 4: 'orange', 6: 'yellow', 8: 'green'}
    for name in selection_configs:
        data = all_results[name]
        config = data['config']
        k = config.get('k', 2)
        color = color_map.get(k, 'black')
        gens = data['generations']
        label = f"{k}-tournament"
        
        plt.plot(gens, data['best_mean'], label=label, color=color, linewidth=2)
        if show_variance:
            plt.fill_between(gens, data['best_mean'] - data['best_std'], 
                             data['best_mean'] + data['best_std'], alpha=0.3, color=color)
    plt.title(f"Selection Analysis (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def plot_population_program_combinations(all_results):
    """Create a plot comparing combinations of population size and program length"""
    plt.figure(figsize=(20, 8))
    
    # Get the number of samples
    sample_count = next(iter(all_results.values()))['num_samples']
    
    # Define specific population sizes and program lengths to compare
    target_pop_sizes = [20, 50, 100, 150]
    target_prog_lengths = [10, 15, 20, 25]
    
    # Color map for better visualization
    colors = plt.cm.tab20(np.linspace(0, 1, 20))
    
    # Plot 1: Best Fitness Evolution for all combinations
    plt.subplot(1, 2, 1)
    
    line_count = 0
    for i, pop_size in enumerate(target_pop_sizes):
        for j, prog_length in enumerate(target_prog_lengths):
            # Look for configs that match both population size and program length
            matching_configs = [
                name for name, data in all_results.items() 
                if data['config'].get('pop_size') == pop_size 
                and data['config'].get('prog_length') == prog_length
                and 'tournament' not in name.lower() 
                and 'Crossover' not in name 
                and 'Mutation' not in name
                and 'Standard' not in name
            ]
            if matching_configs:
                config_name = matching_configs[0]
                data = all_results[config_name]
                gens = data['generations']
                color = colors[line_count % len(colors)]
                
                # Plot best fitness
                plt.plot(gens, data['best_mean'], color=color, linewidth=2, 
                        label=f'P={pop_size},L={prog_length}')
                line_count += 1
    
    plt.title(f"Best Fitness Evolution - Combinations (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Mean Fitness Evolution for all combinations
    plt.subplot(1, 2, 2)
    
    line_count = 0
    for i, pop_size in enumerate(target_pop_sizes):
        for j, prog_length in enumerate(target_prog_lengths):
            # Look for configs that match both population size and program length
            matching_configs = [
                name for name, data in all_results.items() 
                if data['config'].get('pop_size') == pop_size 
                and data['config'].get('prog_length') == prog_length
                and 'tournament' not in name.lower() 
                and 'Crossover' not in name 
                and 'Mutation' not in name
                and 'Standard' not in name
            ]
            if matching_configs:
                config_name = matching_configs[0]
                data = all_results[config_name]
                gens = data['generations']
                color = colors[line_count % len(colors)]
                
                # Plot mean fitness with variance (always shown)
                plt.plot(gens, data['mean_mean'], color=color, linewidth=2, 
                        label=f'P={pop_size},L={prog_length}')
                plt.fill_between(gens, data['mean_mean'] - data['mean_std'], 
                                data['mean_mean'] + data['mean_std'], alpha=0.3, color=color)
                line_count += 1
    
    plt.title(f"Mean Fitness Evolution - Combinations (mean over {sample_count} runs)")
    plt.xlabel("Generation")
    plt.ylabel("Mean Fitness")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Define comprehensive configurations including combinations
configurations = [
    # Standard configurations
    {"name": "Standard", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    
    # Population size variations
    {"name": "Population 10", "prog_length": 20, "pop_size": 10, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Population 20", "prog_length": 20, "pop_size": 20, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Population 40", "prog_length": 20, "pop_size": 40, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Population 50", "prog_length": 20, "pop_size": 50, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Population 80", "prog_length": 20, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Population 100", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Population 120", "prog_length": 20, "pop_size": 120, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Population 150", "prog_length": 20, "pop_size": 150, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Population 200", "prog_length": 20, "pop_size": 200, "k": 2, "p_c": 0.6, "p_m": 0.1},
    
    # Program length variations
    {"name": "Length 10", "prog_length": 10, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Length 12", "prog_length": 12, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Length 15", "prog_length": 15, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Length 20", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Length 25", "prog_length": 25, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Length 30", "prog_length": 30, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    
    # Specific combinations for the combination plot
    {"name": "Combination_P20_L10", "prog_length": 10, "pop_size": 20, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P20_L15", "prog_length": 15, "pop_size": 20, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P20_L20", "prog_length": 20, "pop_size": 20, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P20_L25", "prog_length": 25, "pop_size": 20, "k": 2, "p_c": 0.6, "p_m": 0.1},
    
    {"name": "Combination_P50_L10", "prog_length": 10, "pop_size": 50, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P50_L15", "prog_length": 15, "pop_size": 50, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P50_L20", "prog_length": 20, "pop_size": 50, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P50_L25", "prog_length": 25, "pop_size": 50, "k": 2, "p_c": 0.6, "p_m": 0.1},
    
    {"name": "Combination_P100_L10", "prog_length": 10, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P100_L15", "prog_length": 15, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P100_L20", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P100_L25", "prog_length": 25, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    
    {"name": "Combination_P150_L10", "prog_length": 10, "pop_size": 150, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P150_L15", "prog_length": 15, "pop_size": 150, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P150_L20", "prog_length": 20, "pop_size": 150, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P150_L25", "prog_length": 25, "pop_size": 150, "k": 2, "p_c": 0.6, "p_m": 0.1},
    
    # Selection variations (2, 4, 6, 8 tournament)
    {"name": "2-tournament", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "4-tournament", "prog_length": 20, "pop_size": 100, "k": 4, "p_c": 0.6, "p_m": 0.1},
    {"name": "6-tournament", "prog_length": 20, "pop_size": 100, "k": 6, "p_c": 0.6, "p_m": 0.1},
    {"name": "8-tournament", "prog_length": 20, "pop_size": 100, "k": 8, "p_c": 0.6, "p_m": 0.1},
    
    # Crossover probability variations
    {"name": "Crossover 0.0", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.0, "p_m": 0.1},
    {"name": "Crossover 0.2", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.2, "p_m": 0.1},
    {"name": "Crossover 0.4", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.4, "p_m": 0.1},
    {"name": "Crossover 0.6", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Crossover 0.8", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.8, "p_m": 0.1},
    {"name": "Crossover 1.0", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 1.0, "p_m": 0.1},
    
    # Mutation rate variations
    {"name": "Mutation 0.01", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.01},
    {"name": "Mutation 0.05", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.05},
    {"name": "Mutation 0.1", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Mutation 0.3", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.3},
]

# Run experiments with your chosen parameters
num_samples = 15   # ← CHANGE THIS TO YOUR DESIRED NUMBER OF SAMPLES
max_generations = 100  # ← CHANGE THIS TO YOUR DESIRED NUMBER OF GENERATIONS
show_variance = False   # ← SET TO False TO HIDE VARIANCE BANDS

# Run the experiments
all_results = run_experiments(configurations, num_samples, max_generations, show_variance)

# Create the three plots
plot_population_analysis(all_results, show_variance)
plot_program_length_analysis(all_results, show_variance)
plot_population_program_combinations(all_results)