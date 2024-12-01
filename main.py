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
        score = sum(1 for word in query if word in doc['keywords'])
        if score > 0:
            results.append({"index": i, "score": score})
    return sorted(results, key=lambda x: x['score'], reverse=True)


def re_rank(results, data, query, generic_words, weight_specific=2, weight_generic=-1):
    """ Re-rank results and reduce score for generic words """
    for result in results:
        keywords = data[result["index"]]["keywords"]
        generic_count = sum(1 for word in query if word in generic_words and word in keywords)
        specific_count = sum(1 for word in query if word not in generic_words and word in keywords)
        
        result["score"] += (specific_count * weight_specific)  
        result["score"] += (generic_count * weight_generic)    

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

    query = "Computer chess IC bearing the name of developer Frans Morsch (see Mephisto)"
    query = [word.lower() for word in query.split()]
    synonyms = {
        "tournament": ["tournament", "event", "competition", "championship"],
        "chess": ["chess", "game", "board game", "strategy game"],
        "player": ["player", "competitor", "participant", "challenger"],
        "stockfish": ["stockfish", "supercomputer", "neural networks", "machine learning"],
        "ding": ["ding", "liren", "ding liren", "chess grandmasters"],
    }
    generic_words = ["chess", "game", "tournament", "player", "match", "against", "challenger", "championship"]

    query = expand_query(query, synonyms)
    print(f"Expanded query: {query}")
    results = search_chunks(query, data)
    for result in results:
        print(f"Chunk {result['index']+1} - Score: {result['score']}")

    print('\n')
    results = re_rank(results, data, query, generic_words)
    for result in results:
        print(f"Chunk {result['index']+1} - Score: {result['score']}")

except Exception as e:
    print(f"Error: {e}")