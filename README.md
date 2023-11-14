# Flappy Plane
![Icon](doc/res/Icon.png)
Un jeu d'esquive d'obstacle où les joueurs doivent programmer leurs propres robots !
### 🎯 Contexte & cahier des charges :
Développé dans le cadre d'une formation, le flappy plane doit être un nouveau mode de jeu pour PytactX (voir [jusdeliens.com](https://jusdeliens.com)) et permettre au groupe de monter en compétences en python en mettant en pratique les principes SOLID.
![Playground](doc/Playground.png)
### 🎲 Règles du jeu :
Les joueurs rejoignent la carte et doivent esquiver les différents obstacles, il est possible de gêner les autres joueurs en se mettant devant eux.
Si un joueur est touché par un obstacle, il meurt et obtient alors un score en fonction final correspondant au nombre d'obstacles passés.
![Rules](doc/Rules-1.png)
### 🎮 Use cases :
#### Administrateur : 
- L'administrateur peut configurer l'arène via le fichier d'options.
#### Joueur :
- Si vous êtes un joueur, référez vous au [README_API](api/README_API.md)
## 📞 Diagramme de séquence :
expliquer le déroulé d'une partie, les principales étapes à faire dans l'ordre et qui/quoi/comment, les couches s'échangent quelles données pour qui/pour quoi, et l'architecture matérielle
## ✅ Pré-requis
En tant qu'administrateur vous aurez besoin de python 3.12 pour éxécuter le projet.
Si vous voulez faire votre propre robot pour jouer au jeu, consultez [le read me de l'API](api/README_API.md) à la place
## ⚙️ Installation :
step by step (commandes à executer par l'administrateur, paquets à installer ...)
## 🧪 Tests:
définition du plan de test ce qu'on attend quand on fait quoi
step by step pour lancer les tests
## 🛣️ Roadmap
- [ ] Jeu de base en FFA continu
- [ ] Manches
- [ ] Mode Battle Royale
- [ ] Equipes
- [ ] Collectables
## 🧑‍💻 Auteurs
- Augustin BUKIN ([Nehocute](https://github.com/Nehocute))
- Théo LEBIEZ ([Deeffault](https://github.com/Deeffault))
- Teiva TESSON ([teidova](https://github.com/teidova))
- Samy VASSE ([samy313](https://github.com/samy313))
## Dépendances
- librairie j2l (auteur: [jusdeliens.com](https://jusdeliens.com))
## ⚖️ License

Background images by vectorpocket on Freepik : 
<a href="https://www.freepik.com/free-vector/background-with-night-city-neon-lights_3586829.htm?query=city%20towers#from_view=detail_alsolike">bg1</a>,  <a href="https://www.freepik.com/free-vector/background-with-night-city-neon-lights_3586319.htm?query=city%20towers#from_view=detail_alsolike">bg2</a> & <a href="https://www.freepik.com/free-vector/neon-megapolis-background-with-buildings-skyscrapers_3586320.htm?query=city%20towers#from_view=detail_alsolike">bg3</a> 

MIT License

Copyright (c) 2023 Augustin BUKIN, Théo LEBIEZ, Teiva TESSON, Samy VASSE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.