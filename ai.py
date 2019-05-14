import cherrypy
import sys
import copy
import random

class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        
        body = cherrypy.request.json
        #print(body)
        
        response = self.AI(body)
        
        return response
    

    def AI(self, body): 
        InfoGrille = self.InfoBody(body)
        state= InfoGrille[0]                   # Liste qui contient toutes les valeurs de ma grille (1|O|None)
        Jsymbol = InfoGrille[1]                   # Liste qui contient toutes les coups joués
        symbolAdv = InfoGrille[2]                 # Liste qui contient mon nom et celui de mon adversaire
        moves = InfoGrille[3] 
        print("moves")
        print(moves)
        #Score initiaux:
        JBestScore = self.BestScoredelaGrille(state, Jsymbol)
        AdvBestScore = self.BestScoredelaGrille(state, symbolAdv)
        
        #Coups possibles:
        CoupAttaque = self.MeilleurcoupAttaque(state, Jsymbol, symbolAdv)    #{case:direction}
        CoupDefense = self.MeilleurcoupDefense(state, Jsymbol, symbolAdv)    #{case:direction}

        #Faire un choix:
        if AdvBestScore >=3: 
            coup = CoupDefense
            self.message= "je defend" 
        else : 
            coup = CoupAttaque
            self.message= "j'attaque" 
        # Renvoyer le choix sous le bon format :
        cube = list(coup.keys())[0]
        direction = list(coup.values())[0]
        
        response =  {
	        "move": {
                "cube": cube,
                "direction": direction
	        },
	        "message": self.message }
        
        return response

    
    def InfoBody(self, body): #Vérifié , ca fonctionne, il faut mettre les sorties en liste et les récuperer une par une
        "Cette fonction est identique à Infobody  mais peut etre utiliser pour les étapes transitoires #recursivitée "
        Lbody = list(body.values())       # Liste des valeurs de mon body(etatdeLaGrille,LesCoupsPrécedents,2players, Moi)
        state = Lbody[0]                   # Liste de toutes les valeurs de ma grille 
        coups = Lbody[1]                   # Liste de tous les coups joués
        players = Lbody[2]                 # Liste de mon nom et celui de mon adversaire
        Me = Lbody[3]  

        if Me==players[0]:
          Jsymbol = 0 
          symbolAdv = 1                     #je joue avec le symbole O

        elif Me==players[1]:                       
          Jsymbol = 1                       #je joue avec le symbole X
          symbolAdv = 0

        resultat = state, Jsymbol, symbolAdv , coups
        return resultat

     
    def playableCases(self, Istate, Jsymbol): #Vérifié , elle fonctionne #Renvois une liste de cases
        "définit les cases du contour jouables, à partir de l'etat du jeux et de mon symbol"
        playableCases = []
        Indxsides = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24]
        for i in Indxsides:
            if Istate[i] == Jsymbol or Istate[i] == None :
                playableCases.append(i)
            else :
                pass
        return playableCases  #Renvois la liste des cases jouables
    

    def directionsJouables(self, case) :  #Vérifié Validié    #renvoit une lsite
        "renvoit les directions que l'on peut jouer quand on est sur une certaine case"
        #lesdirections = ['N', 'S', 'E', 'W']
        #les directions interditent à certaines cases
        angles = [0, 4, 20, 24]                                 #J'ai mis les angles apart
        E = [9, 14, 19]
        W = [5, 10, 15]
        N = [1, 2, 3]
        S = [21, 22, 23]
        #Les direction jouables par chaque case 
        if case in angles :
            if case ==0 :
                c = ["E", "S"]
            if case ==4 :
                c = ["W", "S"]
            if case ==20 :
                c = ["N", "E"]
            if case ==24 :
                c = ["N", "W"] 
        elif case in E:
            c = ["W", "N", "S"]
        elif case in W :
            c = ["E", "N", "S"]
        elif case in N:
            c = ["E", "W", "S"]
        elif case in S :
            c = ["E", "W", "N"]
        else:
            c = None
        return c 
   

    def JoueurDeCoup(self, Istate, dicoCoup, Jsymbol):  #Vérifié, fonctionne #je peux le modifier de maniere a ce qu'il prennent un coup dico en entrée {case: direction}
        "A partir d'un etat initial et d'un coup, renvoit un nouvel etat"
        case = list(dicoCoup.keys())[0]
        D = list(dicoCoup.values())[0]
        Fstate = copy.deepcopy(Istate)
        
        idxlignes = [0, 1, 2, 3, 4], [ 5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]
        idxcolonnes = [0, 5, 10, 15, 20],[1, 6, 11, 16, 21], [2, 7, 12, 17, 22], [3, 8, 13, 18, 23], [4, 9, 14, 19, 24]
        
        def chercheALign(case, typeAlign):
            for a in typeAlign:
                for valeur in a: 
                    if valeur == case :
                        Aligne = a
                        return Aligne
            
        if D =="E" :
            Alignement = chercheALign(case, idxlignes)
            idxF = 4                        
            idxI = Alignement.index(case)
            movedcases = Alignement[idxI :5]   #je prend les cases influencé par le coup            
            mainmove = Alignement[idxF] - Alignement[idxI]
            othersmove = -1
        
        elif D =="W":
            Alignement = chercheALign(case, idxlignes)
            idxF = 0
            idxI = Alignement.index(case)
            movedcases = Alignement[0 :idxI+1]
            mainmove = Alignement[idxF] - Alignement[idxI]
            othersmove = 1
        
        elif D =="N":
            Alignement = chercheALign(case, idxcolonnes)
            idxF = 0 
            idxI =  Alignement.index(case)
            movedcases = Alignement[0 :idxI+1]
            mainmove = Alignement[idxF] - Alignement[idxI]
            othersmove = 5
       
        elif D =="S" :
            Alignement = chercheALign(case, idxcolonnes)   
            idxF = 4                                #la derniere case de l'alignement
            idxI = Alignement.index(case)                       #la case 
            movedcases = Alignement[idxI :5]
            mainmove = Alignement[idxF] - Alignement[idxI]  #je calcul la varition d'index de la case du coup
            othersmove = -5
        
        for c in movedcases : # chaque élement de notre alignement 
            if c != case :     #s'il n'est pas la case, je garde en mémoir sa valeur, je lui change d'index
                val = Istate[c]
                Newidx = c + othersmove
                Fstate[Newidx] = val
            elif c == case :     #s'il est pas la case, je le met à mon signe, je lui fait changer d'index
                val = Jsymbol
                Newidx = c + mainmove
                Fstate[Newidx] = val
        
        return Fstate
   
   
    def NouvelEtatPourcoup( self, Istate, case, D, Jsymbol):  #Vérifié, fonctionne  # Renvoit une liste state  #je peux le modifier de maniere a ce qu'il prennent un coup dico en entrée {case: direction}
        "A partir d'un etat initial et d'un coup, renvoit un nouvel etat"
        if D =="E":
            mainmove = 4 
            others = 1
            othersmove = -1
        if D =="W":
            mainmove = -4 
            others = -1
            othersmove = 1
        if D =="N":
            mainmove = -20
            others = -5
            othersmove = 5
        if D =="S" :
            mainmove = 20
            others = 5
            othersmove = -5
        
        # Je copie la liste qi contient toutes les valeurs de mes cases 
        Fstate = copy.deepcopy(Istate)   # C'est un body transitoire dont l'intéret est seulement d'extraire des élements
        
        # Mes index initiaux :
        X = case              # x est l'index de notre case
        T = X + others       
        U = X + (2*others)
        V = X + (3*others)    # index des case à coté de la case que je vais déplacer
        W = X + (4*others)

        #Mes index finaux : 
        NX = X + mainmove     # xNew est l'index de ou notre case aprés deplacement
        NT = T + othersmove     
        NU = U + othersmove 
        NV = V + othersmove
        NW = W + othersmove

        # Les valeurs initiales de mes cases:
        valX = Jsymbol                  # Je stoque les signes (X|O|none) initiaux de chacune de mes cases  
        valT = Istate[T]
        valU = Istate[U]
        valV = Istate[V]
        valW = Istate[W]

        # j'injecte dans les valeurs initiales de mes cases dans leurs nouveaux emplaments:
        Fstate[NX] = valX
        Fstate[NT] = valT
        Fstate[NU] = valU
        Fstate[NV] = valV
        Fstate[NW] = valW

        return(Fstate)
    
    
    def BestScoredelaGrille(self, state, Jsymbol):    #Vérifié        #Renvoit le meilleur score d'un etat par rapport à un joueur
        "Cette fonction évalue qu'elle ligne, colonne ou diagonale est la plus proche de la victoire"
        # state est la liste de tous les élements qui sont sur ma grille
        #je découpe ma lsite de données en lignes symboles et colonnes

        lignes = [state[0:5], state[5:10], state[10:15], state[15:20], state[20:25]]  
        colonnes = [state[0:21:5], state[1:22:5], state[2:23:5], state[3:24:5], state[4:25:5]]
        diagonales = [[state[0],state[6],state[12],state[18],state[24]], [state[20],state[16],state[12],state[8],state[4]]]
        
        alignements = lignes + colonnes + diagonales
    
    
        #Dicos des meilleurs scores:
        Bscore1 = self.MeilleurscoreI(alignements, Jsymbol)  #liste contenant la liste des meilleurs alignements, et le meilleur score
        return Bscore1
    def MeilleurscoreI(self, alignements,Jsymbol):  #Vérifié   # Sous fonction de BestScoredelaGrille  #donne le meilleur score actuel de ma grille
        "cette fonction permet pour une liste d'allignements d'avoir leur meilleur lignes et leurs scores"
        scoresCombinaisons = {}              #dico de tous les scores du type d'alignements analysés
        combinaison = -1                    
        for combi in alignements:                          #Pour chaque ligne 
            combinaison+= 1                                #J'identifie son index  
            score = self.scoreDealignement(combi, Jsymbol)       #Je calcul son score           
            scoresCombinaisons[combinaison] = score        #J'associe l'index de chaque ligne à son score
                        
        l=0
        for i in scoresCombinaisons.values():              #je détermine mon plus grand score calculé
            if i>=l:                                  
               l=i
            else: 
               pass 
     
        c = -1 
        lignes = []
        for n in scoresCombinaisons.values():     #je retouve la ligne du meilleur score garce à son index
            c += 1
            if n == l :   
                ligne = alignements[c]
                lignes.append(ligne)   
            else :
                pass
        return l 
    def scoreDealignement(self, state, Jsymbol):   #Vérifié  #sous fonction de BestScoredelaGrille
        "Calcul le nombre de fois qu'on retrouve un symbole dans une ligne"
       #combi = les symboles de ma ligne
        score= 0  
        for i in state:                      #je parcours tous les elements de mon alignement
            if i == Jsymbol:                  #si je trouve mon symbole dans la ligne +1pourScore
                score += 1
            else :                               #aussinon passscoreDealignement(self,combi, symbol)
                pass
        return score


    def TrieurDecoups(self, state, Jsymbol, Advsymbol):    
        "fonction qui trie les coups jouables selon leur pertinenece"
        GGcoupsMoi = []         
        StagnecoupsMoi = []     
        BadcoupsMoi = []          
         
        GGcoupsadv = [] 
        Stagnecoupsadv = [] 
        Badcoupsadv = [] 

        playCases = self.playableCases(state, Jsymbol)                  # Prend toutes les cases jouables 
        ImeilleurScoreJ = self.BestScoredelaGrille(state, Jsymbol)                 # Mon meilleur score actuel dans la grille
        ImeilleurScoreadv = self.BestScoredelaGrille(state, Advsymbol)
       #je commence à jouer mes coups
        for c in playCases :                                        #je prends chaque case jouable 
            for d in self.directionsJouables(c):                             #je déplace la case dans l'une des directions autorisés 
                dicoCoup = {c : d}                    
                newState = self.JoueurDeCoup(state, dicoCoup, Jsymbol)     # grace  à mon coup j'obtient un nouvel etat
                NewJScore = self.BestScoredelaGrille(newState, Jsymbol)  #je calcul mon score ou celui de mon adversaire selon si j'attaque ou je défends
                Newscoreadv = self.BestScoredelaGrille(newState, Advsymbol)
                
                
                # De MON POINT DE VUE : 
                if NewJScore > ImeilleurScoreJ  and Newscoreadv !=5:    
                    dico = {}
                    dico[c]=d                          
                    GGcoupsMoi.append(dico)                  # [{case: direction}, {case: direction}, {case: direction}]
                    
                # Si ce coup ne fait pas évoluer mon jeux  je le met dans Stagnecoups 
                elif NewJScore == ImeilleurScoreJ and Newscoreadv !=5 :
                    dico = {}
                    dico[c]=d                          
                    StagnecoupsMoi.append(dico)                  # [{case: direction}, {case: direction}, {case: direction}]

                # Si ce coup fait reculer mon jeux  je le met dans Badcoups
                elif NewJScore < ImeilleurScoreJ and Newscoreadv !=5 :
                    dico = {}
                    dico[c]=d
                    BadcoupsMoi.append(dico)                                              # [{case: direction}, {case: direction}, {case: direction}]

            
                # Du point de vue de mon adversaire : 
                if Newscoreadv > ImeilleurScoreadv and Newscoreadv !=5 :    
                    dico = {}
                    dico[c]=d                          
                    GGcoupsadv.append(dico)                  # [{case: direction}, {case: direction}, {case: direction}]
                    
                # Si ce coup ne fait pas évoluer mon jeux  je le met dans Stagnecoups 
                elif Newscoreadv == ImeilleurScoreadv and Newscoreadv !=5:
                    dico = {}
                    dico[c]=d                          
                    Stagnecoupsadv.append(dico)                  # [{case: direction}, {case: direction}, {case: direction}]

                # Si ce coup fait reculer mon jeux  je le met dans Badcoups
                elif Newscoreadv <ImeilleurScoreadv and Newscoreadv !=5:
                    coup = {}
                    coup[c]=d
                    Badcoupsadv.append(dico)                               # [{case: direction}, {case: direction}, {case: direction}]
        resultatPouradv = [GGcoupsadv, Stagnecoupsadv, Badcoupsadv]       #[[{case: direction}, {case: direction}], [{case: direction}, {case: direction}],[{case: direction}, {case: direction}] ]
        resultatPourMoi = [GGcoupsMoi, StagnecoupsMoi, BadcoupsMoi]       #[[{case: direction}, {case: direction}], [{case: direction}, {case: direction}],[{case: direction}, {case: direction}] ]
        resultat = [resultatPourMoi ,resultatPouradv]
        print(resultat)
        return  resultat  #[   [[], [], []],   [ [],[],[] ]    ]


    def MeilleurcoupAttaque (self, Istate, Jsymbol, symbolAdv):     
        "Permet de faire un choix parmi les coups triers"
        CoupsTrier = self.TrieurDecoups(Istate, Jsymbol, symbolAdv)
        CoupsTrierPourMOi = CoupsTrier[0]                     # [[],[],[]]                  
        CoupsTrierPourAdv = CoupsTrier[1]                     # [[],[],[]]
        
        GGcoupsMoi = CoupsTrierPourMOi[0]         # [{},{},{}]
        StagnecoupsMoi = CoupsTrierPourMOi[1]      # [{},{},{}]
        BadcoupsMoi = CoupsTrierPourMOi[2]         # [{},{},{}]
         
        GGcoupsadv = CoupsTrierPourAdv[0]          # [{},{},{}]
        Stagnecoupsadv = CoupsTrierPourAdv[1]      # [{},{},{}]
        Badcoupsadv = CoupsTrierPourAdv[2]         # [{},{},{}]
        
        TopCoups = []
        Moyenscoups = []
        CoupEvite = []
        resultat = 0


        if len(GGcoupsMoi)!= 0 :             #Si j'ai des coups qui font évoluer mon jeux 
            for coup in GGcoupsMoi :      

                if coup in Badcoupsadv :      #font reculer mon adversaire
                   TopCoups.append(coup)
                elif coup in Stagnecoupsadv:  #n'influence pas mon adversaire
                    Moyenscoups.append(coup)
                elif coup in GGcoupsadv:        #font avancer mon adversaire
                    Moyenscoups.append(coup)

                if len(TopCoups)!=0 :
                    resultat = random.choice(TopCoups)
                elif len(Moyenscoups)!=0 :
                    resultat = random.choice(Moyenscoups)
                elif len(CoupEvite)!=0 :
                    resultat = random.choice(CoupEvite)
               
        elif len(StagnecoupsMoi)!= 0 :        #Si j'ai des coups qui me font stagné
            print("j'ai des StagnecoupsMoi ") 
            for coup in StagnecoupsMoi :        
                if coup in Badcoupsadv :      #font reculer mon adversaire
                   TopCoups.append(coup)
                elif coup in Stagnecoupsadv:  #n'influence pas mon adversaire
                    Moyenscoups.append(coup)
                elif coup in GGcoupsadv:        #font avancer mon adversaire
                    Moyenscoups.append(coup)

                if len(TopCoups)!=0 :
                    resultat = random.choice(TopCoups)
                elif len(Moyenscoups)!=0 :
                    resultat = random.choice(Moyenscoups)
                elif len(CoupEvite)!=0 :
                    resultat = random.choice(CoupEvite)

        elif len(BadcoupsMoi)!= 0 :             #Si j'ai des coups qui font évoluer mon jeux 
            for coup in BadcoupsMoi :        
                if coup in Badcoupsadv :      #font reculer mon adversaire
                   TopCoups.append(coup)
                elif coup in Stagnecoupsadv:  #n'influence pas mon adversaire
                    Moyenscoups.append(coup)
                elif coup in GGcoupsadv:        #font avancer mon adversaire
                    Moyenscoups.append(coup)

                if len(TopCoups)!=0 :
                    resultat = random.choice(TopCoups)
                elif len(Moyenscoups)!=0 :
                    resultat = random.choice(Moyenscoups)
                elif len(CoupEvite)!=0 :
                    resultat = random.choice(CoupEvite)
        return resultat


    def MeilleurcoupDefense(self, Istate, Jsymbol, symbolAdv):     
        "Permet de faire un choix parmi les coups triers"
        CoupsTrier = self.TrieurDecoups(Istate, Jsymbol, symbolAdv)
        CoupsTrierPourMOi = CoupsTrier[0]                     # [[],[],[]]                  
        CoupsTrierPourAdv = CoupsTrier[1]                     # [[],[],[]]
        
        GGcoupsMoi = CoupsTrierPourMOi[0]         # [{},{},{}]
        StagnecoupsMoi = CoupsTrierPourMOi[1]      # [{},{},{}]
        BadcoupsMoi = CoupsTrierPourMOi[2]         # [{},{},{}]
         
        GGcoupsadv = CoupsTrierPourAdv[0]          # [{},{},{}]
        Stagnecoupsadv = CoupsTrierPourAdv[1]      # [{},{},{}]
        Badcoupsadv = CoupsTrierPourAdv[2]         # [{},{},{}]
        
        TopCoups = []
        Moyenscoups = []
        CoupEvite = []
        resultat = 0


        if (len(Badcoupsadv)!= 0) :             #Si j'ai des coups qui font reculer mon adversaire 
            for coup in Badcoupsadv :      
                if coup in GGcoupsMoi:      #font reculer mon adversaire
                   TopCoups.append(coup)
                elif coup in StagnecoupsMoi:  #n'influence pas mon adversaire
                    Moyenscoups.append(coup)
                elif coup in BadcoupsMoi:        #font avancer mon adversaire
                    CoupEvite.append(coup)

                if len(TopCoups)!=0 :
                    resultat = random.choice(TopCoups)
                elif len(Moyenscoups)!=0 :
                    resultat = random.choice(Moyenscoups)
                elif len(CoupEvite)!=0 :
                    resultat = random.choice(CoupEvite)
               
        elif (len(Stagnecoupsadv)!= 0) :        #Si j'ai des coups qui me font stagné 
            for coup in Stagnecoupsadv :        
                if coup in GGcoupsMoi:      #font reculer mon adversaire
                   TopCoups.append(coup)
                elif coup in StagnecoupsMoi:  #n'influence pas mon adversaire
                    Moyenscoups.append(coup)
                elif coup in BadcoupsMoi:        #font avancer mon adversaire
                    CoupEvite.append(coup)

                if len(TopCoups)!=0 :
                    resultat = random.choice(TopCoups)
                elif len(Moyenscoups)!=0 :
                    resultat = random.choice(Moyenscoups)
                elif len(CoupEvite)!=0 :
                    resultat = random.choice(CoupEvite)

        elif (len(GGcoupsadv)!= 0) :             #Si j'ai des coups qui font évoluer mon jeux  
            for coup in GGcoupsadv :        
                if coup in GGcoupsMoi:      #font reculer mon adversaire
                   TopCoups.append(coup)
                elif coup in StagnecoupsMoi:  #n'influence pas mon adversaire
                    Moyenscoups.append(coup)
                elif coup in BadcoupsMoi:        #font avancer mon adversaire
                    CoupEvite.append(coup)

                if len(TopCoups)!=0 :
                    resultat = random.choice(TopCoups)
                elif len(Moyenscoups)!=0 :
                    resultat = random.choice(Moyenscoups)
                elif len(CoupEvite)!=0 :
                    resultat = random.choice(CoupEvite)
        return resultat 

        
    
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8008 #c'etait 8080 mais le mien etait buzzy

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())







    