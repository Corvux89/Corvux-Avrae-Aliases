input_array = ['(SW) Call Lightning', '-with', 'wis', 'bch', '-f', 'Force Points (-4)|37/57', '-dc', '+0', '-b', '2', '-i']

# Iterate through the array
result = None
for item in input_array:
    # Check if the string contains a '-' followed by digits
    if 'Force Points' in item:
        result = item.split('-')
        result = result[1].split(")")[0]
        break

    if result:
        break

print(result)
