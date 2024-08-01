import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tkinter import *
from tkinter import ttk, font, messagebox

class Rectangle:
    def __init__(self, width, height, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def area(self):
        return self.width * self.height


def check_zero(matrix, i, j, new_height, new_width):
    for m in range(i, new_height):
        for n in range(j, new_width):
            if matrix[m][n] != 0:
                return False
    return True

areas_dict = {}
def fit(rectangles, chromosome, return_matrix=False):
    if not return_matrix:
        if chromosome in areas_dict:
            return areas_dict[chromosome]

    material_matrix = np.zeros((material.height, material.width))
    area = material.area()

    for i in range(len(rectangles)):
        if chromosome[i] == "1":
            j, k = 0, 0
            while j < material.height and k < material.width:
                if material_matrix[j][k] == 0:
                    new_height = j + rectangles[i].height
                    new_width = k + rectangles[i].width
                    if new_height <= material.height and new_width <= material.width:
                        if check_zero(material_matrix, j, k, new_height, new_width):
                            area -= rectangles[i].area()
                            for m in range(j, new_height):
                                for n in range(k, new_width):
                                    material_matrix[m][n] = i + 1
                            break

                    new_height = j + rectangles[i].width
                    new_width = k + rectangles[i].height
                    if new_height <= material.height and new_width <= material.width:
                        if check_zero(material_matrix, j, k, new_height, new_width):
                            area -= rectangles[i].area()
                            for m in range(j, new_height):
                                for n in range(k, new_width):
                                    material_matrix[m][n] = i + 1
                            break

                k += 1
                if k == material.width:
                    k = 0
                    j += 1

    areas_dict[chromosome] = area

    if return_matrix:
        return material_matrix
    else:
        return area


def is_valid_chromosome(rectangles, chromosome):
    temp = 0
    for i in range(len(rectangles)):
        if chromosome[i] == "1":
            temp += rectangles[i].area()

    material_area = material.area()
    if chromosome in areas_dict:
        if areas_dict[chromosome] == material_area - temp:
            return True
    elif fit(rectangles, chromosome) == material_area - temp:
        return True

    return False


def initialize_population(population_size, individual_count, rectangles):
    population = []
    while len(population) < population_size:
        new_chromosome = "".join(random.choice("01") for _ in range(individual_count))

        if is_valid_chromosome(rectangles, new_chromosome):
            population.append(new_chromosome)

    return population


def tournament_selection(population, individual_count, rectangles):
    def fitness(chromosome):
        return fit(rectangles, chromosome)

    parents = random.sample(population, individual_count)
    return min(parents, key=fitness)


def natural_selection(individuals, individual_count):
    return individuals[:individual_count]


def sorting(individuals, rectangles):
    return sorted(individuals, key=lambda x: fit(rectangles, x))


def roulette_selection(parents):
    pairs = []
    for i in range(0, len(parents), 2):
        chances = []
        for i in range(len(parents)):
            chances.append((len(parents) - i) * random.random())
        if chances[0] >= chances[1]:
            max1 = 0
            max2 = 1
        else:
            max1 = 1
            max2 = 0

        for i in range(2, len(parents)):
            if chances[i] > chances[max1]:
                max2 = max1
                max1 = i
            elif chances[i] > chances[max2]:
                max2 = 1
        pairs.append([parents[max1], parents[max2]])

    return pairs

def crossover(pairs, rectangles):
    length = len(pairs[0][0])
    children = []

    for (a, b) in pairs:
        while True:
            r1 = random.randrange(0, length)
            r2 = random.randrange(0, length)

            if r1 < r2:
                d1 = a[:r1] + b[r1:r2] + a[r2:]
                d2 = b[:r1] + a[r1:r2] + b[r2:]

                if is_valid_chromosome(rectangles, d1) and is_valid_chromosome(rectangles, d2):
                    children.append(d1)
                    children.append(d2)
                    break
            else:
                d1 = a[:r2] + b[r2:r1] + a[r1:]
                d2 = b[:r2] + a[r2:r1] + b[r1:]
                if is_valid_chromosome(rectangles, d1) and is_valid_chromosome(rectangles, d2):
                    children.append(d1)
                    children.append(d2)
                    break

    return children

def inverse_mutation(individuals, percentage, rectangles):
    mutated_individuals = []

    for individual in individuals:
        while True:
            if random.random() < percentage and len(individual) > 1:
                r1 = random.randrange(0, len(individual) - 1)
                r2 = random.randrange(0, len(individual) - 1)

                if r1 < r2:
                    mutated = individual[:r1] + individual[r1:r2][::-1] + individual[r2:]
                    if is_valid_chromosome(rectangles, mutated):
                        mutated_individuals.append(mutated)
                        break
                else:
                    mutated = individual[:r2] + individual[r2:r1][::-1] + individual[r1:]
                    if is_valid_chromosome(rectangles, mutated):
                        mutated_individuals.append(mutated)
                        break

            else:
                mutated_individuals.append(individual)
                break

    return mutated_individuals

def elitism(old_individuals, mutated_individuals, elitism_rate, population_size):
    old_individual_size = int(np.round(population_size * elitism_rate))
    return old_individuals[:old_individual_size] + mutated_individuals[:(population_size - old_individual_size)]

def cost(rectangles, chromosome):
    return fit(rectangles, chromosome) / material.area()


def draw_rectangle(matrix):
    # Create a color map to map values to colors
    cmap = plt.get_cmap('jet')
    # Normalize the matrix values to the range [0, 1]
    norm = plt.Normalize(vmin=np.min(matrix), vmax=np.max(matrix))
    # Create a figure
    fig, ax = plt.subplots()
    # Plot the matrix as a rectangle with each element represented as a square
    ax.imshow(matrix, cmap=cmap, norm=norm)
    # Remove the axis labels
    ax.set_xticks([])
    ax.set_yticks([])
    # Create a custom legend
    unique_values = np.unique(matrix)
    patches = []
    for value in unique_values:
        color = cmap(norm(value))
        patches.append(mpatches.Patch(color=color, label=str(int(value))))
    ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    # Display the figure
    plt.show()

def remaining_percentage(rectangles, chromosome):
    if chromosome in areas_dict:
        return areas_dict[chromosome] / material.area() * 100
    else:
        return fit(rectangles, chromosome) / material.area() * 100


class InputForm(Tk):
    def __init__(self):
        self.cuts = []
        self.material_width = 0
        self.material_height = 0

        super().__init__()

        self.geometry("470x450")
        self.title("Input Form")

        input_font = font.Font(size=15)
        label_font = font.Font(size=15)

        style = ttk.Style()
        style.configure("TEdge.TEntry",
                        background="white",
                        fieldbackground="white",
                        foreground="black",
                        relief="solid",
                        bordercolor="black",
                        borderwidth=2,
                        padding=5,
                        font=input_font,
                        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        label_1 = Label(self, text="Cut Width:", font=label_font)
        label_2 = Label(self, text="Cut Height:", font=label_font)
        label_3 = Label(self, text="Rectangle Width:", font=label_font)
        label_4 = Label(self, text="Rectangle Height:", font=label_font)

        vcmd = (self.register(self.validate), '%P')
        self.input_1 = Entry(self, validate="key", validatecommand=vcmd)
        self.input_2 = Entry(self, validate="key", validatecommand=vcmd)
        self.input_3 = Entry(self, validate="key", validatecommand=vcmd)
         self.input_4 = Entry(self, validate="key", validatecommand=vcmd)

        label_1.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        label_2.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        label_3.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        label_4.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        self.input_1.grid(row=0, column=1, padx=10, pady=10, sticky=W+E)
        self.input_2.grid(row=1, column=1, padx=10, pady=10, sticky=W+E)
        self.input_3.grid(row=2, column=1, padx=10, pady=10, sticky=W+E)
        self.input_4.grid(row=3, column=1, padx=10, pady=10, sticky=W+E)

        self.submit_button = Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=20)

    def validate(self, value):
        return value.isdigit() or value == ""

    def submit(self):
        try:
            material_width = int(self.input_1.get())
            material_height = int(self.input_2.get())
            rectangle_width = int(self.input_3.get())
            rectangle_height = int(self.input_4.get())

            if material_width <= 0 or material_height <= 0 or rectangle_width <= 0 or rectangle_height <= 0:
                raise ValueError

            material = Rectangle(material_width, material_height)
            rectangles = [Rectangle(rectangle_width, rectangle_height)]

            self.cuts = rectangles
            self.material_width = material_width
            self.material_height = material_height

            self.destroy()
            self.show_results()

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter positive integers only.")

    def show_results(self):
        global material
        global rectangles
        material = Rectangle(self.material_width, self.material_height)
        rectangles = self.cuts

        population_size = 50
        individual_count = len(rectangles)
        generations = 100
        elitism_rate = 0.1
        mutation_rate = 0.1

        population = initialize_population(population_size, individual_count, rectangles)
        best_individual = None

        for _ in range(generations):
            sorted_population = sorting(population, rectangles)
            parents = roulette_selection(sorted_population)
            children = crossover(parents, rectangles)
            mutated_children = inverse_mutation(children, mutation_rate, rectangles)
            population = elitism(sorted_population, mutated_children, elitism_rate, population_size)

            best_individual = min(population, key=lambda x: fit(rectangles, x))

        result_area = fit(rectangles, best_individual)
        remaining_percentage = (result_area / material.area()) * 100

        draw_rectangle(fit(rectangles, best_individual, return_matrix=True))

        result_window = Toplevel(self)
        result_window.title("Results")
        result_window.geometry("300x150")

        Label(result_window, text=f"Best Fit Chromosome: {best_individual}", font=("Arial", 12)).pack(pady=10)
        Label(result_window, text=f"Remaining Area Percentage: {remaining_percentage:.2f}%", font=("Arial", 12)).pack(pady=10)

if __name__ == "__main__":
    app = InputForm()
    app.mainloop()
