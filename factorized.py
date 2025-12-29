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

def plot_metric_subplot(ax, all_results, config_names, metric_key, metric_std_key, title, ylabel, color_map=None, show_variance=True, always_show_variance=False, label_func=None):
    """Generic function to plot a metric subplot"""
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'pink', 'gray', 'olive']
    
    for i, name in enumerate(config_names):
        if name not in all_results:
            continue
        data = all_results[name]
        color = color_map.get(name, colors[i % len(colors)]) if color_map else colors[i % len(colors)]
        gens = data['generations']
        
        # Generate label
        if label_func:
            label = label_func(name, data)
        else:
            label = name
            
        ax.plot(gens, data[metric_key], label=label, color=color, linewidth=2)
        
        # Show variance if requested or if always_show_variance is True
        if show_variance or always_show_variance:
            ax.fill_between(gens, data[metric_key] - data[metric_std_key], 
                           data[metric_key] + data[metric_std_key], alpha=0.3, color=color)
    
    ax.set_title(title)
    ax.set_xlabel("Generation")
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True, alpha=0.3)

def get_config_value(config, key, default):
    """Helper to get configuration value"""
    return config.get(key, default)

def plot_single_analysis(all_results, show_variance=True, analysis_type="population"):
    """Create focused plots for different types of analysis with 2 subplots"""
    plt.figure(figsize=(15, 6))
    
    # Get the number of samples
    sample_count = next(iter(all_results.values()))['num_samples']

    # Define analysis-specific configurations
    if analysis_type == "population":
        config_filter = lambda name: 'Population' in name and 'tournament' not in name.lower()
        title_prefix = "Population Size"
        label_func = lambda name, data: f"Pop {get_config_value(data['config'], 'pop_size', 100)}"
        color_map = {}
    elif analysis_type == "program_length":
        config_filter = lambda name: 'Length' in name and 'tournament' not in name.lower() and 'Crossover' not in name and 'Mutation' not in name
        title_prefix = "Program Length"
        label_func = lambda name, data: f"Length {get_config_value(data['config'], 'prog_length', 20)}"
        color_map = {}
    elif analysis_type == "crossover":
        config_filter = lambda name: 'Crossover' in name
        title_prefix = "Crossover"
        label_func = lambda name, data: f"pc={get_config_value(data['config'], 'p_c', 0.6)}"
        color_map = {0.0: 'red', 0.2: 'orange', 0.4: 'yellow', 0.6: 'green', 0.8: 'blue', 1.0: 'purple'}
    elif analysis_type == "mutation":
        config_filter = lambda name: 'Mutation' in name
        title_prefix = "Mutation"
        label_func = lambda name, data: f"pm={get_config_value(data['config'], 'p_m', 0.1)}"
        color_map = {0.01: 'blue', 0.05: 'green', 0.1: 'yellow', 0.3: 'red'}
    elif analysis_type == "selection":
        config_filter = lambda name: any(str(k) + '-tournament' in name for k in [2, 4, 6, 8])
        title_prefix = "Selection"
        label_func = lambda name, data: f"{get_config_value(data['config'], 'k', 2)}-tournament"
        color_map = {2: 'red', 4: 'orange', 6: 'yellow', 8: 'green'}
    
    configs_to_plot = [name for name in all_results.keys() if config_filter(name)]
    
    # Plot 1: Best Fitness
    ax1 = plt.subplot(1, 2, 1)
    plot_metric_subplot(ax1, all_results, configs_to_plot, 'best_mean', 'best_std',
                       f"{title_prefix} - Best Fitness (mean over {sample_count} runs)",
                       "Best Fitness", color_map, show_variance, False, label_func)

    # Plot 2: Mean Fitness (ALWAYS show variance)
    ax2 = plt.subplot(1, 2, 2)
    plot_metric_subplot(ax2, all_results, configs_to_plot, 'mean_mean', 'mean_std',
                       f"{title_prefix} - Mean Fitness (mean over {sample_count} runs)",
                       "Mean Fitness", color_map, show_variance, True, label_func)

    plt.tight_layout()
    plt.show()

def plot_convergence_analysis(all_results, show_variance=True):
    """Create a separate plot for convergence analysis"""
    plt.figure(figsize=(15, 6))
    
    # Get the number of samples
    sample_count = next(iter(all_results.values()))['num_samples']
    
    # Define all analysis types for convergence comparison
    analysis_configs = [
        ("Population Size", lambda name: 'Population' in name and 'tournament' not in name.lower(), 
         lambda name, data: f"Pop {get_config_value(data['config'], 'pop_size', 100)}", {}),
        ("Program Length", lambda name: 'Length' in name and 'tournament' not in name.lower() and 'Crossover' not in name and 'Mutation' not in name,
         lambda name, data: f"Len {get_config_value(data['config'], 'prog_length', 20)}", {}),
        ("Crossover", lambda name: 'Crossover' in name,
         lambda name, data: f"pc={get_config_value(data['config'], 'p_c', 0.6)}", 
         {0.0: 'red', 0.2: 'orange', 0.4: 'yellow', 0.6: 'green', 0.8: 'blue', 1.0: 'purple'}),
        ("Mutation", lambda name: 'Mutation' in name,
         lambda name, data: f"pm={get_config_value(data['config'], 'p_m', 0.1)}", 
         {0.01: 'blue', 0.05: 'green', 0.1: 'yellow', 0.3: 'red'}),
        ("Selection", lambda name: any(str(k) + '-tournament' in name for k in [2, 4, 6, 8]),
         lambda name, data: f"{get_config_value(data['config'], 'k', 2)}-tournament", 
         {2: 'red', 4: 'orange', 6: 'yellow', 8: 'green'})
    ]
    
    # Plot 1: Convergence comparison - Best parameters from each category
    ax1 = plt.subplot(1, 2, 1)
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    for i, (title_prefix, config_filter, label_func, color_map) in enumerate(analysis_configs):
        configs_to_plot = [name for name in all_results.keys() if config_filter(name)]
        # Select representative configurations (either standard or best performing)
        if configs_to_plot:
            # For simplicity, plot the first few configurations
            selected_configs = configs_to_plot[:3] if len(configs_to_plot) > 3 else configs_to_plot
            for j, config_name in enumerate(selected_configs):
                if config_name in all_results:
                    data = all_results[config_name]
                    color = colors[i] if j == 0 else plt.cm.Set1(i * 0.1 + j * 0.3)
                    label = label_func(config_name, data)
                    ax1.plot(data['generations'], data['percent_mean'], 
                            label=f"{title_prefix}: {label}", color=color, linewidth=2)
                    if show_variance:
                        ax1.fill_between(data['generations'], 
                                       data['percent_mean'] - data['percent_std'], 
                                       data['percent_mean'] + data['percent_std'], 
                                       alpha=0.2, color=color)
    
    ax1.set_title(f"Convergence Analysis - Percentage Reaching Optimal Solution (mean over {sample_count} runs)")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Percentage of Population Reaching Optimal Solution")
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Detailed convergence for standard configuration compared to variations
    ax2 = plt.subplot(1, 2, 2)
    
    # Find standard configuration
    standard_config = None
    for name in all_results.keys():
        if name == "Standard":
            standard_config = name
            break
    
    if standard_config:
        data = all_results[standard_config]
        ax2.plot(data['generations'], data['percent_mean'], 
                label="Standard Configuration", color='black', linewidth=3)
        if show_variance:
            ax2.fill_between(data['generations'], 
                           data['percent_mean'] - data['percent_std'], 
                           data['percent_mean'] + data['percent_std'], 
                           alpha=0.3, color='black')
    
    # Plot convergence for key variations
    key_configs = [
        ("Population 100", lambda name: 'Population 100' in name),
        ("Length 20", lambda name: 'Length 20' in name and 'tournament' not in name.lower()),
        ("2-tournament", lambda name: '2-tournament' in name),
        ("Crossover 0.6", lambda name: 'Crossover 0.6' in name),
        ("Mutation 0.1", lambda name: 'Mutation 0.1' in name)
    ]
    
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    for i, (label, filter_func) in enumerate(key_configs):
        matching_configs = [name for name in all_results.keys() if filter_func(name)]
        if matching_configs:
            config_name = matching_configs[0]
            data = all_results[config_name]
            ax2.plot(data['generations'], data['percent_mean'], 
                    label=label, color=colors[i], linewidth=2)
            if show_variance:
                ax2.fill_between(data['generations'], 
                               data['percent_mean'] - data['percent_std'], 
                               data['percent_mean'] + data['percent_std'], 
                               alpha=0.3, color=colors[i])
    
    ax2.set_title(f"Convergence Comparison - Key Configurations (mean over {sample_count} runs)")
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Percentage of Population Reaching Optimal Solution")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_population_program_combinations(all_results):
    """Create a plot comparing combinations of population size and program length"""
    plt.figure(figsize=(20, 8))
    
    # Get the number of samples
    sample_count = next(iter(all_results.values()))['num_samples']
    
    # Define specific population sizes and program lengths to compare
    target_pop_sizes = [20, 50, 80, 100, 150]
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

    {"name": "Combination_P80_L10", "prog_length": 10, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P80_L15", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P80_L20", "prog_length": 20, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P80_L25", "prog_length": 25, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.1},
    
    {"name": "Combination_P100_L10", "prog_length": 10, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P100_L15", "prog_length": 15, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P100_L20", "prog_length": 20, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P100_L25", "prog_length": 25, "pop_size": 100, "k": 2, "p_c": 0.6, "p_m": 0.1},

    
    {"name": "Combination_P150_L10", "prog_length": 10, "pop_size": 150, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P150_L15", "prog_length": 15, "pop_size": 150, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P150_L20", "prog_length": 20, "pop_size": 150, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Combination_P150_L25", "prog_length": 25, "pop_size": 150, "k": 2, "p_c": 0.6, "p_m": 0.1},
    
    # Selection variations (2, 4, 6, 8 tournament)
    {"name": "2-tournament", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "4-tournament", "prog_length": 15, "pop_size": 80, "k": 4, "p_c": 0.6, "p_m": 0.1},
    {"name": "6-tournament", "prog_length": 15, "pop_size": 80, "k": 6, "p_c": 0.6, "p_m": 0.1},
    {"name": "8-tournament", "prog_length": 15, "pop_size": 80, "k": 8, "p_c": 0.6, "p_m": 0.1},
    
    # Crossover probability variations
    {"name": "Crossover 0.0", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.0, "p_m": 0.1},
    {"name": "Crossover 0.2", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.2, "p_m": 0.1},
    {"name": "Crossover 0.4", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.4, "p_m": 0.1},
    {"name": "Crossover 0.6", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Crossover 0.8", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.8, "p_m": 0.1},
    {"name": "Crossover 1.0", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 1.0, "p_m": 0.1},
    
    # Mutation rate variations
    {"name": "Mutation 0.01", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.01},
    {"name": "Mutation 0.05", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.05},
    {"name": "Mutation 0.1", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.1},
    {"name": "Mutation 0.3", "prog_length": 15, "pop_size": 80, "k": 2, "p_c": 0.6, "p_m": 0.3},
]

# Run experiments with your chosen parameters
num_samples = 1000   # ← CHANGE THIS TO YOUR DESIRED NUMBER OF SAMPLES
max_generations = 100  # ← CHANGE THIS TO YOUR DESIRED NUMBER OF GENERATIONS
show_variance = False   # ← SET TO False TO HIDE VARIANCE BANDS

# Run the experiments
all_results = run_experiments(configurations, num_samples, max_generations, show_variance)

# Create individual analysis plots
plot_single_analysis(all_results, show_variance, "population")
plot_single_analysis(all_results, show_variance, "program_length")
plot_single_analysis(all_results, show_variance, "crossover")
plot_single_analysis(all_results, show_variance, "mutation")
plot_single_analysis(all_results, show_variance, "selection")

# Create convergence analysis plot
plot_convergence_analysis(all_results, show_variance)

# Create combination plot
plot_population_program_combinations(all_results)
