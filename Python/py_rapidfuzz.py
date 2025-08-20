from rapidfuzz import fuzz, process

# 1. Simple Ratio (Levenshtein Distance similarity)
print(f"fuzz.ratio :{fuzz.ratio("hello world", "hallo werld")}")

# 2. Partial Ratio (finds the best matching substring)
print(f"fuzz.partial_ratio :{fuzz.partial_ratio("apple", "red delicious apple")}")

# 3. Token Sort Ratio (compares sorted tokens, ignores order)
print(f"fuzz.token_sort_ratio :{fuzz.token_sort_ratio("world hello", "hello world")}")

# 4. Token Set Ratio (compares unique tokens, ignores duplicates and order)
print(f"fuzz.token_set_ratio :{fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")}")

# 5. Weighted Ratio (combines multiple metrics and weights them)
print(f"fuzz.WRatio :{fuzz.WRatio("this is a test", "this is a new test!!!")}")


choices = ["New York Jets", "New York Giants", "Dallas Cowboys", "Atlanta Falcons"]

# 1. extract: Find top N best matches
query = "new york jets"
results = process.extract(query, choices, scorer=fuzz.WRatio, limit=2)
print(results)
print(f"extract: Find top N best matches :{results}")

# Output: [('New York Jets', 100.0, 0), ('New York Giants', 78.57142857142857, 1)]
# (match_string, score, original_index)

# 2. extractOne: Find the single best match
query = "cowboys"
best_match = process.extractOne(query, choices, scorer=fuzz.WRatio)
print(f"Find the single best match :{best_match}")

# Output: ('Dallas Cowboys', 90.0, 2)