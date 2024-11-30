def load_data(chunk_files, keyword_files):
    data = []
    
    for chunk_path, keyword_path in zip(chunk_files, keyword_files):
        with open(chunk_path, 'r') as chunk_file:
            chunk_text = chunk_file.read().strip()
        
        with open(keyword_path, 'r') as keyword_file:
            keywords = [line.strip() for line in keyword_file.readlines()]
        
        data.append({"chunk": chunk_text, "keywords": keywords})
    
    return data


chunk_files = [f"data/chunk{i}.txt" for i in range(1, 6)]
keyword_files = [f"data/keywords{i}.txt" for i in range(1, 6)]

try:
    data = load_data(chunk_files, keyword_files)
    for entry in data:
        print(f"Chunk: {entry['chunk']}\n\nKeywords: {entry['keywords']}\n")
except Exception as e:
    print(f"Error: {e}")
