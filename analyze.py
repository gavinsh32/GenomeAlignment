saved_data = []

class Data:
    def __init__(self):
        self.children = []
        self.power = []
        self.tilt = []
        self.generation = 0
        self.success_rate = 0

def save_sequence(pop, generation, success):
    
    tilt = [obj.calcTilt() for obj in pop.population]
    power = [obj.calcPower() for obj in pop.population]
    
    curr = Data()
    curr.children = pop
    curr.power = power
    curr.tilt = tilt
    curr.generation = generation
    curr.success_rate = success
    
    saved_data.append(curr)

import pandas as pd
import matplotlib.pyplot as plt

def graphs_generations():
    global saved_data

    if not saved_data:  # Ensure there is data to process
        print("No data available to plot.")
        return

    # Extracting data from instances of Data class
    power = sum([sublist.power for sublist in saved_data], [])
    tilt = sum([sublist.tilt for sublist in saved_data], [])
    time = [obj.generation for obj in saved_data]
    success = [obj.success_rate*100 for obj in saved_data]

    # TRIM if needed
    min_length = min(len(time), len(power))
    time = time[:min_length]
    power = power[:min_length]
    tilt = tilt[:min_length]
    success = success[:min_length]

    # Creating DataFrame
    data = {'time': time, 'power': power, 'tilt': tilt, 'success': success}
    dataframe = pd.DataFrame(data)
    # print(dataframe)
    # print(dataframe.dtypes)

    # Plotting the data
    dataframe.plot(x='time', y=['power', 'tilt', 'success'], kind='line', 
                   title='Gene Stats Over Time', 
                   xlabel='Time (Generations)', 
                   ylabel='Count', 
                   grid=True, 
                   figsize=(8, 7))

    # Saving the plot
    plt.savefig("analyze_generations.png")
    #plt.show()  # To display the graph in interactive environments
    print("Plot saved to analyze.png")
    
    

from collections import Counter

def graph_gene_count():
    global saved_data

    if not saved_data:  # Ensure there is data to process
        print("No data available to plot.")
        return
    
    # Initialize dictionaries to store total gene counts for tilt and power genes for each generation
    tilt_counts = {'A': [], 'C': [], 'T': [], 'G': []}
    power_counts = {'A': [], 'C': [], 'T': [], 'G': []}
    generations = []
    
    # Process each cannon in the population
    for obj in saved_data:
        generations.append(obj.generation)
        
        # Initialize counts for each generation
        total_a_tilt = 0
        total_c_tilt = 0
        total_t_tilt = 0
        total_g_tilt = 0
        total_a_power = 0
        total_c_power = 0
        total_t_power = 0
        total_g_power = 0
        
        for cannon in obj.children.population:
            # Separate tilt and power genes
            tilt_genes = cannon.getTiltGene()
            power_genes = cannon.getPowerGene()
            
            # Count occurrences of each allele in tilt genes
            tilt_counts_current = Counter(tilt_genes)
            total_a_tilt += tilt_counts_current.get('A', 0)
            total_c_tilt += tilt_counts_current.get('C', 0)
            total_t_tilt += tilt_counts_current.get('T', 0)
            total_g_tilt += tilt_counts_current.get('G', 0)
            
            # Count occurrences of each allele in power genes
            power_counts_current = Counter(power_genes)
            total_a_power += power_counts_current.get('A', 0)
            total_c_power += power_counts_current.get('C', 0)
            total_t_power += power_counts_current.get('T', 0)
            total_g_power += power_counts_current.get('G', 0)

        # Store the results for the current generation
        num_children = len(obj.children.population)
        tilt_counts['A'].append(total_a_tilt / num_children)
        tilt_counts['C'].append(total_c_tilt / num_children)
        tilt_counts['T'].append(total_t_tilt / num_children)
        tilt_counts['G'].append(total_g_tilt / num_children)
        power_counts['A'].append(total_a_power / num_children)
        power_counts['C'].append(total_c_power / num_children)
        power_counts['T'].append(total_t_power / num_children)
        power_counts['G'].append(total_g_power / num_children)
        
    # Create DataFrame for plotting
    data = {
        'Generation': generations,
        'A (Tilt)': tilt_counts['A'],
        'C (Tilt)': tilt_counts['C'],
        'T (Tilt)': tilt_counts['T'],
        'G (Tilt)': tilt_counts['G'],
        'A (Power)': power_counts['A'],
        'C (Power)': power_counts['C'],
        'T (Power)': power_counts['T'],
        'G (Power)': power_counts['G']
    }
    
    dataframe = pd.DataFrame(data)

    # Plot the data
    ax = dataframe.plot(x='Generation', y=['A (Tilt)', 'C (Tilt)', 'T (Tilt)', 'G (Tilt)',
                                           'A (Power)', 'C (Power)', 'T (Power)', 'G (Power)'], kind='line',
                       title='Average Gene Count Comparison by Generation (Tilt vs Power)',
                       xlabel='Generation',
                       ylabel='Average Count',
                       grid=True,
                       figsize=(10, 8))

    # Set the y-axis limit to 100
    # ax.set_ylim(0, 100)
    
    # Save and display the plot
    plt.savefig("average_gene_counts.png")
    plt.show()
    print("Plot saved to average_gene_counts.png")
