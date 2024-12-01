import nltk
#nltk.download('wordnet')
#nltk.download('omw-1.4')  

from nltk.corpus import wordnet


def add_synonyms(words, max_synonyms=4):
    """ Add synonyms for a list of words """
    expanded_words = {}
    
    for word in words:
        synonyms = set()
        synsets = wordnet.synsets(word)

        if synsets:
            main_synset = synsets[0]
            
            for lemma in main_synset.lemmas():
                synonyms.add(lemma.name().replace('_', ' '))
                if len(synonyms) >= max_synonyms:
                    break
        
        synonyms.add(word)
        expanded_words[word] = list(synonyms)
    
    return expanded_words


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

data = load_data(chunk_files, keyword_files)

query = "A naive implementation of the minimax algorithm can only search to a small depth in a practical amount of time, so various methods have been devised to greatly speed the search for good moves. Alpha–beta pruning, a system of defining upper and lower bounds on possible search results and searching until the bounds coincided, is typically used to reduce the search space of the program."
query = [word.lower() for word in query.split()]
query = add_synonyms(query)

# Manually add synonyms for query words 
'''synonyms = {
    "tournament": ["tournament", "event", "competition", "championship"],
    "chess": ["chess", "game", "board game", "strategy game"],
    "player": ["player", "competitor", "participant", "challenger"],
    "stockfish": ["stockfish", "supercomputer", "neural networks", "machine learning"],
    "ding": ["ding", "liren", "ding liren", "chess grandmasters"],
}
query = expand_query(query, synonyms)'''

print(f"Expanded query: {query}")
results = search_chunks(query, data)
for result in results:
    print(f"Chunk {result['index']+1} - Score: {result['score']}")

generic_words = ["chess", "game", "tournament", "player", "match", "against", "challenger", "championship"]
results = re_rank(results, data, query, generic_words)
print("\nRe-ranked results:")
for result in results:
    print(f"Chunk {result['index']+1} - Score: {result['score']}")
