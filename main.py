def expand_query(query, synonyms):
    """ Expand query with synonyms """
    expanded_query = []
    for word in query:
        expanded_query.extend(synonyms.get(word, [word]))
    return expanded_query


def search_chunks(query, data):
    """ Search keyword chunks for query words """
    results = []
    for i, doc in enumerate(data):
        score = sum(1 for word in doc['keywords'] if word in query)
        if score > 0:
            results.append({"index": i+1, "chunk": doc['chunk'], "score": score})
    return sorted(results, key=lambda x: x['score'], reverse=True)


def load_data(chunk_files, keyword_files):
    """ Load data from chunk and keyword files """
    data = []
    for chunk_path, keyword_path in zip(chunk_files, keyword_files):
        with open(chunk_path, 'r') as chunk_file:
            chunk_text = chunk_file.read().strip()
        with open(keyword_path, 'r') as keyword_file:
            keywords = [line.strip().lower() for line in keyword_file.readlines()]
        data.append({"chunk": chunk_text, "keywords": keywords})
    return data


chunk_files = [f"data/chunk{i}.txt" for i in range(1, 6)]
keyword_files = [f"data/keywords{i}.txt" for i in range(1, 6)]

try:
    data = load_data(chunk_files, keyword_files)
    # for entry in data:
    #     print(f"Chunk: {entry['chunk']}\n\nKeywords: {entry['keywords']}\n")
except Exception as e:
    print(f"Error: {e}")

query = "Ding against Stockfish"
query = [word.lower() for word in query.split()]
synonyms = {
    "tournament": ["tournament", "event", "competition", "championship"],
    "chess": ["chess", "game", "board game", "strategy game"],
    "player": ["player", "competitor", "participant", "challenger"],
    "stockfish": ["stockfish", "supercomputer", "neural networks", "machine learning"],
    "ding": ["ding", "liren", "ding liren", "chess grandmasters"],
}
query = expand_query(query, synonyms)
print(f"Expanded query: {query}")
results = search_chunks(query, data)
for result in results:
    print(f"Chunk {result['index']} - Score: {result['score']}")
