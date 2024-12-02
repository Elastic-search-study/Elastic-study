# Elastic-study

## Expected Outcome
| Chunk               | 1   | 2   | 3   | 4   | 5   |
|---------------------|-----|-----|-----|-----|-----|
| **Chess**           | X   | X   | X   | X   | X   |
| **Tournament**      | X   | X   | X   | X   |     |
| **Algorithm**       |     |     |     | X   | X   |
| **Game**            |     | X   | X   | X   |     |
| **Strategy**        |     | X   |     | X   |     |
| **Rating**          | X   |     | X   | X   | X   |
| **Search techniques**|     |     |     | X   | X   |
| **Endgame tablebase**|     | X   |     | X   | X   |
| **Opening book**    | X   | X   | X   |     | X   |
| **Node**            |     |     |     | X   | X   |
| **Events**          | X   | X   | X   | X   |     |

***

Results with initial keywords:

Prompt: I want to extract 20 key words from this wikipedia page extract : '''Page name : World Chess Championship 2024 + ‘’’chunk’’’

1. Chess - Expected: \[1, 2, 3, 4, 5\], Obtained: \[1, 2, 3, 4, 5\] 
2. Tournament - Expected: \[1, 2, 3, 4\], Obtained: \[1, 2, 3\]
3. Algorithm - Expected: \[4, 5\], Obtained: \[4, 5\]
4. Game - Expected: \[2, 3, 4\], Obtained: \[2, 5\]
5. Strategy - Expected: \[2, 4\], Obtained: \[2\]
6. Rating - Expected: \[1, 3, 4, 5\], Obtained: \[1, 3, 4, 5\]
7. Search Techniques - Expected: \[4, 5\] - Obtained: \[4, 5\],
8. Endgame Tablebase - Expected: \[2, 4, 5\], Obtained: \[4, 5\]
9. Opening Book - Expected: \[1, 2, 3, 5\], Obtained: \[2, 5\]
10. Node - Expected: \[4, 5\], Obtained: \[\]
11. Events - Expected: \[1, 2, 3, 4\], Obtained: \[\]

***

Results with modified keywords:

Prompt: Extract the 30 most specific and relevant keywords from this text. Ensure all keywords are converted to their lemma forms (e.g., singular nouns, infinitive verbs): + ‘’’chunk’’’

1. Chess - Expected: \[1, 2, 3, 4, 5\], Obtained: \[1, 2\]
2. Tournament - Expected: \[1, 2, 3, 4\], Obtained: \[1, 3, 4\]
3. Algorithm - Expected: \[4, 5\], Obtained: \[5\]
4. Game - Expected: \[2, 3, 4\], Obtained: \[1, 2\]
5. Strategy - Expected: \[2, 4\], Obtained: \[4\]
6. Rating - Expected: \[1, 3, 4, 5\], Obtained: \[2, 3, 4\]
7. Search Techniques - Expected: \[4, 5\], Obtained: \[4, 5\]
8. Endgame Tablebase - Expected: \[2, 4, 5\], Obtained: \[2\]
9. Opening Book - Expected: \[1, 2, 3, 5\], Obtained: \[2\]
10. Node - Expected: \[4, 5\], Obtained: \[4, 5\]
11. Events - Expected: \[1, 2, 3, 4\], Obtained: \[2, 3\]


Prompt: Extract the 30 most relevant keywords from this text, you can include generic words from the topic (if they are relevant). Ensure all keywords are converted to their lemma forms (e.g., singular nouns, infinitive verbs): + ‘’’chunk’’’

1. Chess - Expected: \[1, 2, 3, 4, 5\], Obtained: \[1, 2, 3, 4, 5\]
2. Tournament - Expected: \[1, 2, 3, 4\], Obtained: \[1, 3, 4, 5\]
3. Algorithm - Expected: \[4, 5\], Obtained: \[4, 5\]
4. Game - Expected: \[2, 3, 4\], Obtained: \[1, 2, 4, 5\]
5. Strategy - Expected: \[2, 4\], Obtained: \[4\]
6. Rating - Expected: \[1, 3, 4, 5\], Obtained: \[1, 3, 4, 5\]
7. Search Techniques - Expected: \[4, 5\], Obtained: \[4, 5\]
8. Endgame Tablebase - Expected: \[2, 4, 5\], Obtained: \[\]
9. Opening Book - Expected: \[1, 2, 3, 5\], Obtained: \[2\]
10. Node - Expected: \[4, 5\], Obtained: \[4, 5\]
11. Events - Expected: \[1, 2, 3, 4\], Obtained: \[2, 3\]
