DATA ANALYSIS PROJECT WORKFLOW
(avec les fonctions les plus utilisées)

│
├── 1. Comprendre l'énoncé
│
│   Objectif :
│   - Identifier ce que l'on cherche à démontrer.
│   - Identifier les questions métier.
│   - Identifier les livrables attendus.
│
│   Fonctions :
│   - Aucune (phase de réflexion)
│
│   Résultat :
│   - Je sais quelles analyses produire.
│
├── 2. Explorer les données
│
│   Objectif :
│   - Comprendre le dataset.
│
│   Fonctions :
│
│   df.head()
│   df.tail()
│   df.sample()
│   df.info()
│   df.describe()
│   df.shape
│   df.columns
│   df.dtypes
│   df.isnull().sum()
│   df.duplicated().sum()
│
│   Questions :
│   - Quelles sont les colonnes ?
│   - Quels sont les types ?
│   - Y a-t-il des valeurs manquantes ?
│   - Quelle est la taille du dataset ?
│
│   Résultat :
│   - Je connais mes données.
│
├── 3. Nettoyer les données
│
│   Objectif :
│   - Corriger les problèmes détectés.
│
│   Fonctions :
│
│   dropna()
│   fillna()
│   replace()
│   astype()
│   drop_duplicates()
│   to_datetime()
│
│   Résultat :
│   - Dataset propre et exploitable.
│
├── 4. Comprendre l'histoire racontée par les données
│
│   Objectif :
│   - Observer les tendances.
│
│   Fonctions :
│
│   plt.plot()
│   sns.lineplot()
│   plt.scatter()
│   sns.scatterplot()
│   plt.bar()
│   sns.barplot()
│
│   Questions :
│   - Le prix augmente-t-il ?
│   - Le volume augmente-t-il ?
│   - Y a-t-il des pics ?
│   - Y a-t-il des anomalies ?
│
│   Résultat :
│   - Première compréhension du comportement.
│
├── 5. Analyse descriptive
│
│   Objectif :
│   - Résumer les données numériquement.
│
│   Fonctions :
│
│   mean()
│   median()
│   mode()
│   min()
│   max()
│   std()
│   var()
│   quantile()
│   describe()
│
│   Questions :
│   - Quelle est la valeur moyenne ?
│   - Quelle est la dispersion ?
│   - Les données sont-elles stables ?
│
│   Résultat :
│   - Description quantitative du dataset.
│
├── 6. Analyse des relations
│
│   Objectif :
│   - Comprendre les liens entre variables.
│
│   Fonctions :
│
│   corr()
│   np.corrcoef()
│   sns.heatmap()
│   sns.pairplot()
│
│   Questions :
│   - Existe-t-il une corrélation ?
│   - Les variables évoluent-elles ensemble ?
│
│   Résultat :
│   - Identification des relations importantes.
│
├── 7. Répondre aux questions statistiques
│
│   Objectif :
│   - Vérifier des hypothèses.
│
│   Fonctions :
│
│   scipy.stats.ttest_ind()
│   scipy.stats.ttest_rel()
│   scipy.stats.chi2_contingency()
│   scipy.stats.f_oneway()
│
│   Exemple :
│
│   H0 :
│   Les moyennes sont égales.
│
│   H1 :
│   Les moyennes sont différentes.
│
│   Décision :
│
│   p < 0.05
│   → Rejet de H0
│
│   p > 0.05
│   → H0 conservée
│
│   Résultat :
│   - Réponse statistiquement justifiée.
│
├── 8. Tester les hypothèses du dataset
│
│   Objectif :
│   - Vérifier les conditions statistiques.
│
│   Fonctions :
│
│   scipy.stats.shapiro()
│   scipy.stats.normaltest()
│   scipy.stats.kstest()
│
│   Questions :
│   - Les données suivent-elles une loi normale ?
│
│   Résultat :
│   - Compréhension statistique approfondie.
│
├── 9. Analyse avancée
│
│   Objectif :
│   - Aller plus loin.
│
│   Fonctions NumPy :
│
│   np.mean()
│   np.median()
│   np.std()
│   np.var()
│   np.percentile()
│   np.convolve()
│   np.corrcoef()
│
│   Fonctions Pandas :
│
│   rolling()
│   expanding()
│   ewm()
│
│   Fonctions SciPy :
│
│   signal.savgol_filter()
│   signal.find_peaks()
│
│   Questions :
│
│   - Quelle est la tendance de fond ?
│   - Peut-on lisser le bruit ?
│   - Quels sont les pics importants ?
│
│   Résultat :
│   - Analyse plus approfondie.
│
├── 10. Interpréter les résultats
│
│   Objectif :
│   - Transformer les chiffres en insights.
│
│   Exemple :
│
│   Mauvais :
│   "La moyenne vaut 105."
│
│   Bon :
│   "Le prix moyen observé est de 105 $,
│   ce qui indique une valorisation élevée."
│
│   Résultat :
│   - Compréhension métier.
│
├── 11. Résumer les insights
│
│   Exemple :
│
│   - Tendance haussière
│   - Forte volatilité
│   - Rendements non normaux
│   - Corrélation faible
│   - Différences significatives
│
│   Résultat :
│   - Réponse claire aux objectifs.
│
└── 12. Conclusion et réflexion
    │
    ├── Difficultés rencontrées
    ├── Solutions apportées
    ├── Ce que j'ai appris
    └── Pistes d'amélioration
    │
    └── END PROJECT