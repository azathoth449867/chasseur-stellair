import random

# ------------------ CLASSES ------------------

class Explosion:
    def __init__(self, x, y, max_radius=30, steps=15):
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.steps = steps  # vitesse de l'explosion
        self.step = 0
        self.circles = []
        self.radius = 0
        self.color = None
        self.mise_a_jour()
    
    def mise_a_jour(self):
        self.radius = (self.step / self.steps) * self.max_radius
        self.color = random.choice(["yellow", "orange", "red", "white"])
        self.step += 1
        
class Projectile:
    def __init__(self, x, y, typeBullet):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = -10  # vers le haut
        self.dommage = 5 # dommange de base
        self.taille_x = 2
        self.taille_y = 10
        self.goodBad = typeBullet
        self.alive = True
        if self.goodBad == "b":
            self.vy = 10

    def mise_a_jour(self):
        self.y += self.vy
    def appliquer_degat(self, cible):
        if hasattr(cible, 'bouclier'):
            # target est le vaisseau
            if cible.bouclier > 0:
                cible.bouclier -= 1
            else: 
                cible.hp -= self.dommage
            return
        cible.hp -= self.dommage

class Shotgun(Projectile):
    def __init__(self, x, y, typeBullet, vx):
        super().__init__(x, y, typeBullet)
        self.vx = vx
    def mise_a_jour(self):
        self.y += self.vy
        self.x += self.vx

class Beam(Projectile):
    def __init__(self, x, y, typeBullet):
        super().__init__(x, y, typeBullet)
    def mise_a_jour(self):
        self.taille_y += self.vy * 3

class Vaisseau:
    def __init__(self, parent, x, y):
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
        self.arme = "Basic"

    def deplacer(self, x, y):
        self.x += (x - self.x) * 0.14
        self.y += (y - self.y) * 0.14
        
    def tirer(self):
        if self.arme == "DoubleCannon":
            proj_gauche = Projectile(self.x - 10, self.y - 20, "g")
            proj_droite = Projectile(self.x + 10, self.y - 20, "g")
            self.projectiles.append(proj_gauche)
            self.projectiles.append(proj_droite)
            return
        elif self.arme == "Shotgun":
            proj_gauche = Shotgun(self.x, self.y - 20, "g", -5)
            proj_milieu = Shotgun(self.x, self.y - 20, "g", 0)
            proj_droite = Shotgun(self.x, self.y - 20, "g", 5)
            self.projectiles.append(proj_gauche)
            self.projectiles.append(proj_milieu)
            self.projectiles.append(proj_droite)
            return
        
        nouveau_proj = Projectile(self.x, self.y - 20, "g")
        self.projectiles.append(nouveau_proj)

    def collision_vaisseau(self, cible):
        if self.invincible == False:
            if self.bouclier > 0:
                self.bouclier -= 1
                cible.hp -= self.dommage_collision
            else:
                self.hp -= cible.dommage_collision
                cible.hp -= self.dommage_collision

    def mise_a_jour(self):
        if self.hp <= 0:                             
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
    def __init__(self, parent, vx, taille_x, taille_y, hp, niveau):
        self.x = 300
        self.y = 50
        self.vx = vx
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.projectiles = []
        self.hp = hp * niveau
        self.dommage_collision = 100
        self.cooldown = 0
        self.estVivant = True
        self.enTire = True
        self.parent = parent

    def tirer(self):
        nouveau_proj = Projectile(self.x, self.y + 20, "b")
        self.projectiles.append(nouveau_proj)
    def mouvement_projectile(self):
        for p in self.projectiles: 
            p.mise_a_jour()
    def mise_a_jour(self):
        if isinstance(self, DoubleCannon):
            self.x += self.vx
        elif isinstance(self, Laser):
            if not self.projectiles:
                self.x += self.vx
        elif isinstance(self, Fonceur):
            self.x += self.vx * 0.7
            self.y += self.vy

            if self.y >= 600 or self.y <= 50:
                self.vy = -self.vy

        if self.hp <= 0: # check état de vie
            self.estVivant = False

        if self.x >= 500 or self.x <= 100:
            self.vx = -self.vx

        self.projectiles = [
                    p for p in self.projectiles
                    if p.y < 700 and p.taille_y < 900 and p.alive
                ]
        
    def gunCooldown(self):
        if self.enTire == True:
                if self.cooldown == 0:
                    self.tirer()
                    self.cooldown = self.maxCooldown
                self.cooldown -= 1
        if self.parent.frames >= 5:
            self.enTire = not self.enTire
            self.parent.frames = 0   
        self.mouvement_projectile()

class DoubleCannon(Boss):
    def __init__(self, parent, niveau):
        super().__init__(parent, 3, 20, 30, 200, niveau)
        self.nom = "DoubleCannon"
        self.maxCooldown = 3
        
    def tirer(self):
        proj_gauche = Projectile(self.x - 10, self.y + 20, "b")
        proj_droite = Projectile(self.x + 10, self.y + 20, "b")
        self.projectiles.append(proj_gauche)
        self.projectiles.append(proj_droite)
    
class Laser(Boss):
    def __init__(self, parent, niveau):
        super().__init__(parent, 3, 30, 25, 300, niveau)
        self.nom = "Laser"
        self.maxCooldown = 8

    def tirer(self):
        laser = Beam(self.x, self.y + 30, "b")
        self.projectiles.append(laser)

class Fonceur(Boss):
    def __init__(self, parent, niveau):
        super().__init__(parent, 6, 25, 20, 350, niveau)
        self.nom = "Fonceur"
        self.maxCooldown = 12
        self.vy = 7

    def tirer(self):
            proj_gauche = Shotgun(self.x, self.y - 20, "b", -5)
            proj_milieu = Shotgun(self.x, self.y - 20, "b", 0)
            proj_droite = Shotgun(self.x, self.y - 20, "b", 5)
            self.projectiles.append(proj_gauche)
            self.projectiles.append(proj_milieu)
            self.projectiles.append(proj_droite)

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
        super().__init__(vaisseau, x, 5)
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
        self.obstacleApparationRate = 0.02
        self.souris_x, self.souris_y = 300, 600
        self.tire = None
        self.enPause = False
        self.pauseCompteur = 0
        self.chronometre = None
        self.vie = 3
        self.game_over = False
        self.boss_id = 0
        self.recompense_id = None
        self.estCommence = False
        self.explosion = []

    def enregistrer(self):
        fichier = open("log.txt", "a")
        fichier.write(f"{self.score},{self.niveau},{self.round} \n")
        fichier.close()

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
            if self.conteur_invincibilite >= 5:
                self.vaisseau.invincible = False
            self.conteur_invincibilite += 1 * 0.03
            
        if self.boss == None:
            if self.frames >= 1:                   # Temp entre chaque vague
                self.frames = 0
                self.round += 1
                self.prochaine_round()
        if self.round > 3:
            if self.boss == None:
                self.boss = self.creer_boss(self.boss_id)
                self.apparationRate = 0
                self.obstacleApparationRate = 0
            if self.boss.estVivant == False:
                self.score += 100 * self.niveau
                self.appliquer_recompense(self.recompense_id)
                self.prochain_niveau()
                    
    def pause_compteur(self):
        self.pauseCompteur += 1 * 0.03
    
    def prochaine_round(self):
        self.enPause = True
        self.apparationRate = 0.02 * (self.round * 0.5 + self.niveau)
        self.ressources = []
        self.explosion = []
        
    def prochain_niveau(self):
        self.boss = None
        self.round = 1
        self.niveau += 1
        self.enPause = True
        self.boss_od = None
        self.vaisseau.hp = self.vaisseau.maxHp # vaisseau regagne hp entre niveau
        self.vaisseau.projectiles = []
        self.ressources = []
        self.definir_niveau()
        
    def definir_niveau(self):
        if self.boss_id < 3:
            self.boss_id += 1
        else: 
            self.boss_id = 1
        self.recompense_id = random.randint(1, 2) # les IDs des récompenses displonibles
        self.estCommence = True
        self.apparationRate = 0.02 * (self.round * 0.5 + self.niveau)

    def appliquer_recompense(self, recompense_id):
        def max_hp():
            self.vaisseau.maxHp += 15
        def generer_arme():
            arme = random.choice(["DoubleCannon", "Shotgun"])
            while arme == self.vaisseau.arme:
                arme = random.choice(["DoubleCannon", "Shotgun"])
            self.vaisseau.arme = arme
        RECOMPENSES_TYPES = {
            1: max_hp,
            2: generer_arme
        }
        return RECOMPENSES_TYPES[recompense_id]()

    def creer_boss(self, boss_id): # génère un boss aléatoire pour le niveau
        BOSS_TYPES = {
            1: DoubleCannon(self, self.niveau),
            2: Laser(self, self.niveau),
            3: Fonceur(self, self.niveau)
        }
        self.vaisseau.projectiles = [] # vide projectiles existants
        return BOSS_TYPES[boss_id]
    
    def creer_ressource(self, ressource_id, vaisseau):
        x = random.randint(50,550)
        RESSOURCE_TYPES = {
            1: Bouclier(vaisseau, x)
        }
        return RESSOURCE_TYPES[ressource_id]

    def collisions_projectiles(self):
            b = self.boss
         #Verifie si projectile vaisseau touche ovnis ou boss
            for p in self.vaisseau.projectiles:
                if p.goodBad == "g":
                    for o in self.ovnis:
                        if (p.x <= o.x + o.taille_x and 
                            p.x >= o.x - o.taille_x):
                                if p.y - p.taille_y <= o.y + o.taille_y and p.y + p.taille_y > o.y - o.taille_y:
                                    p.appliquer_degat(o) #hp ovnis - dommage projectile
                                    p.alive = False
                    if self.boss != None:
                        if (p.x <= b.x + b.taille_x and 
                            p.x >= b.x - b.taille_x):
                                if p.y - p.taille_y <= b.y + b.taille_y and p.y + p.taille_y > b.y - b.taille_y:
                                    p.appliquer_degat(b)
                                    p.alive = False

            #Vérifie si projectile ovnis touche vaisseau
            for o in self.ovnis:
                for p in o.projectiles:
                        if (p.x <= self.vaisseau.x + self.vaisseau.taille_x and 
                            p.x >= self.vaisseau.x - self.vaisseau.taille_x):
                                if p.y + p.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and p.y - p.taille_y <= self.vaisseau.y + self.vaisseau.taille_y:
                                    if not self.vaisseau.invincible:
                                        p.appliquer_degat(self.vaisseau)
                                        p.alive = False
                                        
            #Verifie si projectile boss touche vaisseau
            if self.boss != None:
                for p in self.boss.projectiles:
                    if (p.x <= self.vaisseau.x + self.vaisseau.taille_x and 
                            p.x >= self.vaisseau.x - self.vaisseau.taille_x):
                                if p.y + p.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and p.y - p.taille_y <= self.vaisseau.y + self.vaisseau.taille_y:
                                    if not self.vaisseau.invincible:
                                        if not isinstance(p, Beam):
                                            p.alive = False
                                        p.appliquer_degat(self.vaisseau)
                                        
            #Verifie si projectile vaisseau touche asteroides
            for p in self.vaisseau.projectiles:
                if p.goodBad == "g":
                    for a in self.asteroides:
                        if (p.x <= a.x + a.taille_x and 
                            p.x >= a.x - a.taille_x):
                                if p.y - p.taille_y <= a.y + a.taille_y and p.y + p.taille_y > a.y - a.taille_y:
                                    p.appliquer_degat(a) #hp asteroides - dommage projectile
                                    p.alive = False

    def collisions_objets(self):
            b = self.boss
            # Vérifie collisions ressources avec vaisseau
            for r in self.ressources:
                 if (r.x <= self.vaisseau.x + self.vaisseau.taille_x and 
                            r.x >= self.vaisseau.x - self.vaisseau.taille_x):
                                if r.y + r.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and r.y - r.taille_y <= self.vaisseau.y + self.vaisseau.taille_y:
                                    r.contact_vaisseau()

            #Vérifie si ovnis ou boss touche vaisseau
            for o in self.ovnis:
                if (o.x + o.taille_x >= self.vaisseau.x - self.vaisseau.taille_x and 
                    o.x - o.taille_x <= self.vaisseau.x + self.vaisseau.taille_x):
                    if (o.y + o.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and
                        o.y - o.taille_y <= self.vaisseau.y + self.vaisseau.taille_y):
                            self.vaisseau.collision_vaisseau(o)
            if b != None:
                if (b.x + b.taille_x >= self.vaisseau.x - self.vaisseau.taille_x and 
                    b.x - b.taille_x <= self.vaisseau.x + self.vaisseau.taille_x):
                    if (b.y + b.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and
                        b.y - b.taille_y <= self.vaisseau.y + self.vaisseau.taille_y):
                            self.vaisseau.collision_vaisseau(b)

            #Vérifie si vaisseau touche astéroides
            for a in self.asteroides:
                if (a.x + a.taille_x >= self.vaisseau.x - self.vaisseau.taille_x and 
                    a.x - a.taille_x <= self.vaisseau.x + self.vaisseau.taille_x):
                    if (a.y + a.taille_y >= self.vaisseau.y - self.vaisseau.taille_y and
                        a.y - a.taille_y <= self.vaisseau.y + self.vaisseau.taille_y):
                            self.vaisseau.collision_vaisseau(a)

    def verifier_collisions(self):
        self.collisions_objets()
        self.collisions_projectiles()
        
    def apparition_aléatoire(self):
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
        if self.boss != None: self.obstacleApparationRate = 0.02 * (self.round * 0.5 + self.niveau)
        if alea_asteroide < self.obstacleApparationRate:
            nouvel_ast = Asteroide(
                random.randint(0, self.largeur),
                0,
                random.randint(3, 6)
            )
            self.asteroides.append(nouvel_ast)

        # Apparition aléatoire des ressoruces
        alea_ressource = random.random()
        if alea_ressource < 0.0035:
            ressource_id = 1
            nouvelle_res = self.creer_ressource(ressource_id, self.vaisseau)
            self.ressources.append(nouvelle_res)
        
        # Les ennemis tirent
        for o in self.ovnis:
            alea_frequence = random.random()
            if alea_frequence < 0.02:
                o.tirer()

    def calculer_score(self):
        #Calcule des points
        for o in self.ovnis:
            if o.hp <= 0:
                self.score += 2
        for a in self.asteroides:
            if a.hp <= 0:
                self.score += 1

    def nettoyage(self):
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

        self.explosion = [
            e for e in self.explosion
            if e.step < e.steps
        ]

    def mouvement_objets(self):
        for o in self.ovnis:
            o.mise_a_jour()

        for a in self.asteroides:
            a.mise_a_jour()
            
        if self.boss != None:
            self.boss.mise_a_jour()

        # Ressources
        for r in self.ressources:
            r.mise_a_jour()

    def mouvement_projectiles(self):
        for o in self.ovnis:
            o.mouvement_projectile()
        
        if self.boss != None:
            self.boss.gunCooldown()

    def generer_explosion(self):
        for o in self.ovnis:
            if o.hp <= 0:
                self.explosion.append(Explosion(o.x,o.y))
        for a in self.asteroides:
            if a.hp <= 0:
                self.explosion.append(Explosion(a.x,a.y, 45))
    
    def verifier_gameover(self):
        if self.vaisseau.vie == 0:
            self.enregistrer()
            self.vaisseau = None       
            self.game_over = True
            return

    def mise_a_jour(self):
        self.vaisseau.mise_a_jour()
        self.verifier_gameover()
        self.incrementer_jeu()
        self.verifier_collisions()
        self.vaisseau.deplacer(self.souris_x, self.souris_y)
        self.apparition_aléatoire()
        self.mouvement_objets()
        self.mouvement_projectiles()
        self.calculer_score()
        self.generer_explosion()
        self.nettoyage()