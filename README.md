# AI Quixo 

## Règles

[https://www.gigamic.com/files/catalog/products/rules/quixo_rule-fr.pdf](https://www.gigamic.com/files/catalog/products/rules/quixo_rule-fr.pdf)

## L'ntelligence Artificielle YALA:

YALA est une intelligence artificielle jouant au jeu quixo.
Elle a la capacité de lire et d'analyser l'état du jeu, et de choisir en conséquence entre une stratégie d'attaque ou de défense qui, quoi qu'il en soit sera optimisée au maximum, pour être la plus avantageuse possible.

## Strategie de notre IA: 

Notre stratégie repose sur l'idée que dans un jeu à deux joueurs, si notre adversaire ne peut pas gagner, alors de notre côté nous ne pouvons pas perdre, et donc nous ne pouvons que gagner.

Chaque fois que notre IA doit renvoyer un coup, cette dernière commence par:
-rechercher toutes les cases qu'il lui est permis des joueurs.
-Rechercher les directions qu'elle peut jouer avec chaque case.
Ensuite dans un second temps, notre IA, se projète en jouant chaque coup possible et en évaluant la variation de la grille qu'il génère, et trie en conséquence tous les coups dans trois listes qui la concernent et qui sont :
une liste de coups qui lui sont favorables, une liste de coups qui font stagner son score, et une liste de coup qui font reculer son score.
Et en parrallel elle trie aussi ces coups dans trois listes qui concernent son adversaire et qui sont :
une liste de coup qui fait reculer le jeu de mon adversaire, une liste de coup qui n'influence pas son adversaire, et enfin une liste de coup qui fait gagner son adversaire.
Ensuite notre ia, revient a l'état réel de la grille (état que le serveur nous a envoyé), et décide s'il serait plus judicieux d'attaquer ou de défendre, et pour cela elle se base simplement sur le score de la meilleure ligne de son adversaire, si cette dernière à un alignement de plus ou égale trois élement, notre ia défend, et cela dans tous les cas, sauf si mon score est de 4 et que je peux gagner en un coup, et dans ce cas mon IA va plutôt attaquer quel que soit le score de l'adversaire car elle est sure de gagner quoi qu'il en soit.


## fonctionnement de l'attaque et de  la défense: 

Les stratégies de notre IA sont donc attaque ou défense, néanmoins, ces deux dernières sont fort semblables dans le raisonnement, seule la priorité numéro 1 change.

Pour être plus claire, lorsque notre IA est en attaque, elle commence par chercher dans les coups qui la concernent ceux qui lui sont le plus favorable, si elle en trouve un seul elle le joue; mais si elle en trouve plusieurs alors la priorité sera tel qu'il suit:

1- Coup qui font évoluer mon score ET reculer celui de mon adversaire.

2- Coup qui font évoluer mon score ET stagner celui de mon adversaire.

3- Coup qui font évoluer mon score mais augmente le score de mon adversaire.

( il est facile de deviner la suite des priorités, si je n'ai pas de bon coup pour moi, se sera comme vu ci-dessus mais en remplaçant coup favorable par coup qui me stagné, et même chose pour les coups qui me font reculer).
Tandis que dans le cas de la position de défense, les trois premières priorités seront les suivantes:
1 - coup défavorable pour mon adversaire ET à mon avantage

 2 - Coup défavorable pour mon adversaire ET qui n'influence pas mon score.

3 - Coup défavorable pour mon adversaire et défavorable pour moi.

(Comme pour l'attaque, il est aisé de deviner la suite.)
Néanmoins, un cas reste non couvert par ce que je viens de citer, et c'est le cas ou par exemple: l'IA trouverait plusieurs coups qui augmentent mon score et qui désavantagent mon adversaire:
la réponse est RANDOM, car dans notre raisonnement, si deux coups influence exactement de la même manière les scores des joueurs alors ils n'ont aucune différence notable


## Avantages et inconvénients de la stratégie de notre IA : 
 laya
Si nous reprenons la phrase avec laquelle nous avons commencé ce document et qui était : 
"notre stratégie repose sur l'idée que dans un jeu à deux joueurs, si notre adversaire ne peut pas gagner, alors de notre côté nous ne pouvons pas perdre, et donc nous ne pouvons que gagner".

Eh bien ce raisonnement n'est pas complétement correct, car "Yala" ne perd presque jamais dû à son extrême vigilance, mais d'autre part face à une IA adverse qui a un raisonnement similaire, YALA fait presque toujours match nul, et elle finit toujours par se retrouver dans une boucle infinie lorsqu'elle joue contre elle-même .

Néanmoins, LAYA a la particularité d'être toujours très pertinente dans son jeu, car elle ne recourt à Random qu'après avoir sélectionné les meilleurs coups possibles, de plus, vu qu'elle ne repose pas sur des fonctions récursives et une lecture profonde de jeux, elle arrive à jouer de très bons coups un très peu de temps, et ceux quelle que soit la complexité de la situation.

Pour conclure, YALA est une IA rapide, efficace et pertinent, elle pourrait être améliorée en travaillant sur sa capacité à sortir intelligemment d'une boucle de coups infini.
 
