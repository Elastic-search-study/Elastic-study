import pytest
from chunk_retrieval import add_synonyms_auto, categorize, categorize_chunks, add_synonyms_manual, search_chunks, re_rank, load_data

chunk_files = [f"data/chunk{i}.txt" for i in range(1, 6)]
keyword_files = [f"data/keywords{i}.txt" for i in range(6, 11)] # Use different keyword files
categories = {"Competition": ["tournament", "chess", "champion", "player", "match", "game", "world chess championship"],
            "Mathematics/Algorithms": ["machine learning", "algorithm", "minimax", "alpha-beta pruning"]}
generic_words = ["chess", "game", "tournament", "player", "match", "against", "challenger", "championship"]

@pytest.fixture
def sample_data():
    """ Load sample chunks and keywords for testing """
    return load_data(chunk_files, keyword_files)


def test_add_synonyms_auto():
    words = ["chess", "player"]
    result = add_synonyms_auto(words)
    assert "chess" in result
    assert "player" in result
    assert "participant" in result


def test_categorize():
    words = ["chess", "game", "algorithm"]
    result = categorize(words, categories)
    assert "Competition" in result
    assert "Mathematics/Algorithms" in result


def test_categorize_chunks(sample_data):
    categorized_data = categorize_chunks(sample_data, categories)
    for chunk in categorized_data:
        assert "category" in chunk
        assert isinstance(chunk["category"], list)


def test_add_synonyms_manual():
    query = ["chess", "game"]
    synonyms = {"chess": ["chess", "board game"], "game": ["game", "match"]}
    result = add_synonyms_manual(query, synonyms)
    assert "board game" in result
    assert "match" in result


def test_search_chunks(sample_data):
    query = ["chess", "strategy"]
    categorized_data = categorize_chunks(sample_data, categories)
    result = search_chunks(query, categorized_data, categories, weight_category=2)
    assert len(result) > 0
    assert all("index" in r and "score" in r for r in result)
    assert result[0]["score"] >= result[-1]["score"]


def test_re_rank(sample_data):
    query = ["chess", "algorithm"]
    results = [{"index": 0, "score": 3}, {"index": 1, "score": 1}]
    reranked = re_rank(results, sample_data, query, generic_words)
    assert reranked[0]["score"] >= reranked[-1]["score"]


def test_load_data():
    data = load_data(chunk_files, keyword_files)
    assert len(data) == len(chunk_files)
    for doc in data:
        assert "chunk" in doc
        assert "keywords" in doc


def test_expected_results():
    data = load_data(chunk_files, keyword_files)
    data = categorize_chunks(data, categories)
    
    expected_results = {
        "Chess": [1, 2, 3, 4, 5],
        "Tournament": [1, 2, 3, 4],
        "Algorithm": [4, 5],
        "Game": [2, 3, 4],
        "Strategy": [2, 4],
        "Rating": [1, 3, 4, 5],
        "Search Techniques": [4, 5],
        "Endgame Tablebase": [2, 4, 5],
        "Opening Book": [1, 2, 3, 5],
        "Node": [4, 5],
        "Events": [1, 2, 3, 4],
    }

    failed_queries = []

    for query_word, expected_chunks in expected_results.items():
        query = [word for word in query_word.lower().split()]
        query = add_synonyms_auto(query)

        results = search_chunks(query, data, categories=categories, weight_category=0) # Ignore category
        returned_chunks = [result["index"] + 1 for result in results]
        returned_chunks.sort()
        
        if set(returned_chunks) != set(expected_chunks):
            failed_queries.append({"query": query_word, "expected": expected_chunks, "returned": returned_chunks})
    
    if failed_queries:
        for failure in failed_queries:
            print(f"Query: {failure['query']} - Expected: {failure['expected']}, "f"Obtained: {failure['returned']}")
    
    assert not failed_queries

