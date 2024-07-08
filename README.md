## ABSA-Synthetic
Progetto per il corso di Natural Language Processing, a.a. 2023/2024, Università degli Studi di Salerno, corso di laurea magistrale in Informatica

L'obiettivo del progetto è di valutare le prestazioni di un modello di Aspect Sentiment Triplet Extraction su un dataset sintetico.

### Modello utilizzato, realizzato da Lu Xu, Yew Ken Chia e Lidong Bing, con licenza MIT:

https://github.com/chiayewken/Span-ASTE

### Dataset utilizzato:

https://github.com/yangheng95/ABSADatasets/tree/v2.0/datasets/acos_datasets/506.Synthetic

### Comparison:
Il file "comparison_ASTE.ipynb" è stato eseguito con Google Colab, e utilizza il framework PyABSA, con licenza MIT, e la sua documentazione:
https://github.com/yangheng95/PyABSA
https://pyabsa.readthedocs.io/en/latest/

Le metriche di valutazione sono in questo caso calcolate come nel metodo "score" del file "aste/wrapper.py" della repository: https://github.com/chiayewken/Span-ASTE

Per eseguire il codice in Google Colab, caricare un dataset con nome "test_final.txt" nella cartella "/content" del runtime.

### Requisiti:
Python 3.8

Creare un virtual environment ed installare i requisiti nel file "requirements.txt"

Eseguire il file "setup.py", che si occupa di importare il modello originale clonando la repository https://github.com/chiayewken/Span-ASTE,
e modificando i parametri di configurazione per permettere di addestrare il modello senza l'utilizzo di CUDA

Il dataset deve essere inserito nell'apposita cartella "synthetic/dataset"

Per motivi di dimensione dei file, nella cartella "outputs" non sono riportati i pesi dei risultati di addestramento del modello facente utilizzo di BERT.