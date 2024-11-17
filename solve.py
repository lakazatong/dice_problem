import math, itertools

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
	"""
	Generate all subsets of a given size from the array using backtracking.
	"""
	def backtrack(start, subset):
		if len(subset) == subset_size:
			result.append(sum(subset))
			return
		
		for i in range(start, len(arr)):
			backtrack(i + 1, subset + [arr[i]])

	result = []
	backtrack(0, [])
	return result

def find_combinations(values, target_sum, t):
	"""
	Find all combinations of size t that sum up to target_sum.
	Uses backtracking to explore all possibilities.
	"""
	result = set()
	values = list(values)  # Convert set to list
	
	def backtrack(start, current_combination, current_sum):
		# If the combination size is t, check if the sum matches
		if len(current_combination) == t:
			if current_sum == target_sum:
				result.add(tuple(current_combination))
			return
		# Try adding more elements from start position
		for i in range(start, len(values)):
			current_combination.append(values[i])
			backtrack(i, current_combination, current_sum + values[i])
			current_combination.pop()
	
	backtrack(0, [], 0)
	return result

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

S = {1, 2, 3, 4, 5, 6}

for n in range(1, 10+1):
	for k in range(1, n//2+1):
		t = 0
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
			# print()
			# continue
			cur = sum(count_permutations(n, f) for f in valid_filters)
			# print(target_sum, cur)
			t += cur
		print(n, k, t)