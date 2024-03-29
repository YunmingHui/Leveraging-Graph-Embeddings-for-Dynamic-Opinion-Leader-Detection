# Leveraging Graph Embedding for Opinion Leader Detection in Dynamic Social Networks
This is the code for paper "Leveraging Graph Embedding for Opinion Leader Detection in Dynamic Social Networks"

## Introduction
Detecting opinion leaders from dynamic social networks is an important and complex problem. The few methods in this field are poor in generalisation and cannot fully consider various dynamic features. In this paper, we propose a novel and generic method based on dynamic graph embedding and clustering. Inspired by the existing knowledge about dynamic opinion leader detection, the proposed method can exploit both the topological and temporal information of dynamic social networks comprehensively. It is also generalisable, as shown experimentally on three different dynamic social network datasets. The experimental results show that the proposed method runs faster than competitors.

## Run the code
Dependencies (with python >= 3.6):

```{bash}
networkx
numpy
scikit_learn
```
### Graph Embedding
Please used the code provided by the authors of TGN to do graph embedding first: [TGN](https://github.com/twitter-research/tgn) and save the graph embedding results in 'Embeddings'

### Run the proposed method
```{bash}
python run.py
```

### Evaluate with SI model
```{bash}
python evaluation.py
```

### Baselines
```{bash}
### INDDSN
python INDDSN.py

### LeaderRank
python LeaderRank.py

### SSA
python SSA.py
```

## Cite us
```bibtex
@inproceedings{hui2023leveraging,
  title={Leveraging Graph Embedding for Opinion Leader Detection in Dynamic Social Networks},
  author={Hui, Yunming and Chekol, Mel and Wang, Shihan},
  booktitle={European Conference on Artificial Intelligence},
  pages={5--22},
  year={2023},
  organization={Springer}
}
```
