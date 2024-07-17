 
# Import des différents modules nécessaire
# OS pour intéragir avec le système d'exploitation
# SOCKET pour obtenir le nom d'hôte de machine
# SYS pour renvoie les codes de sortie a RMM
# DATETIME pour obtenir la date



import os
import socket
import sys
from datetime import datetime
import subprocess

# BS4 nécessite sont téléchargement, le script tente de l'importer et si il est en erreur il lance la commande pour l'installer.

try:
    import bs4
except ImportError:
    subprocess.check_call([
        "python", "-m", "pip", "install", "beautifulsoup4"
        ])

# Il retente de l'installer et importe BeautifulSoup permettant d'analyser le fichier de log HTML

import bs4

from bs4 import BeautifulSoup

# Définition des variables

file_path = r"C:\ProgramData\IperiusBackup\Logs\Job001\LogFile.htm"
target_line = 23
hostname = socket.gethostname()
now = datetime.now()


#message début de script
print(f"Verification etat du job de sauvegarde de iperius backup sur la machine '{hostname}' le {now}")
print(f"--------------------------------------------------------------------------------------------------------------------")

def extract_span_content(file_path, target_line):
    with open(file_path, 'r', encoding='utf-16 LE') as file:
        # Lire toutes les lignes du fichier
        lines = file.readlines()
        
        # Vérifier si la ligne cible existe
        if target_line <= len(lines):
            # Extraire la ligne spécifique (les indices commencent à 0)
            target_html = lines[target_line - 1].strip()
            
            # Utiliser BeautifulSoup pour parser la ligne
            soup = BeautifulSoup(target_html, 'html.parser')
            
            # Trouver la balise span et extraire son contenu
            span = soup.find('span')
            if span:
                return span.string
            else:
                return "Balise span non trouvée sur la ligne spécifiée"
        else:
            return f"La ligne {target_line} n'existe pas dans le fichier"


result = extract_span_content(file_path, target_line)
#print(result)

def main():


    if result is None:
        # Vérifie que la variable result est vide.
        # Dans ces cas-là, aucun fichier de Log n'a été trouvé ou bien être lu.
        print(f"Une erreur s est produite lors de la recherche.")
        print(f"Les logs ne sont pas accessibles ou bien la sauvegarde ne s est pas lance.")
        print(f"La sauvegarde est donc echoue, veuilliez vous connecter sur le serveur '{hostname}' pour resoudre le probleme.")
        # Dans ces cas la fonction renvoie le code 1 interprété par RMM comme tache "ALERT" une notification sera envoyée si elle est configurée.
        sys.exit(1)
        return 1

    elif result == "Sauvegarde terminée avec des avertissements":
        # Vérifie que le résultat dans la variable {result} est le message d'avertissement.
        # Dans cet état cela ne veut pas dire que la sauvegarde est en erreur.
        # La sauvegarde a bien tourné mais n'a rien trouvé à copier car par exemple aucun fichier n'a été modifier depuis la dernière sauvegarde.
        print(f"Le message de retour du job est '{result}'.")
        print(f"Iperius backup n'a detecte aucun changement dans les fichiers et donc n a rien sauvegarder.")
        print(f"La sauvegarde sur le serveur '{hostname}' est donc en avertissement, supition d'erreur.")
        # Dans ces cas la fonction renvoie le code 2 interprété par RMM comme tache "WARNING" une notification sera envoyée si elle est configurée.
        sys.exit(5)
        return 1
        
    elif result == "Sauvegarde terminée avec succès":
        # Vérifie que le résultat dans la variable {result} est identique au message dans de succès de la sauvegarde (dans la variable {search_string})
        print(f"Le message de retour du job est '{result}'.")
        print(f"La sauvegarde sur le serveur '{hostname}' est donc correct.")
        # Dans ces cas la fonction renvoie le code 0 interprété par RMM comme tache "OK"
        sys.exit(0)
        return 0
    
    else:
        print(f"Le message de retour du job est '{result}'.")
        print(f"Les logs indiques que la sauvegarde est en erreur et ne s'est pas lance.")
        print(f"La sauvegarde est donc echoue, veuilliez vous connecter sur le serveur '{hostname}' pour resoudre le probleme.")
        # Dans ces cas la fonction renvoie le code 1 interprété par RMM comme tache "ALERT" une notification sera envoyée si elle est configurée.
        sys.exit(1)
        return 1
    
if __name__ == "__main__":
    main()
