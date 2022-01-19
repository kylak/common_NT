from parametres import DATA_TYPE, textes # pour connaître le DATA_TYPE et les textes qu'on ne veut pas utiliser.
from infos import book   # pour avoir les noms de livres
import re 		# pour la regex
import os			# pour gérér les fichiers
import glob		# pour gérér les fichiers
import diff_match_patch as dmp_module	# pour comparer deux chaînes
dmp = dmp_module.diff_match_patch()


# DATA_TYPE est définie dans le fichier parametres.py



base_chemin = "/Users/gustavberloty/Documents/GitHub/Sébastien LAST/"
base_chemin += "nouveautestament.github.io/outil/bw/manuscrits/versifie/"

def getData(path, data):
    path = base_chemin + path
    for filename in glob.glob(os.path.join(path, '*.txt')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            filename = re.search(".*/(.*).txt", filename).group(1)

            # permet de sélectionner les textes que l'on veut
            # notamment utile pour pouvoir évincer les textes critiques
            if filename not in textes:
                data.append((filename, f.read()))


# 0 : brute, 1 : NS_explicited_but_not_removed/
# 2 : NS_replaced_by_content/
data = []
for i in range(3): data.append([])

getData("brute/", data[0])
getData("NS_explicited_but_not_removed/", data[1])
getData("NS_replaced_by_content/", data[2])





nb_livre = len(book)
nb_chapitre = 30
nb_verset = 70

dmp.Diff_Timeout = 0


# fonction qui compare une liste de chaîne.
# codée en itérative dû au coût pour python.
def compare(strings):
    retour = ""
    nb_chaine = len(strings)
    while(nb_chaine > 1):
        common = []
        for x in range(nb_chaine):
            for y in range(x, nb_chaine):
                if x != y:
                    tmp = dmp.diff_main(strings[x], strings[y])
                    tmp2= ""
                    for (a, b) in tmp:
                        if a == 0:
                            tmp2 = tmp2 + b
                    if tmp2 not in common:
                        common.append(tmp2)
        strings = common
        nb_chaine = len(strings)
        if (nb_chaine == 1):
            retour = strings[0]
        else:
            if (nb_chaine == 0):
                retour = ""
    return retour



def getManuscrit(ref, string):
    manuscrit = ""
    string = re.sub("\|", "\|", string)
    string = re.sub("_", ".", string)
    stringRef = "^" + ref + " " + string + "$"
    for x in data[DATA_TYPE]:
        if re.search(stringRef, x[1], re.MULTILINE) != None:
            manuscrit += ":" + x[0]
    return manuscrit

# On indique les ajouts communs des manuscrits :
# _ implique que tous les manuscrits ont un caractère à cet endroit
# mais qu'il n'y a pas unanimité quant à l'identication du caractère.
def getAjout(string, ref):
    scripture = []
    for x in data[DATA_TYPE]:
        tmp = re.search(ref + " (.*)$", x[1],  re.MULTILINE)
        if tmp != None:
            modifs = dmp.diff_main(string, tmp.group(1))
            texte = ""
            for (c, d) in modifs:
                if (c == 1):
                    taille = len(d)
                    for y in range(taille):
                        texte += "_"
                else:
                    if (c == 0):
                        texte += d
            if texte not in scripture:
                scripture.append(texte)
    if len(scripture) > 1:
        # Je n'ai pas réussi à faire fonctionner l'algo de Google correctement
        # pour cette fonctionnalité, alors j'utlise un que j'ai fais.
        for y in scripture:
            if '_' not in y:
                return y
        while(len(scripture) > 1):
            chaine = ""
            i = 0; j = 0
            while j != len(scripture[-1]) and i != len(scripture[-2]):
                if(scripture[-1][j] == scripture[-2][i]):
                    chaine += scripture[-1][j]
                else:
                    while(scripture[-1][j] != scripture[-2][i]):
                        if (scripture[-1][j] == '_'):
                            j += 1
                        else:
                            i += 1
                        chaine += scripture[-1][j]
                    i += 1
                    j += 1
            if '_' not in chaine:
                return chaine
            scripture.pop()
            scripture[-1] = chaine
        return scripture[0]
    else:
        if len(scripture) == 1:
            return scripture[0]
    return ""


# Fonction main ci-dessous.

livres = nb_livre + 1
for livre in range(1, livres) :
    nom_livre = book[livre]
    for chapitre in range(1, nb_chapitre):
        for verset in range(1, nb_verset):

            ref = "^" + str(livre) + ":" + str(chapitre) + ":" + str(verset) + ":.*"

            texte = []
            for (a, b) in data[DATA_TYPE]:
                tmp = re.search(ref, b, re.MULTILINE)
                if tmp != None:
                    tmp = re.search(ref + " (.*)", tmp.group(0))
                    texte.append(tmp.group(1))

            resultat = compare(texte)
            if resultat != "":
                ref = ref[1:-2] + nom_livre
                resultat = getAjout(resultat, ref)
                manuscrit = getManuscrit(ref, resultat)
                print(ref + manuscrit + " " + resultat)


