import pytest
from main import add_synonyms, categorize, categorize_chunks, expand_query, search_chunks, re_rank, load_data

chunk_files = [f"data/chunk{i}.txt" for i in range(1, 6)]
keyword_files = [f"data/keywords{i}.txt" for i in range(1, 6)]
categories = {"Competition": ["tournament", "chess", "champion", "player", "match", "game", "world chess championship"],
            "Mathematics/Algorithms": ["machine learning", "algorithm", "minimax", "alpha-beta pruning"]}
generic_words = ["chess", "game", "tournament", "player", "match", "against", "challenger", "championship"]

@pytest.fixture
def sample_data():
    """ Load sample chunks and keywords for testing """
    return load_data(chunk_files, keyword_files)

def test_add_synonyms():
    words = ["chess", "player"]
    result = add_synonyms(words, max_synonyms=3)
    assert "chess" in result
    assert len(result["chess"]) <= 3
    assert "player" in result

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

def test_expand_query():
    query = ["chess", "game"]
    synonyms = {"chess": ["chess", "board game"], "game": ["game", "match"]}
    result = expand_query(query, synonyms)
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
