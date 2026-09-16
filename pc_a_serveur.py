import socket
import json
import threading
import urllib.request

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

HOST = "0.0.0.0"
PORT = 8080


# ---------------------------------------------------------------------------
# CONFIGURATION DU PC B
# ---------------------------------------------------------------------------

# Adresse IP du PC B
PC_B = "192.168.1.50"

# Port utilisé par le récepteur du PC B
PORT_B = 9000


# ---------------------------------------------------------------------------
# PAGE WEB HÉBERGÉE SUR LE PC A
# ---------------------------------------------------------------------------

PAGE_HTML = """<!DOCTYPE html>
<html lang="fr">

<head>

    <meta charset="utf-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>Serveur PC A</title>

    <style>

        body {
            background: #0d1117;
            color: #e6edf3;
            font-family: "Segoe UI", sans-serif;
            text-align: center;
            padding-top: 100px;
        }

        h1 {
            color: #58a6ff;
        }

        .status {
            margin-top: 30px;
            font-size: 18px;
            color: #3fb950;
        }

    </style>

</head>

<body>

    <h1>
        Serveur HTTP PC A
    </h1>

    <div class="status">
        ● Connexion établie
    </div>

    <p>
        Cette page est hébergée sur le PC A.
    </p>

</body>

</html>
"""


# ---------------------------------------------------------------------------
# SERVEUR HTTP DU PC A
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):

    def log_message(self, *args):
        pass

    def do_GET(self):

        if self.path == "/":

            corps = PAGE_HTML.encode("utf-8")

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(corps))
            )

            self.end_headers()

            self.wfile.write(corps)

        else:

            self.send_error(404)


# ---------------------------------------------------------------------------
# DÉMARRAGE DU SERVEUR HTTP
# ---------------------------------------------------------------------------

def demarrer_serveur():

    serveur = ThreadingHTTPServer(
        (HOST, PORT),
        Handler
    )

    print(
        f"[OK] Serveur HTTP lancé sur le port {PORT}"
    )

    serveur.serve_forever()


# ---------------------------------------------------------------------------
# RÉCUPÉRATION AUTOMATIQUE DE L'IP DU PC A
# ---------------------------------------------------------------------------

def recuperer_ip_locale():

    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    try:

        s.connect(
            ("8.8.8.8", 80)
        )

        ip_locale = s.getsockname()[0]

        return ip_locale

    finally:

        s.close()


# ---------------------------------------------------------------------------
# DEMANDE D'OUVERTURE DU NAVIGATEUR SUR LE PC B
# ---------------------------------------------------------------------------

def ouvrir_page_sur_pc_b():

    # Récupération automatique de l'IP du PC A
    ip_a = recuperer_ip_locale()

    print(
        f"[INFO] Adresse IP du PC A : {ip_a}"
    )

    # Création des données JSON
    data = json.dumps({

        "ip": ip_a

    }).encode("utf-8")


    # Création de la requête HTTP vers le PC B
    requete = urllib.request.Request(

        f"http://{PC_B}:{PORT_B}/open",

        data=data,

        headers={
            "Content-Type": "application/json"
        },

        method="POST"
    )


    try:

        with urllib.request.urlopen(
            requete,
            timeout=5
        ) as reponse:

            resultat = reponse.read().decode()

            print(
                f"[OK] Réponse du PC B : {resultat}"
            )

    except Exception as e:

        print(
            f"[ERREUR] Impossible de contacter le PC B : {e}"
        )


# ---------------------------------------------------------------------------
# DÉMARRAGE
# ---------------------------------------------------------------------------

print(
    "Démarrage du PC A..."
)


# Lancement du serveur HTTP en arrière-plan
threading.Thread(
    target=demarrer_serveur,
    daemon=True
).start()


# Demande au PC B d'ouvrir la page
ouvrir_page_sur_pc_b()


print(
    "[OK] Serveur actif."
)


# Maintient le programme actif
threading.Event().wait()
