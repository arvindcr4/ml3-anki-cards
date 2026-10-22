# ML3 Anki Cards

Anki flashcards for the PES University **ML3 (Unsupervised Learning)** end-semester assessment. One deck, 50 question/answer cards, stored as a tab-separated text file that Anki imports directly.

## Contents

`ml3_anki_cards.txt` covers:

- **Clustering** – K-Means, hierarchical (linkage methods, dendrograms, cophenetic correlation), DBSCAN (eps/MinPts selection), hard vs soft clustering, choosing an algorithm, hyperparameters, validation without labels, cluster profiling
- **Dimensionality reduction** – PCA (eigenvalues/eigenvectors, choosing components, interpretation, assumptions, practical considerations), curse of dimensionality, PCA + clustering workflows
- **Recommendation systems** – content-based vs collaborative filtering, SVD / matrix factorization and latent factors, `surprise` library parameters, explicit vs implicit feedback, cold start, sparsity, evaluation metrics
- **Association rules** – market basket analysis, support / confidence / lift, Apriori, choosing min_support, interpreting high-lift/low-support rules
- **Practicalities** – scaling, missing values, outliers, categorical variables, distance metrics (Euclidean / Manhattan / cosine), batch vs incremental clustering, `random_state`

## Import into Anki

1. Anki → **File → Import…** and pick `ml3_anki_cards.txt`.
2. The file starts with `#separator:tab` and `#html:true` header lines, so Anki 2.1.54+ picks the tab separator and HTML rendering automatically. On older versions set **Fields separated by: Tab** and tick **Allow HTML in fields** (answers use `<br>` and `<b>` for formatting).
3. Note type **Basic**, field 1 → Front, field 2 → Back. Choose or create a deck (e.g. `ML3`) and import.

## File format

One card per line: `front<TAB>back`. Lines beginning with `#` are Anki directives and are ignored. UTF-8 encoded.

## Validation

```sh
python3 validate_cards.py                    # field count, empty fields, duplicate fronts
python3 -m unittest discover -s tests -v
```
