import math, itertools
from collections import Counter

# common functions for all dices the same or any dices

def generate_filters(n, num_digits):
	valid_numbers = set()
	for r in range(1, num_digits + 1):
		for digits in itertools.product(range(n + 1), repeat=r):
			if sum(digits) == n:
				valid_numbers.add(digits)
	max_length = max(len(digits) for digits in valid_numbers)
	padded_numbers = [
		''.join(map(str, (0,) * (max_length - len(digits)) + digits)) 
		for digits in valid_numbers
	]
	return sorted(set(padded_numbers))

def count_combinations(numbers, target_sum):
	valid_combinations = []
	for r in range(1, len(numbers) + 1):
		for comb in itertools.combinations(numbers, r):
			if sum(comb) == target_sum:
				valid_combinations.append(comb)
	return valid_combinations

def count_permutations(n, filter_str):
	denominator = 1
	for count in filter_str:
		denominator *= math.factorial(int(count))
	return math.factorial(n) // denominator

def generate_subsets(arr, subset_size):
	def backtrack(start, subset):
		if len(subset) == subset_size:
			result.append(sum(subset))
			return
		
		for i in range(start, len(arr)):
			backtrack(i + 1, subset + [arr[i]])

	result = []
	backtrack(0, [])
	return result

# generalised

def generate_counts(sets):
	return Counter(num for s in sets for num in s)

def get_reachable_sums_generalised(sets, n, k):
	reachable_sums = set()
	def find_sums(count, sets_subset):
		dp = {0}
		for s in sets_subset:
			dp = {x + v for x in dp for v in s}
		return dp
	# the order matters now
	for sets_subset in itertools.combinations(sets, k):
		reachable_sums.update(find_sums(k, sets_subset))
	for sets_subset in itertools.combinations(sets, n - k):
		reachable_sums.update(find_sums(n - k, sets_subset))
	return reachable_sums

def find_combinations_generalised(sets, target_sum, t):
	result = set()

	def backtrack(start, current_combination, current_sum):
		if len(current_combination) == t:
			if current_sum == target_sum:
				result.add(tuple(current_combination))
			return
		
		for i in range(start, len(sets)):
			# new for loop here
			for v in sets[i]:
				current_combination.append(v)
				backtrack(i + 1, current_combination, current_sum + v)
				current_combination.pop()

	backtrack(0, [], 0)
	return result

def filter_filters_generalised(filters, numbers, target_sum, n, k, counts):
	valid_arrangements = []
	numbers = sorted(numbers)
	for f in filters:
		digits = list(map(int, f))
		# now compute occurencies to not exceed what's allowed by the sets
		occurrences = {num: 0 for num in numbers}
		for digit, num in zip(digits, numbers):
			occurrences[num] += digit
		if any(occurrences.get(i, 0) > counts.get(i, 0) for i in occurrences):
			continue
		filtered_numbers = [num for num, count in zip(numbers, digits) for _ in range(count)]
		if sum(d * n for d, n in zip(digits, numbers)) != target_sum * 2:
			continue
		if all(sum(comb) != target_sum for comb in itertools.combinations(filtered_numbers, k)) and \
		   all(sum(comb) != target_sum for comb in itertools.combinations(filtered_numbers, n - k)):
			continue
		valid_arrangements.append(f)
	return valid_arrangements

def solve_generalised(sets, n, k, generate_solutions):
	total = 0
	solutions = []
	counts = generate_counts(sets)
	for target_sum in get_reachable_sums_generalised(sets, n, k):
		# print(f"{target_sum = }")
		# continue
		r = find_combinations_generalised(sets, target_sum, k) | find_combinations_generalised(sets, target_sum, n-k)
		# print(r)
		# continue
		numbers = set()
		for tmp in r:
			numbers.update(tmp)
		# print(f"{numbers = }")
		filters = generate_filters(n, len(numbers))
		# print(f"{filters = }")
		# continue
		valid_filters = filter_filters_generalised(filters, numbers, target_sum, n, k, counts)
		# print(f"{valid_filters = }")
		# continue
		if generate_solutions:
			for f in valid_filters:
				cur = count_permutations(n, f)
				total += cur
				solution = tuple(sorted([d for m, d in zip(f, numbers) for _ in range(int(m))]))
				solutions.append((target_sum, solution, cur))
		else:
			total += sum(count_permutations(n, f) for f in valid_filters)
	return total, solutions

# all dices the same (much quicker), especially find_combinations

def get_reachable_sums(values, n, k):
	reachable_sums = set()
	def find_sums(count):
		dp = {0} 
		for _ in range(count):
			dp = {s + v for s in dp for v in values}
		return dp
	reachable_sums.update(find_sums(k))
	reachable_sums.update(find_sums(n - k))
	return reachable_sums

def find_combinations(values, target_sum, t):
	result = set()
	values = list(values)
	def backtrack(current_combination, current_sum):
		if len(current_combination) == t:
			if current_sum == target_sum:
				result.add(tuple(current_combination))
			return
		for v in values:
			current_combination.append(v)
			backtrack(current_combination, current_sum + v)
			current_combination.pop()
	backtrack([], 0)
	return result

def filter_filters(filters, numbers, target_sum, n, k):
	valid_arrangements = []
	for f in filters:
		digits = list(map(int, f))
		filtered_numbers = [num for num, count in zip(numbers, digits) for _ in range(count)]
		if sum(d * n for d, n in zip(digits, numbers)) != target_sum * 2:
			continue
		if not any(sum(comb) == target_sum for comb in itertools.combinations(filtered_numbers, k)) and \
		   not any(sum(comb) == target_sum for comb in itertools.combinations(filtered_numbers, n - k)):
			continue
		valid_arrangements.append(f)
	return valid_arrangements

def solve(S, n, k, generate_solutions):
	total = 0
	solutions = []
	for target_sum in get_reachable_sums(S, n, k):
		# print(f"{target_sum = }")
		r = find_combinations(S, target_sum, k) | find_combinations(S, target_sum, n-k)
		# print(r)
		# continue
		numbers = set()
		for tmp in r:
			numbers.update(tmp)
		# print(f"{numbers = }")
		# continue
		filters = generate_filters(n, len(numbers))
		# print(f"{filters = }")
		# continue
		valid_filters = filter_filters(filters, numbers, target_sum, n, k)
		# print(f"{valid_filters = }")
		# continue
		if generate_solutions:
			for f in valid_filters:
				cur = count_permutations(n, f)
				total += cur
				solution = tuple(sorted([d for m, d in zip(f, numbers) for _ in range(int(m))]))
				solutions.append((target_sum, solution, cur))
		else:
			total += sum(count_permutations(n, f) for f in valid_filters)
	return total, solutions

# main

def report(n, k, generate_solutions, result, solutions):
	print(f"{n = }, {k = }, number of solutions = {result}")
	if generate_solutions:
		if solutions:
			print("solutions:")
		for sol in solutions:
			print(sol)

def solve_one(n, k, sets, generate_solutions=False):
	report(n, k, generate_solutions, *solve_generalised(sets, n, k, generate_solutions))

def solve_all(S, max_n, generate_solutions=False):
	for n in range(1, max_n+1):
		for k in range(1, n//2+1):
			report(n, k, generate_solutions, *solve(S, n, k, generate_solutions))

def main():
	# solve_one(4, 2, [set(range(6)) for _ in range(4)])
	solve_one(4, 1, [{1, 2, 3}, {4, 5, 6}, {2}, {3, 8, 5}], True)
	# solve_all({1, 2, 3, 4, 5, 6}, 10)

if __name__ == '__main__':
	main()