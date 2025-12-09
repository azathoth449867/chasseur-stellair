import tkinter as tk

class Vue:
    def __init__(self, controleur, modele):
        self.controleur = controleur
        self.modele = modele
        self.root = tk.Tk()
        self.root.title("Vertical Shooter - MVC")

        self.creer_fenetre_principale()
        self.creer_frame_canevas()
        self.creer_frame_infos()
        self.creer_frame_attribut()

    # ---------- Création de l'interface ----------
    def creer_fenetre_principale(self):
        self.frame_principale = tk.Frame(self.root)
        self.frame_principale.pack()

    def creer_frame_canevas(self):
        self.canevas = tk.Canvas(self.frame_principale, width=600, height=700, bg="black")
        self.canevas.grid(row=0, column=0)

        # Bindings (la Vue gère le canevas)
        self.canevas.bind("<Motion>", self.deplacer_vaisseau)
        self.canevas.bind("<Button-1>", self.tirer)
        self.canevas.bind("<ButtonRelease-1>", self.release)
        self.btn_start = tk.Button(self.canevas, text="Piloter", command=self.piloter)
        self.btn_start.place(x=250, y=550, width=120, height=60)

    def release(self, evt):
        self.controleur.release()

    def creer_frame_infos(self):
        self.frame_infos = tk.Frame(self.frame_principale, bg="#222")
        self.frame_infos.grid(row=0, column=1, sticky="n")

        self.label_vie = tk.Label(self.frame_infos, text="Vies : 3", fg="white", bg="#222", font=("Arial", 12))
        self.label_vie.pack(pady=10)

        self.label_niveau = tk.Label(self.frame_infos, text="Niveau : 1", fg="white", bg="#222", font=("Arial", 12))
        self.label_niveau.pack(pady=10)

        self.label_vague = tk.Label(self.frame_infos, text="Vagues : 1", fg="white", bg="#222", font=("Arial", 12))
        self.label_vague.pack(pady=10)

        self.label_apparationRate = tk.Label(self.frame_infos, text="Apparation Rate : 0.02", fg="white", bg="#222", font=("Arial", 12))
        self.label_apparationRate.pack(pady=10)

        self.btn_rejouer = tk.Button(self.frame_infos, text="Rejouer", command=self.rejouer)
        self.btn_rejouer.pack(pady=10)
        
        

    def creer_frame_attribut(self):
        self.frame_attribut = tk.Frame(self.frame_principale, bg="#b03c32")
        self.frame_attribut.place(x=604, y=225, width=175)

        self.label_pv = tk.Label(self.frame_attribut, text=f"Pv : {self.modele.vaisseau.hp}", fg="white", bg="#b03c32", font=("Arial", 12))
        self.label_pv.pack(pady=10)

        self.label_niveau = tk.Label(self.frame_attribut, text="Niveau : 1", fg="white", bg="#b03c32", font=("Arial", 12))
        self.label_niveau.pack(pady=10)

        self.label_vague = tk.Label(self.frame_attribut, text="Vagues : 1", fg="white", bg="#b03c32", font=("Arial", 12))
        self.label_vague.pack(pady=10)
        
        self.label_score = tk.Label(self.frame_attribut, text=f"Score : {self.modele.score}", fg="white", bg="#b03c32", font=("Arial", 12))
        self.label_score.pack(pady=10)

        self.label_bouclier = tk.Label(self.frame_attribut, text=f"Bouclier : {self.modele.vaisseau.bouclier}", fg="white", bg="#b03c32", font=("Arial", 12))
        self.label_bouclier.pack(pady=10)

    def piloter(self):
        self.controleur.commencer()
        self.btn_start.destroy()
    
    def creer_btn_piloter(self):
        self.btn_start = tk.Button(self.canevas, text="Piloter", command=self.piloter)
        self.btn_start.place(x=250, y=550, width=120, height=60)

    def creer_fenetre_intervalle(self, type):
        if (type == "round"):
                self.canevas.create_text(300,260,text=f"Round : {self.modele.round}", font=("Arial", 30, "bold"), fill="white")
        if (type == "niveau"):
            self.canevas.create_text(300,198,text=f"Niveau : {self.modele.niveau}", font=("Arial", 50, "bold"), fill="yellow")
        if (type == "over"):
            self.canevas.create_text(300,198,text=f"GAME OVER", font=("Arial", 50, "bold"), fill="red")
            self.canevas.create_text(300,260,text=f"Niveau : {self.modele.niveau}", font=("Arial", 30, "bold"), fill="yellow")
            self.canevas.create_text(300,300,text=f"Round : {self.modele.round}", font=("Arial", 20, "bold"), fill="white")


    def afficher_explosion(self):
        exp = self.modele.explosion
        

        for e in exp:
            if e.step > e.steps:
                for c in e.circles:
                    self.canevas.delete(c)
                continue
            cc = self.canevas.create_oval(
            e.x - e.radius,
            e.y - e.radius,
            e.x + e.radius,
            e.y + e.radius,
            fill= e.color,
            outline=""
            )
            e.circles.append(cc)
            e.mise_a_jour()
    # ---------- Affichage du jeu ----------
    def afficher_jeu(self):
        modele = self.modele
        self.canevas.delete("all")

        # --- Vaisseau du joueur ---
        o = modele.ovnis
        b = modele.boss
        if modele.vaisseau != None:
            v = modele.vaisseau
            couleur1 = "blue" if not v.invincible else "yellow" 
            couleur2 = "lightblue" if not v.invincible else "lightyellow"
            self.canevas.create_rectangle(
                v.x - v.taille_x,
                v.y - 5,
                v.x + v.taille_x,
                v.y + 5,
                fill=couleur1
            )
            self.canevas.create_oval(
                v.x - (v.taille_x // 2),
                v.y - v.taille_y,
                v.x + (v.taille_x // 2),
                v.y - 5,
                fill=couleur2
            )
            self.canevas.create_line(
                v.x,
                v.y - v.taille_y,
                v.x,
                v.y - v.taille_y - 5,
                fill="white",
                width=2
            )
            


        # --- Projectiles ---
            for p in v.projectiles:
                self.canevas.create_rectangle(
                    p.x - p.taille_x,
                    p.y - p.taille_y,
                    p.x + p.taille_x,
                    p.y,
                    fill="yellow"
                )
        
            for ovni in o:
                for p in ovni.projectiles:
                    self.canevas.create_rectangle(
                    p.x - p.taille_x,
                    p.y - p.taille_y,
                    p.x + p.taille_x,
                    p.y,
                    fill="red"
                    )

            if modele.boss != None:
                for p in b.projectiles:
                        self.canevas.create_rectangle(
                        p.x - p.taille_x,
                        p.y - p.taille_y,
                        p.x + p.taille_x,
                        p.y,
                        fill="red"
                        )

        # --- OVNIs ---
        for o in modele.ovnis:
            self.canevas.create_oval(
                o.x - o.taille_x,
                o.y - o.taille_y,
                o.x + o.taille_x,
                o.y + 5,
                fill="red"
            )
            self.canevas.create_rectangle(
                o.x - 20,
                o.y + 5,
                o.x + 20,
                o.y + 10,
                fill="silver"
            )

            self.canevas.create_line(
                o.x,
                o.y - o.taille_y,
                o.x,
                o.y - 20,
                fill="yellow",
                width=2
            )

        self.afficher_explosion()

        # --- Boss ---
        if (b != None):
            self.canevas.create_rectangle(b.x-20, b.y-10, b.x+20, b.y+10, fill="gray")
            self.canevas.create_oval(b.x-15, b.y-3, b.x-10, b.y+2, fill="red")
            self.canevas.create_oval(b.x+10, b.y-3, b.x+15, b.y+2, fill="blue")
            self.canevas.create_rectangle(b.x-15, b.y+10, b.x-5, b.y+15, fill="orange")
            self.canevas.create_rectangle(b.x-13, b.y+15, b.x-7, b.y+20, fill="orange")
            self.canevas.create_rectangle(b.x+5, b.y+10, b.x+15, b.y+15, fill="orange")
            self.canevas.create_rectangle(b.x+7, b.y+15, b.x+13, b.y+20, fill="orange")

        # --- Astéroïdes ---
        for a in modele.asteroides:
            self.canevas.create_oval(a.x - a.taille_x, a.y - a.taille_y, a.x + a.taille_x, a.y + a.taille_y, fill="darkred")
        
            self.canevas.create_line(a.x, a.y-18, a.x, a.y-12, fill="red", width=3)
            self.canevas.create_line(a.x, a.y+12, a.x, a.y+18, fill="red", width=3)
            self.canevas.create_line(a.x - 18, a.y, a.x-12, a.y, fill="red", width=3)
            self.canevas.create_line(a.x+12, a.y, a.x+18, a.y, fill="red", width=3)
        
        # --- Ressources ---
        for r in modele.ressources:
            self.canevas.create_oval(r.x - r.taille_x, r.y - r.taille_y, r.x + r.taille_x, r.y + r.taille_y, fill="blue")

        # --- Infos ---
        self.label_vie.config(text=f"Vies : {modele.vaisseau.vie}")
        self.label_niveau.config(text=f"Niveau : {modele.niveau}")
        self.label_vague.config(text=f"Vagues : {modele.round}")
        self.label_apparationRate.config(text=f"Apparation Rate : {modele.apparationRate}")
        if(not self.modele.game_over):
            self.label_pv.config(text=f"Pv : {self.modele.vaisseau.hp}")
            self.label_score.config(text=f"Score : {self.modele.score}")
            self.label_bouclier.config(text=f"Bouclier : {self.modele.vaisseau.bouclier}")

    def deplacer_vaisseau(self,evt):
        # on pourrait vouloir le déplacer en y aussi
        self.controleur.deplacer_vaisseau(evt.x, evt.y)

    def tirer(self,evt):
        self.controleur.tirer()

    def rejouer(self):
        self.controleur.rejouer()

    # ---------- Affichage des intervalles ----------

    def afficher_intervalle(self, type):
        self.creer_fenetre_intervalle(type)

