from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import webbrowser
import ipaddress


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

HOST = "0.0.0.0"
PORT = 9000


# ---------------------------------------------------------------------------
# RÉCEPTION DE LA DEMANDE DU PC A
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):

        if self.path != "/open":
            self.send_error(404)
            return

        longueur = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )

        contenu = self.rfile.read(longueur)

        try:

            data = json.loads(contenu)

            ip_a = data["ip"]

            # Vérification de l'adresse IP reçue
            adresse = ipaddress.ip_address(ip_a)

            # Accepte uniquement une adresse IP privée
            if not adresse.is_private:
                self.send_error(403)
                return

            # Construction de l'adresse du serveur du PC A
            url = f"http://{ip_a}:8080"

            print(
                f"[INFO] Ouverture de : {url}"
            )

            # Ouverture du navigateur du PC B
            webbrowser.open(url)

            # Réponse envoyée au PC A
            self.send_response(200)
            self.end_headers()

            self.wfile.write(b"OK")

        except Exception as e:

            print(
                f"[ERREUR] {e}"
            )

            self.send_error(400)

    def log_message(self, *args):
        pass


# ---------------------------------------------------------------------------
# DÉMARRAGE
# ---------------------------------------------------------------------------

print(
    f"[OK] PC B en attente sur le port {PORT}"
)

HTTPServer(
    (HOST, PORT),
    Handler
).serve_forever()
