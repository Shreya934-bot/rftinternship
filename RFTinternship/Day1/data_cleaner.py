data = [10, None, 20, 10, "", 30, None, 40]

def clean_data(data):
    cleaned = []
    seen = set()
    removed = 0

    for item in data:
        if item is None or item == "":
            removed += 1
            continue
        
        if item in seen:
            removed += 1
            continue
        
        seen.add(item)
        cleaned.append(item)

    return sorted(cleaned), removed

cleaned_list, removed_count = clean_data(data)

print("Cleaned List:", cleaned_list)
print("Total Removed Values:", removed_count)