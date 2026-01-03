import random
import matplotlib.pyplot as plt
import numpy as np
from joblib import delayed, Parallel
import json
import hashlib
import os

# Cache file path
CACHE_FILE = "experiment_cache.json"

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
def computeFitness(prog,cpu,dataSet):
    if execute(prog, cpu, dataSet[0]) == None:
        return -1
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

# Selection using tournament.
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

# LOOK-UP TABLE YOU HAVE TO REPRODUCE.
nbVar = 4
dataSet=[[0,0,0,0,0],[0,0,0,1,1],[0,0,1,0,0],[0,0,1,1,0],[0,1,0,0,0],[0,1,0,1,0],[0,1,1,0,0],[0,1,1,1,1],[1,0,0,0,0],[1,0,0,1,1],[1,0,1,0,0],[1,0,1,1,0],[1,1,0,0,0],[1,1,0,1,0],[1,1,1,0,0],[1,1,1,1,0]]
print("Original Dataset (Complex function):")
print(dataSet)

# New benchmark dataset: X1 AND X2 AND X3 AND X4
benchmarkDataSet = [[x1, x2, x3, x4, x1 and x2 and x3 and x4] 
                   for x1 in [0,1] for x2 in [0,1] for x3 in [0,1] for x4 in [0,1]]
print("\nBenchmark Dataset (X1 AND X2 AND X3 AND X4):")
print(benchmarkDataSet)

cpu=CPU()

# Function and terminal sets.
functionSet=["AND", "OR", "NOT", "XOR"]
terminalSet=["X1", "X2","X3", "X4"]

# Example of program.
progLength = 5
prog=randomProg(progLength,functionSet,terminalSet)
print("\nExample Program:")
print(prog)

# Execute a program on one row of the data set.
data = dataSet[0]
output=execute(prog,cpu,data)
print(f"\nExample Execution Result: {output}")
print("-------------")

def evaluate_population(gen: list, cpu: CPU, dataSet: list) -> tuple:
    """Evaluate population and return statistics"""
    fitness_list = np.array([computeFitness(i, cpu, dataSet) for i in gen])
    best_individual = gen[np.argmax(fitness_list)]
    valid_fitness_list = fitness_list[fitness_list != -1]
    if len(valid_fitness_list) == 0:
        valid_fitness_list = np.array([0])
    return (float(max(valid_fitness_list)), 
            float(np.mean(valid_fitness_list)), 
            float(np.std(valid_fitness_list)), 
            valid_fitness_list.tolist(),
            best_individual)

def ga(gen: list, cpu: CPU, dataSet: list, max_generations: int = 200, k: int = 2, p_c: float = 0.6, p_m: float = 0.1, verbose: bool = True) -> tuple:
    best = []
    mean = []
    std = []
    percent_max = []
    max_possible_fitness = len(dataSet)
    
    overall_best_fitness = -1
    overall_best_solution = None
    solution_found_generation = None
    
    for generation in range(max_generations):
        best_fit, mean_fit, std_fit, fitness_list, best_individual = evaluate_population(gen, cpu, dataSet)
        best.append(best_fit)
        mean.append(mean_fit)
        std.append(std_fit)
        
        if best_fit > overall_best_fitness:
            overall_best_fitness = best_fit
            if isinstance(best_individual, list):
                overall_best_solution = [str(item) for item in best_individual]
            else:
                overall_best_solution = best_individual
            
        if best_fit == max_possible_fitness and solution_found_generation is None:
            solution_found_generation = generation
        
        count_max = sum(1 for f in fitness_list if f == max_possible_fitness)
        percent_max.append((count_max / len(gen)) * 100)
        
        gen = selection(gen, cpu, dataSet, k=k)
        gen = crossover(gen, p_c)
        gen = mutation(gen, p_m, terminalSet, functionSet)
    
    clean_solution = None
    if overall_best_solution is not None:
        if isinstance(overall_best_solution, list):
            clean_solution = [str(item) for item in overall_best_solution]
        else:
            clean_solution = str(overall_best_solution)
    
    return best, mean, std, percent_max, solution_found_generation, overall_best_solution, overall_best_fitness

# =============================================================================
# CACHE MANAGEMENT SYSTEM
# =============================================================================

def get_experiment_hash(config, num_samples):
    """Generate a unique hash for an experiment based on its parameters"""
    # Create a dictionary with all relevant parameters
    params = {
        'prog_length': config.get('prog_length', DEFAULT_CONFIG['prog_length']),
        'pop_size': config.get('pop_size', DEFAULT_CONFIG['pop_size']),
        'k': config.get('k', DEFAULT_CONFIG['k']),
        'p_c': config.get('p_c', DEFAULT_CONFIG['p_c']),
        'p_m': config.get('p_m', DEFAULT_CONFIG['p_m']),
        'max_generations': config.get('max_generations', DEFAULT_CONFIG['max_generations']),
        'dataset_id': 'benchmark' if config.get('dataset', DEFAULT_CONFIG['dataset']) is benchmarkDataSet else 'original',
        'num_samples': num_samples  # Include number of samples in the hash
    }
    
    # Convert to JSON string and generate hash
    params_str = json.dumps(params, sort_keys=True)
    return hashlib.md5(params_str.encode()).hexdigest()

def load_cache():
    """Load experiment cache from file"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_cache(cache):
    """Save experiment cache to file"""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save cache file: {e}")

def check_cached_result(config, num_samples):
    """Check if an experiment result is already in the cache"""
    cache = load_cache()
    exp_hash = get_experiment_hash(config, num_samples)
    return cache.get(exp_hash), exp_hash

def cache_result(config, num_samples, results):
    """Cache the results of an experiment"""
    cache = load_cache()
    exp_hash = get_experiment_hash(config, num_samples)
    
    # Prepare results for caching (convert numpy arrays to lists)
    cached_results = {
        'config': config,
        'num_samples': num_samples,
        'results': {
            'all_results': {},
            'convergence_stats': results[1].get(config['name'], {}),
            'best_solutions': results[2].get(config['name'], {})
        }
    }
    
    # Convert numpy arrays to lists for JSON serialization
    all_results_data = results[0].get(config['name'], {})
    for key in ['best_mean', 'best_std', 'mean_mean', 'mean_std', 'percent_mean', 'percent_std']:
        if key in all_results_data:
            if isinstance(all_results_data[key], np.ndarray):
                cached_results['results']['all_results'][key] = all_results_data[key].tolist()
            else:
                cached_results['results']['all_results'][key] = all_results_data[key]
    
    if 'generations' in all_results_data:
        cached_results['results']['all_results']['generations'] = all_results_data['generations'].tolist()
    
    cache[exp_hash] = cached_results
    save_cache(cache)
    return exp_hash

def get_config_value(config, key, default):
    """Helper to get configuration value"""
    return config.get(key, default)

def plot_detailed_analysis(all_results, convergence_stats, show_variance=True, analysis_type="population"):
    """Create detailed plots with 4 subplots for each analysis type"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    sample_count = next(iter(all_results.values()))['num_samples']

    # Define analysis configurations
    analysis_configs = {
        "population": {
            "filter": lambda name: 'Population' in name and 'tournament' not in name.lower() and 'Benchmark' not in name,
            "title": "Population Size",
            "label": lambda name, data: f"Pop {get_config_value(data['config'], 'pop_size', DEFAULT_CONFIG['pop_size'])}"
        },
        "program_length": {
            "filter": lambda name: 'Length' in name and 'tournament' not in name.lower() and 'Crossover' not in name and 'Mutation' not in name and 'Benchmark' not in name,
            "title": "Program Length",
            "label": lambda name, data: f"Length {get_config_value(data['config'], 'prog_length', DEFAULT_CONFIG['prog_length'])}"
        },
        "crossover": {
            "filter": lambda name: 'Crossover ' in name and 'Benchmark' not in name,
            "title": "Crossover",
            "label": lambda name, data: f"pc={get_config_value(data['config'], 'p_c', DEFAULT_CONFIG['p_c'])}"
        },
        "mutation": {
            "filter": lambda name: 'Mutation ' in name and 'Benchmark' not in name,
            "title": "Mutation",
            "label": lambda name, data: f"pm={get_config_value(data['config'], 'p_m', DEFAULT_CONFIG['p_m'])}"
        },
        "selection": {
            "filter": lambda name: any(str(k) + '-tournament' in name for k in TOURNAMENT_SIZES) and 'Benchmark' not in name,
            "title": "Selection",
            "label": lambda name, data: f"{get_config_value(data['config'], 'k', DEFAULT_CONFIG['k'])}-tournament"
        },
        "iterations": {
            "filter": lambda name: 'Iterations' in name and 'Benchmark' not in name,
            "title": "Iterations",
            "label": lambda name, data: f"MaxGens {get_config_value(data['config'], 'max_generations', max_generations)}"
        },
        "benchmark": {
            "filter": lambda name: 'Benchmark' in name,
            "title": "Benchmark Comparison",
            "label": lambda name, data: name.replace('Benchmark ', '')
        }
    }
    
    config_info = analysis_configs[analysis_type]
    configs_to_plot = [name for name in all_results.keys() if config_info["filter"](name)]
    
    # Filter convergence stats for relevant configurations only
    relevant_convergence_stats = {name: convergence_stats[name] for name in configs_to_plot if name in convergence_stats}
    
    # Sort configs by their parameter value for better visualization
    if analysis_type == "population":
        configs_to_plot.sort(key=lambda x: get_config_value(all_results[x]['config'], 'pop_size', 0))
    elif analysis_type == "program_length":
        configs_to_plot.sort(key=lambda x: get_config_value(all_results[x]['config'], 'prog_length', 0))
    elif analysis_type == "crossover":
        configs_to_plot.sort(key=lambda x: get_config_value(all_results[x]['config'], 'p_c', 0))
    elif analysis_type == "mutation":
        configs_to_plot.sort(key=lambda x: get_config_value(all_results[x]['config'], 'p_m', 0))
    elif analysis_type == "selection":
        configs_to_plot.sort(key=lambda x: get_config_value(all_results[x]['config'], 'k', 0))
    elif analysis_type == "iterations":
        configs_to_plot.sort(key=lambda x: get_config_value(all_results[x]['config'], 'max_generations', 0))
    
    # Plot 1: Best Fitness Evolution
    for name in configs_to_plot:
        if name not in all_results:
            continue
        data = all_results[name]
        gens = data['generations']
        label = config_info["label"](name, data)
            
        line, = ax1.plot(gens, data['best_mean'], label=label, linewidth=2)
        color = line.get_color()
        
        if show_variance:
            ax1.fill_between(gens, data['best_mean'] - data['best_std'], 
                           data['best_mean'] + data['best_std'], alpha=0.3, color=color)
    
    ax1.set_title(f"{config_info['title']} - Best Fitness Evolution (mean over {sample_count} runs)")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Best Fitness")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Mean Fitness Evolution
    for name in configs_to_plot:
        if name not in all_results:
            continue
        data = all_results[name]
        gens = data['generations']
        label = config_info["label"](name, data)
            
        line, = ax2.plot(gens, data['mean_mean'], label=label, linewidth=2)
        color = line.get_color()
        
        if show_variance:
            ax2.fill_between(gens, data['mean_mean'] - data['mean_std'], 
                           data['mean_mean'] + data['mean_std'], alpha=0.3, color=color)
    
    ax2.set_title(f"{config_info['title']} - Mean Fitness Evolution (mean over {sample_count} runs)")
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Mean Fitness")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Plot 3: Success Rate by Configuration
    if relevant_convergence_stats:
        config_names = list(relevant_convergence_stats.keys())
        success_rates = [relevant_convergence_stats[name]['success_rate'] for name in config_names]
        
        # Sort by parameter value
        if analysis_type == "population":
            sorted_data = sorted(zip(config_names, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'pop_size', 0))
        elif analysis_type == "program_length":
            sorted_data = sorted(zip(config_names, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'prog_length', 0))
        elif analysis_type == "crossover":
            sorted_data = sorted(zip(config_names, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'p_c', 0))
        elif analysis_type == "mutation":
            sorted_data = sorted(zip(config_names, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'p_m', 0))
        elif analysis_type == "selection":
            sorted_data = sorted(zip(config_names, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'k', 0))
        elif analysis_type == "iterations":
            sorted_data = sorted(zip(config_names, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'max_generations', 0))
        elif analysis_type == "benchmark":
            sorted_data = list(zip(config_names, success_rates))
        
        sorted_configs, sorted_rates = zip(*sorted_data) if sorted_data else ([], [])
        labels = [config_info["label"](name, all_results[name]) for name in sorted_configs]
        
        bars = ax3.bar(range(len(sorted_configs)), sorted_rates, color='green', alpha=0.7)
        ax3.set_xlabel('Configuration')
        ax3.set_ylabel('Success Rate (%)')
        ax3.set_title(f'{config_info["title"]} - Success Rate by Configuration')
        ax3.set_xticks(range(len(sorted_configs)))
        ax3.set_xticklabels(labels, rotation=45, ha='right')
        
        # Add value labels on bars
        for i, (bar, rate) in enumerate(zip(bars, sorted_rates)):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{rate:.1f}%', ha='center', va='bottom', fontsize=8)
    
    # Plot 4: Average Generations to Solution
    if relevant_convergence_stats:
        config_names = list(relevant_convergence_stats.keys())
        avg_gens = [relevant_convergence_stats[name]['avg_generations'] for name in config_names]
        success_rates = [relevant_convergence_stats[name]['success_rate'] for name in config_names]
        
        # Sort by parameter value
        if analysis_type == "population":
            sorted_data = sorted(zip(config_names, avg_gens, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'pop_size', 0))
        elif analysis_type == "program_length":
            sorted_data = sorted(zip(config_names, avg_gens, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'prog_length', 0))
        elif analysis_type == "crossover":
            sorted_data = sorted(zip(config_names, avg_gens, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'p_c', 0))
        elif analysis_type == "mutation":
            sorted_data = sorted(zip(config_names, avg_gens, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'p_m', 0))
        elif analysis_type == "selection":
            sorted_data = sorted(zip(config_names, avg_gens, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'k', 0))
        elif analysis_type == "iterations":
            sorted_data = sorted(zip(config_names, avg_gens, success_rates), 
                               key=lambda x: get_config_value(all_results[x[0]]['config'], 'max_generations', 0))
        elif analysis_type == "benchmark":
            sorted_data = list(zip(config_names, avg_gens, success_rates))
        
        sorted_configs, sorted_gens, sorted_rates = zip(*sorted_data) if sorted_data else ([], [], [])
        labels = [config_info["label"](name, all_results[name]) for name in sorted_configs]
        
        # Only show configs that had successful runs
        successful_indices = [i for i, rate in enumerate(sorted_rates) if rate > 0]
        if successful_indices:
            successful_configs = [sorted_configs[i] for i in successful_indices]
            successful_gens = [sorted_gens[i] for i in successful_indices]
            successful_labels = [labels[i] for i in successful_indices]
            
            bars = ax4.bar(range(len(successful_configs)), successful_gens, color='blue', alpha=0.7)
            ax4.set_xlabel('Configuration')
            ax4.set_ylabel('Average Generations to Solution')
            ax4.set_title(f'{config_info["title"]} - Average Generations (Successful Runs)')
            ax4.set_xticks(range(len(successful_configs)))
            ax4.set_xticklabels(successful_labels, rotation=45, ha='right')
            
            # Add value labels on bars
            for i, (bar, gen) in enumerate(zip(bars, successful_gens)):
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                        f'{gen:.1f}', ha='center', va='bottom', fontsize=8)
        else:
            ax4.text(0.5, 0.5, 'No successful runs', ha='center', va='center', 
                    transform=ax4.transAxes, fontsize=12)
            ax4.set_title(f'{config_info['title']} - Average Generations (Successful Runs)')
    
    plt.tight_layout()
    plt.show()

def plot_program_length_pop_size_combination(all_results, convergence_stats):
    """Plot ALL combinations of population size and program length"""
    fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(20, 8))
    sample_count = next(iter(all_results.values()))['num_samples']
    
    # Filter configs for combination experiments - now includes ALL combinations
    configs = [
        name for name, data in convergence_stats.items() 
        if ('Combination' in name or 'Population' in name or 'Length' in name) and 
            '_P' in name and 
            '_L' in name and
            'Benchmark' not in name  # Exclude benchmark for this plot
    ]
    
    # Get ALL unique population_size and program_length values
    pop_size_values = sorted(list(set(
        convergence_stats[name]['config'].get('pop_size', DEFAULT_CONFIG['pop_size']) 
        for name in configs
    )))
    
    program_length_values = sorted(list(set(
        convergence_stats[name]['config'].get('prog_length', DEFAULT_CONFIG['prog_length']) 
        for name in configs
    )))
    
    # Create heatmap data
    success_rates = np.zeros((len(pop_size_values), len(program_length_values)))
    avg_generations = np.zeros((len(pop_size_values), len(program_length_values)))
    
    # Initialize with NaN for missing combinations
    success_rates.fill(np.nan)
    avg_generations.fill(np.nan)
    
    # Fill heatmap data
    for name in configs:
        config = convergence_stats[name]['config']
        ps = config.get('pop_size', DEFAULT_CONFIG['pop_size'])
        pl = config.get('prog_length', DEFAULT_CONFIG['prog_length'])
        
        i = pop_size_values.index(ps)
        j = program_length_values.index(pl)
        
        success_rates[i, j] = convergence_stats[name]['success_rate']
        avg_generations[i, j] = convergence_stats[name]['avg_generations']
    
    # Plot 1: Success Rate Heatmap
    im1 = ax1.imshow(success_rates, cmap='viridis', aspect='auto')
    ax1.set_title(f'Success Rate (%) - ALL Combinations (mean over {sample_count} runs)')
    ax1.set_xlabel('Program Length')
    ax1.set_ylabel('Population Size')
    ax1.set_xticks(range(len(program_length_values)))
    ax1.set_xticklabels([f'{pl}' for pl in program_length_values])
    ax1.set_yticks(range(len(pop_size_values)))
    ax1.set_yticklabels([f'{ps}' for ps in pop_size_values])
    
    # Add text annotations
    for i in range(len(pop_size_values)):
        for j in range(len(program_length_values)):
            if not np.isnan(success_rates[i, j]):
                text = ax1.text(j, i, f'{success_rates[i, j]:.1f}%',
                               ha="center", va="center", color="w" if success_rates[i, j] > 50 else "black")
    
    plt.colorbar(im1, ax=ax1)
    
    # Plot 2: Average Generations Heatmap
    im2 = ax2.imshow(avg_generations, cmap='plasma', aspect='auto')
    ax2.set_title(f'Average Generations - ALL Combinations (mean over {sample_count} runs)')
    ax2.set_xlabel('Program Length')
    ax2.set_ylabel('Population Size')
    ax2.set_xticks(range(len(program_length_values)))
    ax2.set_xticklabels([f'{pl}' for pl in program_length_values])
    ax2.set_yticks(range(len(pop_size_values)))
    ax2.set_yticklabels([f'{ps}' for ps in pop_size_values])
    
    # Add text annotations
    for i in range(len(pop_size_values)):
        for j in range(len(program_length_values)):
            if not np.isnan(avg_generations[i, j]):
                text = ax2.text(j, i, f'{avg_generations[i, j]:.1f}',
                               ha="center", va="center", color="w" if avg_generations[i, j] < 100 else "black")
    
    plt.colorbar(im2, ax=ax2)
    
    plt.tight_layout()
    plt.show()

def plot_crossover_mutation_combinations(all_results, convergence_stats):
    """Plot ALL combinations of crossover and mutation rates"""
    fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(20, 8))
    sample_count = next(iter(all_results.values()))['num_samples']

    # Filter configs for crossover-mutation combinations - now includes ALL combinations
    configs_cx_mut = [
        name for name, data in convergence_stats.items() 
        if ('Crossover_' in name and 'Mutation_' in name) or
           ('Crossover ' in name and 'Mutation ' in name) and
           'Benchmark' not in name  # Exclude benchmark for this plot
    ]
    
    # Get ALL unique crossover and mutation values
    crossover_values = sorted(list(set(
        convergence_stats[name]['config'].get('p_c', DEFAULT_CONFIG['p_c']) 
        for name in configs_cx_mut
    )))
    
    mutation_values = sorted(list(set(
        convergence_stats[name]['config'].get('p_m', DEFAULT_CONFIG['p_m']) 
        for name in configs_cx_mut
    )))
    
    # Create heatmap data
    success_rates = np.zeros((len(crossover_values), len(mutation_values)))
    avg_generations = np.zeros((len(crossover_values), len(mutation_values)))
    
    # Initialize with NaN for missing combinations
    success_rates.fill(np.nan)
    avg_generations.fill(np.nan)
    
    # Fill heatmap data
    for name in configs_cx_mut:
        config = convergence_stats[name]['config']
        pc = config.get('p_c', DEFAULT_CONFIG['p_c'])
        pm = config.get('p_m', DEFAULT_CONFIG['p_m'])
        
        i = crossover_values.index(pc)
        j = mutation_values.index(pm)
        
        success_rates[i, j] = convergence_stats[name]['success_rate']
        avg_generations[i, j] = convergence_stats[name]['avg_generations']
    
    # Plot 1: Success Rate Heatmap
    im1 = ax1.imshow(success_rates, cmap='viridis', aspect='auto')
    ax1.set_title(f'Success Rate (%) - ALL Combinations (mean over {sample_count} runs)')
    ax1.set_xlabel('Mutation Rate')
    ax1.set_ylabel('Crossover Rate')
    ax1.set_xticks(range(len(mutation_values)))
    ax1.set_xticklabels([f'{pm}' for pm in mutation_values])
    ax1.set_yticks(range(len(crossover_values)))
    ax1.set_yticklabels([f'{pc}' for pc in crossover_values])
    
    # Add text annotations
    for i in range(len(crossover_values)):
        for j in range(len(mutation_values)):
            if not np.isnan(success_rates[i, j]):
                text = ax1.text(j, i, f'{success_rates[i, j]:.1f}%',
                               ha="center", va="center", color="w" if success_rates[i, j] > 50 else "black")
    
    plt.colorbar(im1, ax=ax1)
    
    # Plot 2: Average Generations Heatmap
    im2 = ax2.imshow(avg_generations, cmap='plasma', aspect='auto')
    ax2.set_title(f'Average Generations - ALL Combinations (mean over {sample_count} runs)')
    ax2.set_xlabel('Mutation Rate')
    ax2.set_ylabel('Crossover Rate')
    ax2.set_xticks(range(len(mutation_values)))
    ax2.set_xticklabels([f'{pm}' for pm in mutation_values])
    ax2.set_yticks(range(len(crossover_values)))
    ax2.set_yticklabels([f'{pc}' for pc in crossover_values])
    
    # Add text annotations
    for i in range(len(crossover_values)):
        for j in range(len(mutation_values)):
            if not np.isnan(avg_generations[i, j]):
                text = ax2.text(j, i, f'{avg_generations[i, j]:.1f}',
                               ha="center", va="center", color="w" if avg_generations[i, j] < 100 else "black")
    
    plt.colorbar(im2, ax=ax2)
    
    plt.tight_layout()
    plt.show()

# =============================================================================
# OPTIMIZED CONFIGURATION MANAGEMENT (WITH ALL COMBINATIONS)
# =============================================================================

# Default parameter values
DEFAULT_CONFIG = {
    'prog_length': 20,
    'pop_size': 100,
    'k': 2,
    'p_c': 0.6,
    'p_m': 0.1,
    'max_generations': 200,
    'dataset': dataSet
}

# Parameter ranges for experiments
POP_SIZES = [20, 50, 80, 100, 150]
PROG_LENGTHS = [8, 10, 15, 20, 30]
CROSSOVER_RATES = [0.0, 0.2, 0.4, 0.6, 0.8]
MUTATION_RATES = [0.0, 0.05, 0.1, 0.2, 0.3]
TOURNAMENT_SIZES = [2, 4, 6, 8, 10]
ITERATIONS = [20, 50, 100, 150, 200]

# Cache to track which configurations have been run
config_cache = set()

def get_config_signature(config):
    """Generate a unique signature for a configuration to avoid duplicates"""
    signature_items = {
        'prog_length': config.get('prog_length', DEFAULT_CONFIG['prog_length']),
        'pop_size': config.get('pop_size', DEFAULT_CONFIG['pop_size']),
        'k': config.get('k', DEFAULT_CONFIG['k']),
        'p_c': config.get('p_c', DEFAULT_CONFIG['p_c']),
        'p_m': config.get('p_m', DEFAULT_CONFIG['p_m']),
        'max_generations': config.get('max_generations', DEFAULT_CONFIG['max_generations']),
        'dataset_id': 'benchmark' if config.get('dataset', DEFAULT_CONFIG['dataset']) is benchmarkDataSet else 'original'
    }
    return frozenset(signature_items.items())

def create_configurations():
    """Create unique configurations without duplicates, but with ALL combinations"""
    configurations = []
    config_cache.clear()
    
    # Standard configuration
    standard_config = DEFAULT_CONFIG.copy()
    standard_config['name'] = "Standard"
    sig = get_config_signature(standard_config)
    if sig not in config_cache:
        config_cache.add(sig)
        configurations.append(standard_config)
    
    # Single parameter variations (avoid combinations that are same as DEFAULT_CONFIG)
    
    # Population size variations
    for pop_size in POP_SIZES:
        config = DEFAULT_CONFIG.copy()
        config.update({"name": f"Population {pop_size}", "pop_size": pop_size})
        sig = get_config_signature(config)
        if sig not in config_cache:
            config_cache.add(sig)
            configurations.append(config)
    
    # Program length variations
    for prog_length in PROG_LENGTHS:
        config = DEFAULT_CONFIG.copy()
        config.update({"name": f"Length {prog_length}", "prog_length": prog_length})
        sig = get_config_signature(config)
        if sig not in config_cache:
            config_cache.add(sig)
            configurations.append(config)
    
    # Population-Program length combinations (ALL COMBINATIONS)
    for pop_size in POP_SIZES:
        for prog_length in PROG_LENGTHS:
            config = DEFAULT_CONFIG.copy()
            config.update({
                "name": f"Combination_P{pop_size}_L{prog_length}", 
                "pop_size": pop_size, 
                "prog_length": prog_length
            })
            sig = get_config_signature(config)
            if sig not in config_cache:
                config_cache.add(sig)
                configurations.append(config)
    
    # Selection variations
    for k in TOURNAMENT_SIZES:
        config = DEFAULT_CONFIG.copy()
        config.update({"name": f"{k}-tournament", "k": k})
        sig = get_config_signature(config)
        if sig not in config_cache:
            config_cache.add(sig)
            configurations.append(config)
    
    # Crossover variations
    for p_c in CROSSOVER_RATES:
        config = DEFAULT_CONFIG.copy()
        config.update({"name": f"Crossover {p_c}", "p_c": p_c})
        sig = get_config_signature(config)
        if sig not in config_cache:
            config_cache.add(sig)
            configurations.append(config)
    
    # Mutation variations
    for p_m in MUTATION_RATES:
        config = DEFAULT_CONFIG.copy()
        config.update({"name": f"Mutation {p_m}", "p_m": p_m})
        sig = get_config_signature(config)
        if sig not in config_cache:
            config_cache.add(sig)
            configurations.append(config)
    
    # Crossover-Mutation combinations (ALL COMBINATIONS)
    for p_c in CROSSOVER_RATES:
        for p_m in MUTATION_RATES:    
            config = DEFAULT_CONFIG.copy()
            config.update({
                "name": f"Crossover_{p_c}_Mutation_{p_m}", 
                "p_c": p_c, 
                "p_m": p_m
            })
            sig = get_config_signature(config)
            if sig not in config_cache:
                config_cache.add(sig)
                configurations.append(config)
    
    # Iteration count variations
    for max_gens in ITERATIONS:
        config = DEFAULT_CONFIG.copy()
        config.update({"name": f"Iterations {max_gens}", "max_generations": max_gens})
        sig = get_config_signature(config)
        if sig not in config_cache:
            config_cache.add(sig)
            configurations.append(config)
    
    # Benchmark tests - only add if they're different from regular configurations
    benchmark_config = DEFAULT_CONFIG.copy()
    benchmark_config.update({"dataset": benchmarkDataSet})
    
    # Only add benchmark if it's different from standard
    benchmark_sig = get_config_signature(benchmark_config)
    if benchmark_sig not in config_cache:
        config_cache.add(benchmark_sig)
        benchmark_config['name'] = "Benchmark Standard"
        configurations.append(benchmark_config)
    
    # Benchmark variations that are meaningfully different (ALL COMBINATIONS)
    benchmark_variations = [
        {"name": "Benchmark Population 50", "pop_size": 50},
        {"name": "Benchmark Population 150", "pop_size": 150},
        {"name": "Benchmark Length 12", "prog_length": 12},
        {"name": "Benchmark Length 25", "prog_length": 25},
        {"name": "Benchmark 4-tournament", "k": 4},
        {"name": "Benchmark 8-tournament", "k": 8},
        {"name": "Benchmark Crossover 0.4", "p_c": 0.4},
        {"name": "Benchmark Crossover 0.8", "p_c": 0.8},
        {"name": "Benchmark Mutation 0.05", "p_m": 0.05},
        {"name": "Benchmark Mutation 0.2", "p_m": 0.2},
        {"name": "Benchmark Iterations 50", "max_generations": 50},
        {"name": "Benchmark Iterations 150", "max_generations": 150},
    ]
    
    for variation in benchmark_variations:
        config = benchmark_config.copy()
        config.update(variation)
        sig = get_config_signature(config)
        if sig not in config_cache:
            config_cache.add(sig)
            configurations.append(config)
    
    # Add benchmark combinations (ALL COMBINATIONS)
    for pop_size in POP_SIZES:
        for prog_length in PROG_LENGTHS:
            config = benchmark_config.copy()
            config.update({
                "name": f"Benchmark Combination_P{pop_size}_L{prog_length}", 
                "pop_size": pop_size, 
                "prog_length": prog_length
            })
            sig = get_config_signature(config)
            if sig not in config_cache:
                config_cache.add(sig)
                configurations.append(config)
    
    for p_c in CROSSOVER_RATES:
        for p_m in MUTATION_RATES:   
            config = benchmark_config.copy()
            config.update({
                "name": f"Benchmark Crossover_{p_c}_Mutation_{p_m}", 
                "p_c": p_c, 
                "p_m": p_m
            })
            sig = get_config_signature(config)
            if sig not in config_cache:
                config_cache.add(sig)
                configurations.append(config)
    
    print(f"Created {len(configurations)} unique configurations (all combinations, avoided duplicates)")
    return configurations

# =============================================================================
# OPTIMIZED EXPERIMENT EXECUTION WITH CACHING
# =============================================================================

def run_single_experiment(sample_index, prog_length, pop_size, k, p_c, p_m, max_generations, dataSet, functionSet, terminalSet):
    """Run a single experiment with memoization for identical configurations"""
    # Create a signature for this specific run to potentially cache results
    run_signature = (prog_length, pop_size, k, p_c, p_m, max_generations, 
                    tuple(tuple(row) for row in dataSet))  # Convert dataset to tuple for hashing
    
    # In a more advanced version, you could cache results here
    # For now, we'll just run the experiment
    population = [randomProg(prog_length, functionSet, terminalSet) for _ in range(pop_size)]
    result = ga(population, CPU(), dataSet, max_generations, k, p_c, p_m, verbose=False)
    return result

def run_experiments(configurations, num_samples=100, max_generations=100, show_variance=True):
    """Run experiments with configurable number of samples - OPTIMIZED VERSION WITH CACHING"""
    all_results = {}
    convergence_stats = {}
    best_solutions = {}

    print(f"Running {len(configurations)} unique configurations with {num_samples} samples each")
    
    for config in configurations:
        config_name = config['name']
        
        # Check if this experiment is already cached
        cached_result, exp_hash = check_cached_result(config, num_samples)
        
        if cached_result:
            print(f"Loading cached results for {config_name} (hash: {exp_hash[:8]}...)")
            # Load results from cache
            cached_all_results = cached_result['results']['all_results']
            cached_convergence_stats = cached_result['results']['convergence_stats']
            cached_best_solutions = cached_result['results']['best_solutions']
            
            # Convert lists back to numpy arrays
            for key in ['best_mean', 'best_std', 'mean_mean', 'mean_std', 'percent_mean', 'percent_std']:
                if key in cached_all_results:
                    cached_all_results[key] = np.array(cached_all_results[key])
            
            if 'generations' in cached_all_results:
                cached_all_results['generations'] = np.array(cached_all_results['generations'])
            
            all_results[config_name] = cached_all_results
            convergence_stats[config_name] = cached_convergence_stats
            best_solutions[config_name] = cached_best_solutions
            continue
        
        print(f"Running {config_name}... (not found in cache)")
        
        prog_length = config.get('prog_length', DEFAULT_CONFIG['prog_length'])
        pop_size = config.get('pop_size', DEFAULT_CONFIG['pop_size'])
        k = config.get('k', DEFAULT_CONFIG['k'])
        p_c = config.get('p_c', DEFAULT_CONFIG['p_c'])
        p_m = config.get('p_m', DEFAULT_CONFIG['p_m'])
        max_gens = config.get('max_generations', max_generations)
        dataset_to_use = config.get('dataset', DEFAULT_CONFIG['dataset'])
        
        # Use parallel processing for samples
        results = Parallel(n_jobs=-1)(
            delayed(run_single_experiment)(sample, prog_length, pop_size, k, p_c, p_m, max_gens, 
                                         dataset_to_use, functionSet, terminalSet)
            for sample in range(num_samples)
        )
        
        # Process results (same as before)
        generations_to_solution = []
        success_count = 0
        all_best_solutions = []
        
        for result in results:
            solution_gen = result[4]
            best_solution = result[5]
            best_fitness = result[6]
            
            if solution_gen is not None:
                generations_to_solution.append(solution_gen)
                success_count += 1
                
            all_best_solutions.append((best_solution, best_fitness))
        
        best_results = np.array([r[0] for r in results])
        mean_results = np.array([r[1] for r in results])
        std_results = np.array([r[2] for r in results])
        percent_results = np.array([r[3] for r in results])
        
        all_results_config = {
            'best_mean': np.mean(best_results, axis=0),
            'best_std': np.std(best_results, axis=0),
            'mean_mean': np.mean(mean_results, axis=0),
            'mean_std': np.std(mean_results, axis=0),
            'percent_mean': np.mean(percent_results, axis=0),
            'percent_std': np.std(percent_results, axis=0),
            'generations': np.arange(len(best_results[0])),
            'config': config,
            'num_samples': num_samples
        }
        
        convergence_stats_config = {
            'success_rate': (success_count / num_samples) * 100,
            'avg_generations': np.mean(generations_to_solution) if generations_to_solution else max_gens,
            'std_generations': np.std(generations_to_solution) if generations_to_solution else 0,
            'median_generations': np.median(generations_to_solution) if generations_to_solution else max_gens,
            'min_generations': min(generations_to_solution) if generations_to_solution else max_gens,
            'max_generations': max(generations_to_solution) if generations_to_solution else max_gens,
            'total_successes': success_count,
            'config': config
        }
        
        best_solutions_config = {
            'solutions': all_best_solutions,
            'best_ever': max(all_best_solutions, key=lambda x: x[1]) if all_best_solutions else None,
            'config': config
        }
        
        all_results[config_name] = all_results_config
        convergence_stats[config_name] = convergence_stats_config
        best_solutions[config_name] = best_solutions_config
        
        # Cache the results
        cache_hash = cache_result(config, num_samples, (all_results, convergence_stats, best_solutions))
        print(f"Cached results for {config_name} (hash: {cache_hash[:8]}...)")
    
    return all_results, convergence_stats, best_solutions

# =============================================================================
# MAIN EXECUTION WITH ALL COMBINATIONS AND CACHING
# =============================================================================

# Create configurations with ALL combinations
configurations = create_configurations()

# Run experiments with your chosen parameters
num_samples = 1000  # Reduced for faster testing
max_generations = 200
show_variance = False

print(f"Running {len(configurations)} configurations with ALL combinations...")

# Run the experiments (will use cache if available)
all_results, convergence_stats, best_solutions = run_experiments(
    configurations, num_samples, max_generations, show_variance
)

# Create detailed analysis plots
plot_detailed_analysis(all_results, convergence_stats, show_variance, "population")
plot_detailed_analysis(all_results, convergence_stats, show_variance, "program_length")
plot_detailed_analysis(all_results, convergence_stats, show_variance, "crossover")
plot_detailed_analysis(all_results, convergence_stats, show_variance, "mutation")
plot_detailed_analysis(all_results, convergence_stats, show_variance, "selection")
plot_detailed_analysis(all_results, convergence_stats, show_variance, "iterations")
plot_detailed_analysis(all_results, convergence_stats, show_variance, "benchmark")

plot_program_length_pop_size_combination(all_results, convergence_stats)
plot_crossover_mutation_combinations(all_results, convergence_stats)

# Print best solutions found
print("\n" + "="*50)
print("BEST SOLUTIONS FOUND BY CONFIGURATION")
print("="*50)
for config_name, solution_data in best_solutions.items():
    best_ever = solution_data['best_ever']
    if best_ever:
        solution, fitness = best_ever
        print(f"{config_name}: Fitness={fitness}, Solution={solution}")

# Print configuration summary
print("\n" + "="*50)
print("CONFIGURATION SUMMARY")
print("="*50)
print(f"Total unique configurations run: {len(configurations)}")
print(f"Default Parameters:")
for key, value in DEFAULT_CONFIG.items():
    if key != 'dataset':
        print(f"  {key}: {value}")
