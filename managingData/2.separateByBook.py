import os
import re


db = "last_db.txt"
chemin_brute = []
chemin_brute.append("brute/brute/")
chemin_brute.append("brute/NS_explicited_but_not_removed/")
chemin_brute.append("brute/NS_replaced_by_content/")

chemin_versifie = []
chemin_versifie.append("versifie/brute/")
chemin_versifie.append("versifie/NS_explicited_but_not_removed/")
chemin_versifie.append("versifie/NS_replaced_by_content/")

for chemin in chemin_brute:
    if not os.path.exists(chemin):
        os.makedirs(chemin)
for chemin in chemin_versifie:
    if not os.path.exists(chemin):
        os.makedirs(chemin)

manuscrit = open(db, "r")
texte = []
fichier_brute = []
fichier_versifie = []


def getNom(l):
    return re.search("[^\s]*:([A-Z|0-9]*)" , line).group(1)


# 1ère boucle : détecter les manuscrits et créer les fichiers associés.
for line in manuscrit:
    if(line != "\n"):
        nom = getNom(line)
        if nom not in texte:
            texte.append(nom)
            tmp = []
            for chemin in chemin_brute:
                tmp.append(str(chemin) + nom + ".txt")
            fichier_brute.append(tmp)
            tmp = []
            for chemin in chemin_versifie:
                tmp.append(str(chemin) + nom + ".txt")
            fichier_versifie.append(tmp)

# print(texte)
manuscrit.close()


manuscrit = open(db, "r")

# 2ème boucle: écrire dans les nouveaux fichiers
for line in manuscrit:
    if(line != "\n"):
        i = texte.index(getNom(line))

        # on supprime les infos génantes pour la comparaison:
        metadata = re.search("^..?(:[^:]*){3}(.*) ", line).group(2)
        line = re.sub(metadata, '', line)

        # dossier versifie
        # brute
        tmp = re.sub("\(.*?\)", '', line)
        file = open(fichier_versifie[i][0], 'a')
        file.write(tmp)
        file.close()
        # NS_explicited_but_not_removed
        tmp = re.sub("\|.*?\|", '', line)
        tmp = re.sub("\((.*?)\)", r"{\1}", tmp)
        file = open(fichier_versifie[i][1], 'a')
        file.write(tmp)
        file.close()

        tmp = re.sub("[{}]", '', tmp)
        file = open(fichier_versifie[i][2], 'a')
        file.write(tmp)
        file.close()

        # dossier brute
        line = re.search("[^a-zA-Z0-9-:]+", line).group()
        line = re.sub("\s", '', line)
        # brute
        tmp = re.sub("\(.*?\)", '', line)
        file = open(fichier_brute[i][0], 'a')
        file.write(tmp)
        file.close()
        # NS_explicited_but_not_removed
        tmp = re.sub("\|.*?\|", '', line)
        tmp = re.sub("\((.*?)\)", r"{\1}", tmp)
        file = open(fichier_brute[i][1], 'a')
        file.write(tmp)
        file.close()

        tmp = re.sub("[{}]", '', tmp)
        file = open(fichier_brute[i][2], 'a')
        file.write(tmp)
        file.close()


manuscrit.close()
