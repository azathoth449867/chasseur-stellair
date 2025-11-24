import random

# ------------------ CLASSES ------------------

class Projectile:
    def __init__(self, x, y, typeBullet):
        self.x = x
        self.y = y
        self.vitesse = -10  # vers le haut
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

    def deplacer(self, x, y):
        self.x += (x - self.x) * 0.09
        self.y += (y - self.y) * 0.09
        
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
        self.taille_y = 6

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
        self.taille_x = 10
        self.taille_y = 10

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
        self.souris_x, self.souris_y = 0, 0

    def deplacer_vaisseau(self,x, y):
        self.vaisseau.deplacer(x, y)
        self.souris_x, self.souris_y = x, y
    def tirer(self):
        self.vaisseau.tirer()
    def mise_a_jour(self):
        self.vaisseau.mise_a_jour()
        
        for p in self.vaisseau.projectiles:
            if p.goodBad == "g":
                for o in self.ovnis:
                    if p.x <= o.x + o.taille_x and p.x >= o.x - o.taille_x:
                        if p.y - p.taille_y <= o.y + o.taille_y:
                            p.alive = False

        for o in self.ovnis:
            for p in o.projectiles:
                        if p.x <= self.vaisseau.x + self.vaisseau.taille_x and p.x >= self.vaisseau.x - self.vaisseau.taille_x:
                            if p.y + p.taille_y >= self.vaisseau.y - self.vaisseau.taille_y:
                                p.alive = False
                                print("1")

        # Vaisseau déplace vers souris même sans mouvement de souris
        self.vaisseau.deplacer(self.souris_x, self.souris_y)
                
        # Apparition aléatoire des ennemis
        alea_ovni = random.random()
        if alea_ovni < 0.02:
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
            if o.y < self.hauteur
        ]

        self.asteroides = [
            a for a in self.asteroides
            if a.y < self.hauteur
        ]

