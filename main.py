import random
import time


def generate_solution(k):
    # Generating a list of 0s and 1s.
    solution = [random.randint(0, 1) for _ in range(k)]
    return solution


def determine_quality(solution):
    # Determining the quality of a solution by iterating through the solution and value lists, multiplying the
    # elements with corresponding indexes and adding the result to quality.
    quality = 0
    for i in range(0, len(solution)):
        quality = quality + solution[i] * values[i]
    return quality


def is_valid(solution):
    # Checking if a solution is valid by computing the total weight(same logic as above, this time using weights list
    # instead of value), and comparing it with the max_capacity.
    total_weight = 0
    for i in range(0, len(solution)):
        total_weight = solution[i] * weights[i] + total_weight
    if total_weight <= max_capacity:
        return True
    else:
        return False


def generate_valid_solutions(n):
    # Generating a list of n valid solutions. This code generates a solution, checks validity, ignores invalid solutions
    # and adds valid solutions to a list. The number of valid solutions is also determined.
    valid_solutions = []
    counter = 0
    for i in range(0, n):
        solution = generate_solution(k)
        if is_valid(solution):
            counter = counter + 1
            valid_solutions.append(solution)
    return valid_solutions, counter


def determine_best_solution(valid_solutions):
    # This code determines the best solution out of a list of solutions by quality.
    # It creates a qualities list, from which the best quality is determined by using the max() function.
    # It returns the best solution by the index of the best quality in the qualities list(solution index and quality
    # index will always coincide).
    qualities = []
    for solution in valid_solutions:
        qualities.append(determine_quality(solution))
    return valid_solutions[qualities.index(max(qualities))], max(qualities)


def determine_worst_solution(valid_solutions):
    # The exact same logic as above, using the min() function.
    qualities = []
    for solution in valid_solutions:
        qualities.append(determine_quality(solution))
    return valid_solutions[qualities.index(min(qualities))], min(qualities)


def determine_average_quality(valid_solutions):
    # This code determines the average quality.
    qualities = []
    for solution in valid_solutions:
        qualities.append(determine_quality(solution))
    return sum(qualities) / len(qualities)


def generate_neighbor(solution, n):
    # This code determines a neighbour of a solution by 'bit flipping'.
    # For example:
    #   n = 6
    #   solution = 0 1 1 1 0 1 =>
    #   neighbour = 0 1 1 1 0 0
    neighbor = solution[:]  # shallow copy with new reference
    index = random.randint(0, n - 1)
    if neighbor[index] == 1:
        neighbor[index] = 0
    else:
        neighbor[index] = 1
    return neighbor


def random_search():
    # This code generates a random solution, checks validity, ignores invalid solutions and adds valid solutions
    # to a list.
    # The number of valid solutions is also determined.
    # The best, worst and average quality is determined.
    # The time it took to run the algorithm is also determined.
    # The results are printed to the output file.
    start_time = time.perf_counter()
    valid_solutions, valid_solution_count = generate_valid_solutions(nr_of_solutions_to_generate)
    best_solutions = []
    worst_solutions = []
    if valid_solution_count > 0:
        best_solution = determine_best_solution(valid_solutions)
        worst_solution = determine_worst_solution(valid_solutions)
        average_quality = determine_average_quality(valid_solutions)
        print(f'The generated VALID solutions are:', file=f)
        for solution in valid_solutions:
            print(solution, file=f)
        print(
            f'There is a total of {valid_solution_count} valid solutions out of {nr_of_solutions_to_generate} generated.\n',
            file=f)
        print(
            f'The best solution found for the {nr_of_solutions_to_generate} solutions generated is: {best_solution[0]} with the '
            f'quality:{best_solution[1]}', file=f)
        print(
            f'The worst solution found for the {nr_of_solutions_to_generate} solutions generated is: {worst_solution[0]} with the '
            f'quality:{worst_solution[1]}', file=f)
        print(
            f'The average quality for the {nr_of_solutions_to_generate} solutions generated is: {average_quality}\n',
            file=f)
    else:
        print(f'There were no valid solutions found out of the {nr_of_solutions_to_generate} generated.\n', file=f)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(f'This iteration of random search took {run_time} to finish \n\n', file=f)


def random_hill_climbing(nr_of_solutions_to_generate):
    # This code generates a random solution, checks validity, ignores invalid solutions and adds valid solutions
    # to a list.
    # It also determines the time it took to run the algorithm.
    start_time_hill = time.perf_counter()
    solution = generate_solution(k)
    while not is_valid(solution):  # This while loop makes sure that the starting solution is valid.
        solution = generate_solution(k)
    n = nr_of_solutions_to_generate  # n is the number of iterations for the while loop
    if is_valid(solution):
        quality = determine_quality(solution)  # if the solution is valid, the quality is determined.
        while n > 0:
            # Here we generate a neighbour and determine its quality.
            neighbor = generate_neighbor(solution, k)  # k is from main
            neighbor_quality = determine_quality(neighbor)
            if neighbor_quality > quality and is_valid(neighbor):
                # If the quality of the neighbour is better than the quality of the solution, the solution is replaced
                # by the neighbour.
                solution = neighbor
                quality = neighbor_quality
                n = n - 1
            else:
                n = n - 1
        end_time_hill = time.perf_counter()
        run_time_hill = end_time_hill - start_time_hill
        print(f'The random hill climbing algorithm found the solution: {solution}\n'
              f'    with the quality: {quality}\n'
              f'    and runtime: {run_time_hill}.', file=f)
        return solution


def parse_file(filename):
    # This code parses the input file and returns the values needed for the algorithm.
    # The first line is the number of items
    # The last line is the maximum capacity
    # The rest of the lines are the weights and values of the items
    with open(filename) as f:
        k = f.readline().strip()
        lines = f.readlines()
        max_capacity = lines[-1].strip()
        lines = lines[:-1]
        weights = []
        values = []
        for line in lines[0:]:
            line = line.split()
            weights.append(int(line[1]))
            values.append(int(line[2]))
    return int(k), int(max_capacity), weights, values


if __name__ == '__main__':
    # max_capacity = 1000
    # weights = [56, 121, 200, 5, 343, 65, 23, 434, 150, 90]
    # values = [333, 34, 1231, 6, 44, 1222, 543, 522, 999, 10000]
    # k = 10

    # This code runs the algorithm 10 times and prints the results to the output file.
    # It also prints the best and worst solution found out of the 10 iterations.
    rhc_solutions = []
    with open('output.txt', 'w') as f:
        k, max_capacity, weights, values = parse_file('rucsac-200.txt')
        for i in range(0, 10):
            nr_of_solutions_to_generate = 10
            print(f'Iteration {i + 1}:\n'
                  f'k = {k}\n'
                  f'max_capacity = {max_capacity}\n'
                  f'weights = {weights}\n'
                  f'values = {values}\n', file=f)
            print(f'USING RANDOM SEARCH ALGORITHM:', file=f)
            random_search()
            print(f'USING RHC ALGORITHM:', file=f)
            rhc_solutions.append(random_hill_climbing(nr_of_solutions_to_generate))
            print(f'---------------------------------------------------------------------\n', file=f)

        print(
            f'\n\n\nOut of {nr_of_solutions_to_generate} iterations of RHC, the best solution found was:'
            f' {determine_best_solution(rhc_solutions)} \n', file=f)
        print(f'Out of {nr_of_solutions_to_generate} iterations of RHC, the worst solution found was:'
              f' {determine_worst_solution(rhc_solutions)} \n', file=f)
        print(f'Out of {nr_of_solutions_to_generate} iterations of RHC, the average quality was:'
              f' {determine_average_quality(rhc_solutions)} \n', file=f)
