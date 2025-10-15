import numpy as np
from collections import Counter

# Set seed for reproducibility
np.random.seed(42)

# Define number of rows and columns
rows, cols = 5000, 6

# Define probabilities for each column
probabilities = [0.6, 0.5, 0.4, 0.4, 0.4, 0.3]

# Generate matrix
matrix = np.array([
    np.random.choice([0, 1], size=rows, p=[1 - p, p])
    for p in probabilities
]).T  # Transpose to get shape (5000, 6)

# Print first 10 rows
print("First 10 rows:")
print(matrix[:10])

# Print last 10 rows
print("\nLast 10 rows:")
print(matrix[-10:])

# Convert rows to tuples for counting
tuple_rows = [tuple(row) for row in matrix]

# Filter out tuples with fewer than two 1s
filtered_rows = [tup for tup in tuple_rows if sum(tup) >= 2]

# Count frequency of each tuple
counter = Counter(filtered_rows)

# Get 10 most common tuples, in order to reduce the number of checks the program need to do
most_common_10 = counter.most_common(10)

# Calculate empirical probability of 1 in first column
prob_first_col_1 = np.mean(matrix[:, 0])

# Prepare subtuple frequency counter (columns 2–6)
subtuple_rows_2_6 = [tuple(row[1:]) for row in matrix]
sub_counter_2_6 = Counter(subtuple_rows_2_6)

# Print results with support, confidence, and lift
print("\nTop 10 most frequent tuples with at least two 1s:")
print("Dependency of the combination in columns 2-6 in case the first column is 1")
print(f"Empirical probability of 1 in first column: {prob_first_col_1:.4f}\n")

for tup, count in most_common_10:
    support = count / rows
    confidence = support / prob_first_col_1
    subtuple = tup[1:]
    sub_support = sub_counter_2_6[subtuple] / rows
    lift = confidence / sub_support if sub_support > 0 else 0
    print(f"{tup}: count = {count}, support = {support:.4f}, confidence = {confidence:.4f}, lift = {lift:.4f}")

# --- New Section: Tuples with 1 in both first and second columns ---
print("\nDependency of the combination in columns 3-6 in case the first and the second columns are 1")
print("Tuples with 1 in both first and second columns:\n")

# Calculate empirical probability of 1 in both first and second columns
both_1_mask = (matrix[:, 0] == 1) & (matrix[:, 1] == 1)
prob_first_second_1 = np.mean(both_1_mask)

# Prepare subtuple frequency counter (columns 3–6)
subtuple_rows_3_6 = [tuple(row[2:]) for row in matrix]
sub_counter_3_6 = Counter(subtuple_rows_3_6)

# Filter top 10 tuples with 1 in both first and second columns
filtered_top = [item for item in most_common_10 if item[0][0] == 1 and item[0][1] == 1]

for tup, count in filtered_top:
    support = count / rows
    confidence = support / prob_first_second_1 if prob_first_second_1 > 0 else 0
    subtuple = tup[2:]
    sub_support = sub_counter_3_6[subtuple] / rows
    lift = confidence / sub_support if sub_support > 0 else 0
    print(f"{tup}: count = {count}, support = {support:.4f}, confidence = {confidence:.4f}, lift = {lift:.4f}")