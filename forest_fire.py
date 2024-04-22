###### TODO
## Add function to add desired fraction of species to initial grid
## Add moisture and SOM that influence germination speed and aging
## Add function to calculate germination probability based on soil conditions
## Add genetic diversity and introduce natural selection

import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

class Tree:
    def __init__(self, indicator, species, age, tree_age_max, resistance, germination):
        self.indicator = indicator #Value for plotting
        self.species = species
        self.age = age #Current age
        self.tree_age_max = tree_age_max #Max amount of frames before tree dies
        self.resistance = resistance #Probability of resisting fire
        self.germination = germination #Probability of seeds germinating
        

class Pine(Tree):
    def __init__(self):
        super().__init__(3,'Pine', 0, 500, 0.4, 0.02)

class Oak(Tree):
    def __init__(self):
        super().__init__(4,'Oak', 0, 1000, 0.2, 0.01)
        
class Birch(Tree):
    def __init__(self):
        super().__init__(5,'Birch', 0, 200, 0.1, 0.05)
        
class Other:
    def __init__(self, indicator, age, seed, moisture, SOM):
        self.indicator = indicator
        self.age = age
        self.seed = seed
        self.moisture = moisture
        self.SOM = SOM

class Empty(Other):
    def __init__(self):
        super().__init__(1, 0, False, 1, 10)

class Fire(Other):
    def __init__(self):
        super().__init__(2, 0, False, 0, 0)
    
# Simulation variables
x = 100
y = 100
k = 0.1

# Create a 2D array and fill it with instances of Pine, Oak, and Empty classes
forest = [[random.choice([Pine(), Oak(), Birch(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()]) for dx in range(x)] for dy in range(y)]


# Set random initial ages
for dx in range(x):
    for dy in range(y):
        if isinstance(forest[dx][dy], Tree) == True:
            forest[dx][dy].age = np.random.randint(1,getattr(forest[dx][dy], "tree_age_max"))
            

def germination_probability(plot, species):
    "Function to calculate the probability of germination per species dependent on soil conditions"
    
              
            
# Where to check for neigbouring plots

neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

def forest_fire(forest):
    #Set up next iteration of the forest
    forest_new = np.copy(forest)
    # Pre-calculate random values for the entire grid
    random_grid = np.random.random((x,y))
    
    for dx in range(x):
        for dy in range(y):
            
            
            # New Tree grows
            if isinstance(forest[dx][dy], Empty) == True and getattr(forest[dx][dy], "seed") != False:
                # Calculate probability of germination for Tree species
                germ_prob = getattr(getattr(forest[dx][dy], "seed"), "germination")
                if random_grid[dx,dy] < germ_prob:
                    forest_new[dx][dy] = getattr(forest[dx][dy], "seed")
                    
            # Tree reproduce
            if isinstance(forest[dx][dy], Tree) == True and getattr(forest[dx][dy], "age") >= 3:
                for nx, ny in neighbourhood:
                    try:
                        if isinstance(forest[dx+nx][dy+ny], Empty) == True: #and forest[dx+nx][dy+ny].seed == False:
                            forest_new[dx+nx][dy+ny].seed = type(forest[dx][dy])()
                    except IndexError:
                        pass
            
            # Fire spreads
            if isinstance(forest[dx][dy], Fire) == True:
                forest_new[dx][dy] = Empty()
                for ix, iy in neighbourhood:
                    if abs(ix) == abs(iy) and random_grid[ix,iy] < 0.5:
                        continue
                    try:
                        if isinstance(forest[dx+ix][dy+iy], Tree) == True and random_grid[dx,dy] > getattr(forest[dx+ix][dy+iy], "resistance"):
                            forest_new[abs(dx+ix)][abs(dy+iy)] = Fire()
                    except IndexError:
                        pass
            
            # Increase Tree age
            if isinstance(forest[dx][dy], Tree) == True:
                forest_new[dx][dy].age = forest_new[dx][dy].age + 1  
            
            
            # Tree dies if age is too high
            if isinstance(forest[dx][dy], Tree) == True and random_grid[dx,dy] > 1/(1.0005 + np.exp(k*(getattr(forest[dx][dy], "age")-getattr(forest[dx][dy], "tree_age_max"))/2)):
                    forest_new[dx][dy] = Empty()
            
                
            # Chance of lightning strike
            if random_grid[dx][dy] < 0.000001:
                forest_new[dx][dy] = Fire()
                   
    return forest_new

# Convert forest matrix to plottable matrix
forest_plot = [[obj.indicator for obj in row] for row in forest]

# Variables for plotting [Empty, Fire, Pine, Oak, Birch]
category_names = ['Empty', 'Fire', 'Pine', 'Oak', 'Birch']
colors_list = [(0.2,0,0), 'orange', (0,0.2,0), (0, 0.5, 0), 'grey']
cmap = colors.ListedColormap(colors_list)
bounds = list(range(1, len(colors_list) + 2))
norm = colors.BoundaryNorm(bounds, cmap.N)

# Set up plot grid
fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(forest_plot, cmap=cmap, norm=norm)



# Counter text annotation
counter_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white')

# The animation function: called to produce a frame for each generation.
def animate(i):
    # Running the simulation for one step
    animate.forest = forest_fire(animate.forest)
    # Convert forest matrix to plottable matrix
    test_forest = [[obj.indicator for obj in row] for row in animate.forest]
    # Set result as frame
    im.set_array(test_forest)
    # Update frame counter text
    counter_text.set_text('Frame: {}'.format(i))
    return im, counter_text

# Bind forest to animate function
animate.forest = forest

# Animation variables
total_frames = 10000
interval = 1

# Run the animation
anim = animation.FuncAnimation(fig, animate, frames=total_frames, interval=interval, blit = True)

# Create legend
legend_handles = [plt.Rectangle((0,0),1,1, color=cmap(i)) for i in range(len(category_names))]
plt.legend(legend_handles, category_names, loc='upper left', fontsize='large', bbox_to_anchor=(1, 1))


plt.show()
