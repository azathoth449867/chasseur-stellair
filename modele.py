import random

# ------------------ CLASSES ------------------

class Projectile:
    def __init__(self, x, y, typeBullet):
        self.x = x
        self.y = y
        self.vitesse = -10  # vers le haut
        self.dommage = 5 # dommange de base
        self.taille_x = 2
        self.taille_y = 10
        self.goodBad = typeBullet
        self.alive = True

        if self.goodBad == "b":
            self.vitesse = 10

    def mise_a_jour(self):
        self.y += self.vitesse

class Vaisseau:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 3
        self.projectiles = []
        self.taille_x = 15
        self.taille_y = 15
        self.hp = 10
        self.dommage_collision = 20

    def deplacer(self, x, y):
        self.x += (x - self.x) * 0.14
        self.y += (y - self.y) * 0.14
        
    def tirer(self):
        nouveau_proj = Projectile(self.x, self.y - 20, "g")
        self.projectiles.append(nouveau_proj)

    def mise_a_jour(self):
        for p in self.projectiles:
            p.mise_a_jour()

        self.projectiles = [
            p for p in self.projectiles
            if p.y > 0 and p.alive
        ]

class OVNI:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.projectiles = []
        self.taille_x = 12
        self.taille_y = 15
        self.hp = 10
        self.dommage_collision = 5

    def tirer(self):
        nouveau_proj = Projectile(self.x, self.y + 20, "b")
        self.projectiles.append(nouveau_proj)

    def mouvement_projectile(self):
        for p in self.projectiles: 
            p.mise_a_jour()

    def mise_a_jour(self):
        self.y += self.vy
        self.projectiles = [
                    p for p in self.projectiles
                    if p.y < 700 and p.alive
                ]
        
class Asteroide:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.taille_x = 12
        self.taille_y = 12
        self.hp = 20
        self.dommage_collision = 5

    def mise_a_jour(self):
        self.y += self.vy

# ------------------ MODÈLE ------------------

class Modele:
    def __init__(self, parent, largeur, hauteur):
        self.parent = parent
        self.largeur = 600
        self.hauteur = 700
        self.vaisseau = Vaisseau(self.largeur // 2, self.hauteur - 50)
        self.ovnis = []
        self.asteroides = []
        self.score = 0
        self.niveau = 1
        self.round = 1
        self.frames = 0
        self.apparationRate = 0.02
        self.souris_x, self.souris_y = 300, 600
        self.tire = None
        self.enPause = False
        self.pauseCompteur = 0
        self.chronometre = None

    def deplacer_vaisseau(self,x, y):
        self.souris_x, self.souris_y = x, y
    def tirer(self):
        self.vaisseau.tirer()
    def incrementer_jeu(self):
        self.frames += 1 * 0.03
        if self.frames >= 3:
            self.frames = 0
            self.round += 1
            print("round: ", self.round)
            self.prochaine_round()
        if self.round > 3:
            self.round = 1
            self.niveau += 1
            print("niveau:", self.niveau)
            self.prochain_niveau()
        self.apparationRate = 0.02 * (self.round * 0.5 + self.niveau)
    
    def pause_compteur(self):
        self.pauseCompteur += 1 * 0.03
        print(self.pauseCompteur)
    
    def prochaine_round(self):
        self.enPause = True
        self.parent.afficher_intervalle("round")
        
    def prochain_niveau(self):
        self.enPause = True
        self.parent.afficher_intervalle("niveau")
        
    
    def mise_a_jour(self):
        self.vaisseau.mise_a_jour()
        self.incrementer_jeu()
        #Verifie si projectile vaisseau touche ovnis
        for p in self.vaisseau.projectiles:
            if p.goodBad == "g":
                for o in self.ovnis:
                    if (p.x <= o.x + o.taille_x and 
                        p.x >= o.x - o.taille_x):
                            if p.y - p.taille_y <= o.y + o.taille_y:
                                o.hp -= p.dommage #hp ovnis - dommage projectile
                                print("hp ovnis" , o.hp)
                                p.alive = False

        #Vérifie si projectile ovnis touche vaisseau
        for o in self.ovnis:
            for p in o.projectiles:
                        if (p.x <= self.vaisseau.x + self.vaisseau.taille_x and 
                            p.x >= self.vaisseau.x - self.vaisseau.taille_x):
                                if p.y + p.taille_y >= self.vaisseau.y - self.vaisseau.taille_y:
                                    p.alive = False
                                    self.vaisseau.hp -= p.dommage #hp vaisseau - dommage projectile
                                    print("hp vaisseau" , self.vaisseau.hp)

        #Verifie si projectile vaisseau touche asteroides
        for p in self.vaisseau.projectiles:
            if p.goodBad == "g":
                for a in self.asteroides:
                    if (p.x <= a.x + a.taille_x and 
                        p.x >= a.x - a.taille_x):
                            if p.y - p.taille_y <= a.y + a.taille_y:
                                a.hp -= p.dommage #hp asteroides - dommage projectile
                                print("hp asteroide" , a.hp)
                                p.alive = False

        #Vérifie si ovnis touche vaisseau
        for o in self.ovnis:
            if (o.x + o.taille_x >= self.vaisseau.x - self.vaisseau.taille_x and 
                o.x - o.taille_x <= self.vaisseau.x + self.vaisseau.taille_x):
                if (o.y + o.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and
                    o.y - o.taille_y <= self.vaisseau.y + self.vaisseau.taille_y):
                        o.hp -= self.vaisseau.dommage_collision
                        print("ovni hp", o.hp)
                        self.vaisseau.hp -= o.dommage_collision
                        print("vaisseau hp", self.vaisseau.hp)

        #Vérifie si vaisseau touche astéroides
        for a in self.asteroides:
            if (a.x + a.taille_x >= self.vaisseau.x - self.vaisseau.taille_x and 
                a.x - a.taille_x <= self.vaisseau.x + self.vaisseau.taille_x):
                if (a.y + a.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and
                    a.y - a.taille_y <= self.vaisseau.y + self.vaisseau.taille_y):
                        a.hp -= self.vaisseau.dommage_collision
                        print("asteroides hp", a.hp)
                        self.vaisseau.hp -= a.dommage_collision
                        print("vaisseau hp", self.vaisseau.hp)

        # Vaisseau déplace vers souris même sans mouvement de souris
        self.vaisseau.deplacer(self.souris_x, self.souris_y)
                
        # Apparition aléatoire des ennemis
        alea_ovni = random.random()
        if alea_ovni < self.apparationRate:
            nouvel_ovni = OVNI(
                random.randint(0, self.largeur),
                0,
                random.randint(2, 5)
            )
            self.ovnis.append(nouvel_ovni)

        alea_asteroide = random.random()
        if alea_asteroide < 0.01:
            nouvel_ast = Asteroide(
                random.randint(0, self.largeur),
                0,
                random.randint(3, 6)
            )
            self.asteroides.append(nouvel_ast)

        # Déplacement des ennemis
        for o in self.ovnis:
            o.mise_a_jour()

        for a in self.asteroides:
            a.mise_a_jour()

        # Les ennemis tirent
        for o in self.ovnis:
            alea_frequence = random.random()
            if alea_frequence < 0.02:
                o.tirer()
    
        for o in self.ovnis:
            o.mouvement_projectile()

        # Nettoyage des objets sortis de l'écran
        self.ovnis = [
            o for o in self.ovnis
            if o.y < self.hauteur and o.hp > 0
        ]

        self.asteroides = [
            a for a in self.asteroides
            if a.y < self.hauteur and a.hp > 0
        ]

