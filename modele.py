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
    def appliquer_degat(self, target):
        if hasattr(target, 'bouclier'):
            # target est le vaisseau
            if target.bouclier > 0:
                target.bouclier -= 1
            else: 
                target.hp -= self.dommage
            return
        target.hp -= self.dommage

class Vaisseau:
    def __init__(self,parent, x, y):
        self.x = x
        self.y = y
        self.vie = 3
        self.projectiles = []
        self.taille_x = 15
        self.taille_y = 15
        self.hp = 30
        self.maxHp = 30
        self.dommage_collision = 20
        self.bouclier = 0
        self.invincible = False
        self.parent = parent

    def deplacer(self, x, y):
        self.x += (x - self.x) * 0.14
        self.y += (y - self.y) * 0.14
        
    def tirer(self):
        nouveau_proj = Projectile(self.x, self.y - 20, "g")
        self.projectiles.append(nouveau_proj)

    def mise_a_jour(self):
        if self.hp <= 0:                                #######################################################
            self.vie -=1
            self.hp = self.maxHp
            self.parent.invincibilite()

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
        
class Boss:
    def __init__(self, vx, taille_x, taille_y, hp):
        self.x = 300
        self.y = 50
        self.vx = vx
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.projectiles = []
        self.hp = hp
        self.dommage_collision = 100
        self.attackFrequence = 0
        self.estVivant = True
        self.enTire = True

    def tirer(self):
        nouveau_proj = Projectile(self.x, self.y + 20, "b")
        self.projectiles.append(nouveau_proj)
    def mouvement_projectile(self):
        for p in self.projectiles: 
            p.mise_a_jour()
    def mise_a_jour(self):
        self.x += self.vx
        if self.hp <= 0: # check état de vie
            self.estVivant = False
        if self.x >= 500 or self.x <= 100:
            self.vx = -self.vx
        self.projectiles = [
                    p for p in self.projectiles
                    if p.y < 700 and p.alive
                ]

class DoubleCannon(Boss):
    def __init__(self):
        super().__init__(3, 20, 30, 20)
        
    def tirer(self):
        nouveau_proj = Projectile(self.x, self.y + 20, "b")
        self.projectiles.append(nouveau_proj)
        
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

class Ressource:
    def __init__(self, vaisseau, x, vy):
        self.x = x
        self.y = -5
        self.vy = vy
        self.taille_x = 12
        self.taille_y = 12
        self.vaisseau = vaisseau
        self.alive = True
    
    def mise_a_jour(self):
        self.y += self.vy
    def contact_vaisseau(self):
        self.alive = False
        self.appliquer_buff()
    def appliquer_buff(self):
        pass

class Bouclier(Ressource):
    def __init__(self, vaisseau, x):
        super().__init__(vaisseau, x, 0.75)
    def appliquer_buff(self):
        self.vaisseau.bouclier += 1

# ------------------ MODÈLE ------------------

class Modele:
    def __init__(self, parent, largeur, hauteur):
        self.parent = parent
        self.largeur = 600
        self.hauteur = 700
        self.vaisseau = Vaisseau( self ,self.largeur // 2, self.hauteur - 50)
        self.boss = None
        self.ovnis = []
        self.asteroides = []
        self.ressources = []
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
        self.vie = 3
        self.game_over = False
        self.boss_id = None
        self.recompense_id = None
        self.estCommence = False
        
        
        
    def invincibilite(self):
        self.vaisseau.x = self.largeur // 2
        self.vaisseau.y = self.hauteur - 50
        self.conteur_invincibilite = 0
        self.vaisseau.invincible = True

    def deplacer_vaisseau(self,x, y):
        self.souris_x, self.souris_y = x, y
    def tirer(self):
        self.vaisseau.tirer()
    def incrementer_jeu(self):
        self.frames += 1 * 0.03
        if(self.vaisseau.invincible):
            if self.conteur_invincibilite >= 2:
                self.vaisseau.invincible = False
                print(self.vaisseau.invincible)
            self.conteur_invincibilite += 1 * 0.03
            print(self.vaisseau.invincible)
            
        
        if self.boss == None:
            if self.frames >= 10:                   # Temp entre chaque vague
                self.frames = 0
                self.round += 1
                self.prochaine_round()
        if self.round > 3:
            if self.boss == None:
                self.boss = self.creer_boss(self.boss_id)
                self.apparationRate = 0
            if self.boss.estVivant == False:
                self.score += 10
                self.appliquer_recompense(self.recompense_id)
                self.prochain_niveau()
                    
    def pause_compteur(self):
        self.pauseCompteur += 1 * 0.03
    
    def prochaine_round(self):
        self.enPause = True
        self.apparationRate = 0.02 * (self.round * 0.5 + self.niveau)
        
    def prochain_niveau(self):
        self.boss = None
        self.round = 1
        self.niveau += 1
        self.enPause = True
        self.boss_id = None
        self.boss_od = None
        self.vaisseau.hp = self.vaisseau.maxHp # vaisseau regagne hp entre niveau
        print(self.vaisseau.hp,self.vaisseau.maxHp)
        self.vaisseau.projectiles = []
        self.definir_niveau()
        
    def definir_niveau(self):
        self.boss_id = 1 #random.randint(1, ...) pour futur boss et recompense
        self.recompense_id = 1 
        self.estCommence = True
        self.apparationRate = 0.02 * (self.round * 0.5 + self.niveau)

    def appliquer_recompense(self, recompense_id):
        def max_hp():
            self.vaisseau.maxHp += 5

        RECOMPENSES_TYPES = {
            1: max_hp(),
        }
        return RECOMPENSES_TYPES[recompense_id]

    def creer_boss(self, boss_id): # génère un boss aléatoire pour le niveau
        BOSS_TYPES = {
            1: DoubleCannon()
        }
        self.vaisseau.projectiles = [] # vide projectiles existants
        return BOSS_TYPES[boss_id]
    
    def creer_ressource(self, ressource_id, vaisseau):
        x = random.randint(50,550)
        RESSOURCE_TYPES = {
            1: Bouclier(vaisseau, x)
        }
        return RESSOURCE_TYPES[ressource_id]
        
    def mise_a_jour(self):
        self.vaisseau.mise_a_jour()
        self.vie = self.vaisseau.vie
        b = self.boss
        if self.vaisseau.vie == 0:
            self.vaisseau = None       
            self.game_over = True
        if self.vaisseau != None:
            self.incrementer_jeu()

            # Vérifie collisions ressources avec vaisseau
            for r in self.ressources:
                 if (r.x <= self.vaisseau.x + self.vaisseau.taille_x and 
                            r.x >= self.vaisseau.x - self.vaisseau.taille_x):
                                if r.y + r.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and r.y - r.taille_y <= self.vaisseau.y + self.vaisseau.taille_y:
                                    r.contact_vaisseau()
                                    print(self.vaisseau.bouclier)

            #Verifie si projectile vaisseau touche ovnis ou boss
            for p in self.vaisseau.projectiles:
                if p.goodBad == "g":
                    for o in self.ovnis:
                        if (p.x <= o.x + o.taille_x and 
                            p.x >= o.x - o.taille_x):
                                if p.y - p.taille_y <= o.y + o.taille_y:
                                    p.appliquer_degat(o) #hp ovnis - dommage projectile
                                    print(o.hp)
                                    p.alive = False
                    if self.boss != None:
                        if (p.x <= b.x + b.taille_x and 
                            p.x >= b.x - b.taille_x):
                                if p.y - p.taille_y <= b.y + b.taille_y:
                                    p.appliquer_degat(b)
                                    p.alive = False

            #Vérifie si projectile ovnis touche vaisseau
            for o in self.ovnis:
                for p in o.projectiles:
                        if (p.x <= self.vaisseau.x + self.vaisseau.taille_x and 
                            p.x >= self.vaisseau.x - self.vaisseau.taille_x):
                                if p.y + p.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and p.y - p.taille_y <= self.vaisseau.y + self.vaisseau.taille_y:
                                    if not self.vaisseau.invincible:
                                        p.alive = False
                                        self.vaisseau.hp -= p.dommage #hp vaisseau - dommage projectile

            #Verifie si projectile boss touche vaisseau
            if self.boss != None:
                for p in self.boss.projectiles:
                    if (p.x <= self.vaisseau.x + self.vaisseau.taille_x and 
                            p.x >= self.vaisseau.x - self.vaisseau.taille_x):
                                if p.y + p.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and p.y - p.taille_y <= self.vaisseau.y + self.vaisseau.taille_y:
                                    if not self.vaisseau.invincible:
                                        p.alive = False
                                        self.vaisseau.hp -= p.dommage

            #Verifie si projectile vaisseau touche asteroides
            for p in self.vaisseau.projectiles:
                if p.goodBad == "g":
                    for a in self.asteroides:
                        if (p.x <= a.x + a.taille_x and 
                            p.x >= a.x - a.taille_x):
                                if p.y - p.taille_y <= a.y + a.taille_y:
                                    a.hp -= p.dommage #hp asteroides - dommage projectile
                                    p.alive = False

            #Vérifie si ovnis ou boss touche vaisseau
            for o in self.ovnis:
                if (o.x + o.taille_x >= self.vaisseau.x - self.vaisseau.taille_x and 
                    o.x - o.taille_x <= self.vaisseau.x + self.vaisseau.taille_x):
                    if (o.y + o.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and
                        o.y - o.taille_y <= self.vaisseau.y + self.vaisseau.taille_y):
                            if not self.vaisseau.invincible:
                                o.hp -= self.vaisseau.dommage_collision
                                self.vaisseau.hp -= o.dommage_collision
            if b != None:
                if (b.x + b.taille_x >= self.vaisseau.x - self.vaisseau.taille_x and 
                    b.x - b.taille_x <= self.vaisseau.x + self.vaisseau.taille_x):
                    if (b.y + b.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and
                        b.y - b.taille_y <= self.vaisseau.y + self.vaisseau.taille_y):
                            if not self.vaisseau.invincible:
                                b.hp -= self.vaisseau.dommage_collision
                                self.vaisseau.hp -= b.dommage_collision

            #Vérifie si vaisseau touche astéroides
            for a in self.asteroides:
                if (a.x + a.taille_x >= self.vaisseau.x - self.vaisseau.taille_x and 
                    a.x - a.taille_x <= self.vaisseau.x + self.vaisseau.taille_x):
                    if (a.y + a.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and
                        a.y - a.taille_y <= self.vaisseau.y + self.vaisseau.taille_y):
                            if not self.vaisseau.invincible:
                                a.hp -= self.vaisseau.dommage_collision
                                self.vaisseau.hp -= a.dommage_collision

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

            # Apparition aléatoire des ressoruces
            alea_ressource = random.random()
            if alea_ressource < 0.005:
                ressource_id = 1
                nouvelle_res = self.creer_ressource(ressource_id, self.vaisseau)
                self.ressources.append(nouvelle_res)
                print(nouvelle_res)
            # Déplacement des objets
            # Ennemis
            for o in self.ovnis:
                o.mise_a_jour()

            for a in self.asteroides:
                a.mise_a_jour()
                
            if self.boss != None:
                self.boss.mise_a_jour()

            # Ressources
            for r in self.ressources:
                r.mise_a_jour()
            # Les ennemis tirent
            for o in self.ovnis:
                alea_frequence = random.random()
                if alea_frequence < 0.02:
                    o.tirer()
        
            for o in self.ovnis:
                o.mouvement_projectile()
            
            if self.boss != None:
                if self.boss.enTire == True:
                    if self.boss.attackFrequence == 5:
                        self.boss.tirer()
                        self.boss.attackFrequence = 0
                    self.boss.attackFrequence += 1
                if self.frames >= 5:
                    self.boss.enTire = not self.boss.enTire
                    self.frames = 0   
                self.boss.mouvement_projectile()
                
            #Calcule des points
            for o in self.ovnis:
                if o.hp <= 0:
                    self.score += 2
            for a in self.asteroides:
                if a.hp <= 0:
                    self.score += 1

            # Nettoyage des objets sortis de l'écran
            self.ovnis = [
                o for o in self.ovnis
                if o.y < self.hauteur and o.hp > 0
            ]

            self.asteroides = [
                a for a in self.asteroides
                if a.y < self.hauteur and a.hp > 0
            ]

            self.ressources = [
                r for r in self.ressources
                if r.y < self.hauteur and r.alive == True
            ]

