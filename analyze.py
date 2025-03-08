saved_data = []

class Data:
    def __init__(self):
        self.power = []
        self.tilt = []
        self.generation = 0
        self.success_rate = 0

def save_sequence(pop, generation, success):
    
    tilt = [obj.calcTilt() for obj in pop.population]
    power = [obj.calcPower() for obj in pop.population]
    
    curr = Data()
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
    plt.show()  # To display the graph in interactive environments
    print("Plot saved to analyze.png")