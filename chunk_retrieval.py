import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import wordnet


def add_synonyms_auto(words):
    """ Add synonyms in a list of words """
    synonyms = set()

    for word in words:
        for synset in wordnet.synsets(word): # Synset is a set of synonyms
            for lemma in synset.lemmas(): # Lemma is the base form of a word
                synonyms.add(lemma.name().replace('_', ' '))
    
    return list(set(words + list(synonyms))) # Remove duplicates


def add_synonyms_manual(query, synonyms):
    """ Expand query with manual synonyms dictionary """
    expanded_query = []

    for word in query:
        expanded_query.extend(synonyms.get(word, [word])) 
    return expanded_query


def categorize(words, categories):
    """ Categorize list of words (query or chunks) based on category keywords """
    return [category for category, category_words in categories.items()
            if any(keyword in category_words for keyword in words)]


def categorize_chunks(data, categories):
    """ Categorize chunks based on category keywords """
    for doc in data:
        doc["category"] = categorize(doc["keywords"], categories) 
    return data


def search_chunks(query, data, categories, weight_category=1):
    """ Search keyword chunks for query words """
    results = []
    query_category = categorize(query, categories)

    for i, doc in enumerate(data):
        score = 0
        if query_category: # If query has category
            for category in query_category:
                # Add score if query category relates to chunk category
                # Divide by length of query category if multiple categories
                score += (weight_category / len(query_category)) if category in doc["category"] else 0

        # Add score for each query word in chunk keywords
        score += sum(1 for word in query if word in doc['keywords']) 
        if score > 0:
            results.append({"index": i, "score": score})

    return sorted(results, key=lambda x: x['score'], reverse=True)


def re_rank(results, data, query, generic_words, weight_specific=1, weight_generic=-1):
    """ Re-rank results and reduce score for generic words """
    for result in results:
        keywords = data[result["index"]]["keywords"] # Keywords of specific chunk
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
            keywords = list(set(keyword_file.read().lower().strip().split())) # Remove duplicates

        data.append({"chunk": chunk_text, "keywords": keywords})

    return data


if __name__ == "__main__":

    chunk_files = [f"data/chunk{i}.txt" for i in range(1, 6)]
    keyword_files = [f"data/keywords{i}.txt" for i in range(1, 6)]

    expand_query_flag = True  # Choose whether to expand the query with synonyms
    re_rank_flag = True  # Choose whether to re-rank the results, reducing score for generic words

    data = load_data(chunk_files, keyword_files)

    query = "Chess tournament player Stockfish against Ding Liren"
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

    # Exemple of categories, can be expanded
    categories = {"Competition": ["tournament", "chess", "champion", "player", "match", "game", "world chess championship"],
                "Mathematics/Algorithms": ["machine learning", "algorithm", "minimax", "alpha-beta pruning"]}
    data = categorize_chunks(data, categories)

    results = search_chunks(query, data, categories, weight_category=0) # Set weight_category to 0 to ignore category
    print("Initial results:")
    for result in results:
        print(f"Chunk {result['index']+1} - Score: {result['score']}")

    if re_rank_flag:
        # Exemple of generic words, can be expanded
        generic_words = ["chess", "game", "tournament", "player", "match", "against", "challenger", "championship"]
        results = re_rank(results, data, query, generic_words)

        print("\nRe-ranked results:")
        for result in results:
            print(f"Chunk {result['index']+1} - Score: {result['score']}")