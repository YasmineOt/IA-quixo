# AI Quixo

## Règles

[https://www.gigamic.com/files/catalog/products/rules/quixo_rule-fr.pdf](https://www.gigamic.com/files/catalog/products/rules/quixo_rule-fr.pdf)

## Intelligence Artificielle

## Strategie de notre IA: 

Notre joueur a pour but d'analyser le nombre de ligne où il a le plus de chance de gagner. Il choisis d'abord la stratégie d'attaque en fonction de son adversaire. Si ce dernier a plus ou 3 cube aligné, on va défendre. Dans le cas contraire on va attaquer. 
Lorsque l'état du jeu est envoyé, il joue le coup le plus avantageux. S'il n'y a pas de coups avantgeux, il joue au hasard(random).
Le meilleur coup est choisi en fonction du nombre de cube qu'on a sur nos lignes. Notre ai va calculer chaque cube de chaque ligne et colonne et va jouer sur la ligne où le score est gagnant. 

## Exigences: 
Pour que le coup soit joué, il ne faut pas que notre coup avantage notre adversaire. Dans ce cas-là, il joue une autre ligne(ou colonne ou diagonale). 
Si le coup joué fait reculer le jeu, c'est un mauvais coup. 
