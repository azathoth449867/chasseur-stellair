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

    def creer_fenetre_intervalle(self, type):
        if (type == "round"):
                self.canevas.create_text(300,260,text=f"Round : {self.modele.round}", font=("Arial", 30, "bold"), fill="white")
        if (type == "niveau"):
            self.canevas.create_text(300,198,text=f"Niveau : {self.modele.niveau}", font=("Arial", 50, "bold"), fill="yellow")
        if (type == "over"):
            self.canevas.create_text(300,198,text=f"GAME OVER", font=("Arial", 50, "bold"), fill="red")
            self.canevas.create_text(300,260,text=f"Niveau : {self.modele.niveau}", font=("Arial", 30, "bold"), fill="yellow")
            self.canevas.create_text(300,300,text=f"Round : {self.modele.round}", font=("Arial", 20, "bold"), fill="white")

    # ---------- Affichage du jeu ----------
    def afficher_jeu(self):
        modele = self.modele
        self.canevas.delete("all")

        # --- Vaisseau du joueur ---
        o = modele.ovnis
        if modele.vaisseau != None:
            v = modele.vaisseau
            self.canevas.create_rectangle(
                v.x - v.taille_x,
                v.y - 5,
                v.x + v.taille_x,
                v.y + 5,
                fill="blue"
            )
            self.canevas.create_oval(
                v.x - (v.taille_x // 2),
                v.y - v.taille_y,
                v.x + (v.taille_x // 2),
                v.y - 5,
                fill="lightblue"
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
                fill="yellow"
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

        # --- Astéroïdes ---
        for a in modele.asteroides:
            self.canevas.create_oval(a.x - a.taille_x, a.y - a.taille_y, a.x + a.taille_x, a.y + a.taille_y, fill="darkred")
        
            self.canevas.create_line(a.x, a.y-18, a.x, a.y-12, fill="red", width=3)
            self.canevas.create_line(a.x, a.y+12, a.x, a.y+18, fill="red", width=3)
            self.canevas.create_line(a.x - 18, a.y, a.x-12, a.y, fill="red", width=3)
            self.canevas.create_line(a.x+12, a.y, a.x+18, a.y, fill="red", width=3)

        # --- Infos ---
        self.label_vie.config(text=f"Vies : {modele.vie}")
        self.label_niveau.config(text=f"Niveau : {modele.niveau}")
        self.label_vague.config(text=f"Vagues : {modele.round}")
        self.label_apparationRate.config(text=f"Apparation Rate : {modele.apparationRate}")

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

