# Genetic Algorithm for 2D Cutting Problem

### Students
- Vladimir Čornenki, SV53/2021
- Nemanja Stjepanović, SV75/2021

### Subject
Nonlinear Programming and Evolutionary Algorithms
---

### Problem Description
The 2D cutting problem involves cutting a material of given height and width into smaller pieces of specific dimensions with the goal of minimizing waste.

### Program Structure

1. **Rectangle Class Definition**
   - The `Rectangle` class has two attributes: height and width, and a method `area` that returns the area of the rectangle.
   - The dimensions of the initial material and the rectangles to be placed are input through the GUI.

2. **Solution Functions**
   - One of the crucial functions is `fit`, which places all rectangles onto the main material and returns the amount of free material surface. It uses a matrix of height x width initially filled with 0s. For each rectangle placement, it fills the matrix with the area of the rectangle.
   - The `fit` function takes a chromosome (a binary string where '1' denotes a rectangle placed and '0' denotes a rectangle not placed) and uses another function `check_zeros` to traverse the matrix and check for available space to fit the rectangle. If necessary, it rotates the rectangle and tries to fit it again.

3. **Population Initialization**
   - The population is initialized by generating a random binary string of length equal to the number of rectangles to be placed. The function `valid_chromosome` checks if the string is a valid solution, i.e., if each rectangle marked '1' in the string can be placed on the material.

4. **Genetic Algorithm Loop**
   - The algorithm ranks individuals based on the free surface using the `sort` function and selects the best individuals as parents through natural selection.
   - Parent pairs are chosen using roulette selection, followed by crossover and mutation operations.
   - After crossover and mutation, chromosomes are ranked again, and the best individuals are selected using elitism to form the new population.
   - The average free surface and the surface of the best chromosome in each generation are recorded.

### Mutation and Crossover Implementation

- **Crossover:** Implements two-point crossover, randomly selecting two crossover points in the binary string. New chromosomes (offspring) are created by swapping the segments between the two crossover points. Valid offspring are added to the offspring list. If offspring are not valid, new crossover points are generated until valid offspring are produced.
- **Selection:** Uses roulette selection to determine the probability of each parent being chosen. The probabilities are calculated as `(list length - parent index) * random.random()`, giving higher chances to parents later in the list. The parents with the highest chances are selected.

### Algorithm Parameters and Results

- **Population Size:** 10
- **Mutation Coefficient:** 0.9
- **Number of Individuals for Natural Selection:** 6
- **Maximum Number of Iterations:** 100
- **Elitism Rate:** 0.05 (percentage of population carried over to the next generation)

The program stops generating when the free surface is less than 5% of the total surface 20 times. At the end, a visualization of the rectangles is displayed with occupied areas colored, and the percentage of unfilled surface is printed in the terminal.

---

Feel free to check out the code and provide any feedback or suggestions for improvements!
