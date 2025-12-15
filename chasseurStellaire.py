from modele import Modele
from vue import Vue

class Controleur:
    def __init__(self):
        self.modele = Modele(self,600,800)
        self.vue = Vue(self, self.modele)
        self.vue.afficher_jeu()
        self.vue.root.mainloop()

    def boucle_jeu(self):
        if self.modele.enPause:
            self.modele.ovnis = []
            self.modele.asteroides = []
            self.modele.vaisseau.projectiles = []
            self.modele.vaisseau.x, self.modele.vaisseau.y = 300, 600
            self.vue.afficher_jeu()
            self.afficher_intervalle("round")
            self.afficher_intervalle("niveau")
            self.commence_compteur()
        elif self.modele.game_over:
            self.modele.ovnis = []
            self.modele.asteroides = []
            self.modele.explosion = []
            self.modele.ressources = []
            self.vue.afficher_jeu()
            self.afficher_intervalle("over")
        else:
            if self.modele.estCommence == False:
                self.modele.definir_niveau()
            else:
                self.modele.mise_a_jour()
                self.vue.afficher_jeu()
                self.vue.root.after(30, self.boucle_jeu)

    # Méthodes appelées par la Vue (via bindings)
    def deplacer_vaisseau(self, x, y):
        self.modele.deplacer_vaisseau(x, y)

    def release(self):
        self.vue.root.after_cancel(self.modele.tire)
    
    def tirer(self):
        self.modele.tirer()
        self.modele.tire = self.vue.root.after(100, self.tirer)

    def rejouer(self):
        self.modele = Modele(self,600,800)
        self.vue.modele = self.modele
        self.vue.creer_btn_piloter()
        self.vue.afficher_jeu()

    def commence_compteur(self):
        self.modele.pause_compteur()
        if self.modele.pauseCompteur > 1:
                self.modele.enPause = False
                self.modele.pauseCompteur = 0
                self.vue.root.after_cancel(self.modele.chronometre)
                self.boucle_jeu()
        if self.modele.enPause:
            self.modele.chronometre = self.vue.root.after(30, self.commence_compteur)

    def afficher_intervalle(self, type):
        self.vue.afficher_intervalle(type)

    def commencer(self):
        self.modele.definir_niveau()
        self.modele.estCommence = True
        self.boucle_jeu()

if __name__ == "__main__":
    c = Controleur()