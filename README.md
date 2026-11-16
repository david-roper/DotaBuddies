# DotaBuddies

A machine learning project that predicts the outcome of a Dota 2 match from the heroes each team picks. The long-term goal is to use those predictions to recommend heroes during the draft.

Built as a course project for COMP 432 (Machine Learning) at Concordia University, Winter 2023. The full write-up (abstract, method, results and references) is in [DotaBuddies.ipynb](DotaBuddies.ipynb).

## How it works

1. **Collect matches.** Match results and hero picks come from two sources:
   - Recent public All Pick matches from the [OpenDota API](https://docs.opendota.com/) (40,000 matches, 138 hero IDs).
   - The older [Kaggle "Dota 2 Matches" dataset](https://www.kaggle.com/datasets/devinanzelmo/dota-2-matches) (50,000 matches, 113 hero IDs).
2. **Build feature vectors.** Each match becomes a vector with one slot per hero for each team: a 1 marks a hero picked by Radiant in the first half, or by Dire in the second half. That gives 276 features for the OpenDota data and 226 for the Kaggle data.
3. **Train classifiers.** PyTorch feed-forward networks are trained with `BCEWithLogitsLoss` and Adam (weight decay as L2 regularization), with dropout, batch norm and early stopping on the larger models.
4. **Score symmetrically.** At test time each match is scored twice, once as given and once with the teams swapped, and the two predictions are averaged to get the final result.

## Results

| Model | Data | Test accuracy |
|---|---|---|
| Model 1: small DNN (1 hidden layer, 16 units) | OpenDota | 53.9% |
| Model 2: deeper DNN with dropout | OpenDota | 54.0% |
| Model 1: small DNN | Kaggle | **60.1%** |
| Model 3: deeper DNN with batch norm and dropout | Kaggle | 56.5% |

The 70% target was not reached. The deeper models overfit: training accuracy kept improving while validation accuracy stalled. Accuracy was higher on the older Kaggle data, which suggests that a larger hero pool makes the outcome harder to predict from picks alone. Possible next steps include adding bans and pick order to the features, better regularization, and a wider hyperparameter search. The notebook covers these in more detail.

## Repository layout

| Path | Description |
|---|---|
| [DotaBuddies.ipynb](DotaBuddies.ipynb) | Final report: the full pipeline, training runs, plots and discussion. Written for Google Colab. |
| [currentmatches.ipynb](currentmatches.ipynb) | Experiments on the OpenDota data, including scikit-learn MLP and logistic regression baselines. |
| [model.ipynb](model.ipynb) | Early model prototype on `matchdata.csv`. |
| [getmatchdata.py](getmatchdata.py) | Pages through the OpenDota `publicMatches` endpoint and writes `newmatchdata.csv`. |
| [getolddata.py](getolddata.py) | Converts the Kaggle `match.csv` and `players.csv` into `oldmatchdata.csv`. |
| [check.py](check.py) | Checks for duplicate match IDs between raw JSON pulls and builds the next pagination URL. |
| [heroes.json](heroes.json) | Hero ID → name lookup. |
| `newmatchdata.csv` | 40,000 OpenDota matches (the main dataset). |
| `oldmatchdata.csv` | 50,000 Kaggle matches. |
| `matchdata.csv` | 20,000 OpenDota matches from an earlier pull. |
| `matchdata*.json` | Raw OpenDota API responses. |

All match CSVs have the same columns:

```
radiant_win,rhero1,rhero2,rhero3,rhero4,rhero5,dhero1,dhero2,dhero3,dhero4,dhero5
```

`radiant_win` is `1` if Radiant won and `0` otherwise. The other columns are hero IDs (see `heroes.json`).

## Getting started

Requires Python 3.10 and [Pipenv](https://pipenv.pypa.io/).

```bash
pipenv install
pipenv install pandas requests skorch   # used by the scripts/notebooks but not yet in the Pipfile
pipenv run jupyter notebook             # or pick the Pipenv kernel in VS Code
```

The Pipfile pulls PyTorch from the CUDA 11.8 index. On a machine without an NVIDIA GPU (macOS included), change the `torch`/`torchvision` entries to plain `"*"`. The notebooks fall back to the CPU when CUDA isn't available.

### Refreshing the data

```bash
pipenv run python getmatchdata.py   # ~8 minutes: 400 requests, paced for OpenDota's rate limit
```

To rebuild the Kaggle dataset, download `match.csv` and `players.csv` from Kaggle into the project root, then run `getolddata.py`.

> **Note:** [DotaBuddies.ipynb](DotaBuddies.ipynb) was written for Colab and expects the data under `DotabuddiesData/` (it downloads that folder from Google Drive in its first cell). To run it locally, change those paths to point at the CSVs in the project root.

## References

1. Conley, K., Perry, D. *How Does He Saw Me? A Recommendation Engine for Picking Heroes in Dota 2.* Stanford CS229, 2013. [PDF](https://cs229.stanford.edu/proj2013/PerryConley-HowDoesHeSawMeARecommendationEngineForPickingHeroesInDota2.pdf)
2. [OpenDota API](https://docs.opendota.com/)
3. Anzelmo, D. [Dota 2 Matches](https://www.kaggle.com/datasets/devinanzelmo/dota-2-matches), Kaggle.
