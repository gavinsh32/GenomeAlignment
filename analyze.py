saved_data = []

class Data:
    def __init__(self):
        self.power = []
        self.tilt = []
        self.generation = 0

def save_sequence(children, generation):
    
    tilt = [obj.calcTilt() for obj in children]
    power = [obj.calcPower() for obj in children]
    
    curr = Data()
    curr.power = power
    curr.tilt = tilt
    curr.generation = generation
    
    saved_data.append(curr)

import pandas as pd
import matplotlib.pyplot as plt

def graphs_generations():
    global saved_data

    if not saved_data:  # Ensure there is data to process
        print("No data available to plot.")
        return

    # Extracting data from instances of Data class
    power = [sublist.power for sublist in saved_data]
    tilt = [sublist.tilt for sublist in saved_data]
    time = [obj.generation for obj in saved_data]


    # TRIM if needed
    min_length = min(len(time), len(power))
    generations = generations[:min_length]
    power = power[:min_length]
    tilt = tilt[:min_length]
    time = time[:min_length]

    # Creating DataFrame
    data = {'time': time, 'power': power, 'tilt': tilt}
    dataframe = pd.DataFrame(data)

    # Plotting the data
    dataframe.plot(x='time', y=['power', 'tilt'], kind='line', 
                   title='Gene Stats Over Time', 
                   xlabel='Time (Generations)', 
                   ylabel='Count', 
                   grid=True, 
                   figsize=(8, 7))

    # Saving the plot
    plt.savefig("analyze_generations.png")
    plt.show()  # To display the graph in interactive environments
    print("Plot saved to analyze.png")