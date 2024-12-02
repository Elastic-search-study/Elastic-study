# import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')

from nltk.corpus import wordnet


def add_synonyms_auto(words, max_synonyms=3):
    """ Add synonyms in a list of words """
    synonyms = set()
    for word in words:
        synsets = wordnet.synsets(word)

        if synsets:
            main_synset = synsets[0]
            for lemma in main_synset.lemmas():
                synonyms.add(lemma.name().replace('_', ' '))
                if len(synonyms) >= max_synonyms-1:
                    break
    
    words.extend(list(synonyms))
    return list(set(words))

def categorize(words, categories):
    """ Categorize words based on keywords """
    return [cat for cat, cat_words in categories.items()
            if any(keyword in cat_words for keyword in words)]

def categorize_chunks(data, categories):
    """ Categorize chunks based on keywords """
    for doc in data:
        doc["category"] = categorize(doc["keywords"], categories) 
    return data


def add_synonyms_manual(query, synonyms):
    """ Expand query with synonyms """
    expanded_query = []

    for word in query:
        expanded_query.extend(synonyms.get(word, [word]))
    return expanded_query


def search_chunks(query, data, categories, weight_category=2):
    """ Search keyword chunks for query words """
    results = []
    query_category = categorize(query, categories)

    for i, doc in enumerate(data):
        score = 0
        if query_category:
            for cat in query_category:
                score += (weight_category / len(query_category)) if cat in doc["category"] else 0

        score += sum(1 for word in query if word in doc['keywords'])
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
            keywords = keyword_file.read().lower().strip().split()

        data.append({"chunk": chunk_text, "keywords": keywords})

    return data


if __name__ == "__main__":

    chunk_files = [f"data/chunk{i}.txt" for i in range(1, 6)]
    keyword_files = [f"data/keywords{i}.txt" for i in range(1, 6)]

    expand_query_flag = True  # Choose whether to expand the query with synonyms
    re_rank_flag = True  # Choose whether to re-rank the results, reducing score for generic words

    data = load_data(chunk_files, keyword_files)

    query = "Events"
    query = [word for word in query.lower().split()]
    if expand_query_flag:
        query = add_synonyms_auto(query) # Automatically 

        # Or manually add synonyms for query words 
        '''synonyms = {
            "tournament": ["tournament", "event", "competition", "championship"],
            "chess": ["chess", "game", "board game", "strategy game"],
            "player": ["player", "competitor", "participant", "challenger"],
            "stockfish": ["stockfish", "supercomputer", "neural networks", "machine learning"],
            "ding": ["ding", "liren", "ding liren", "chess grandmasters"]}
        query = add_synonyms_manual(query, synonyms)'''

    #print(f"Expanded query: {query}")

    categories = {"Competition": ["tournament", "chess", "champion", "player", "match", "game", "world chess championship"],
                "Mathematics/Algorithms": ["machine learning", "algorithm", "minimax", "alpha-beta pruning"]}
    data = categorize_chunks(data, categories)

    results = search_chunks(query, data, categories, weight_category=0)
    print("Initial results:")
    for result in results:
        print(f"Chunk {result['index']+1} - Score: {result['score']}")

    if re_rank_flag:
        generic_words = ["chess", "game", "tournament", "player", "match", "against", "challenger", "championship"]
        results = re_rank(results, data, query, generic_words)

        print("\nRe-ranked results:")
        for result in results:
            print(f"Chunk {result['index']+1} - Score: {result['score']}")