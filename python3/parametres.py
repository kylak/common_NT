from infos import textes_critiques   # pour avoir le nom des textes critiques


# À modifier selon la demande de l'utilisateur.
# Valeurs possibles : 0, 1 ou 2.
# 0 : brute/
# 1 : NS_explicited_but_not_removed/
# 2 : NS_replaced_by_content/
# La DATA_TYPE 1 n'est pas encore operationnelle il me semble.
DATA_TYPE = 0

# si on est sur data type = 0 (<=> texte brute)
# pouvoir choisir les manuscrits : NOTAMMENT pouvoir exclure les textes critiques
# ------- BONUS : --------------------------------------------------------
## si on choisit de tester aussi les textes critiques :
# on compare les textes grecques de manuscrits
#on obtient un résultat
# on compare ce résultat avec les textes critiques en data_type = 2
# ensuite il faut reprendre les nominasacra
# […]
# si on est sur data type = 1
# […]
# si on est sur data type = 2
# choisir les textes que l'on veut utiliser.
# […]


# texte représente les textes que l'on veut exclure de l'exécution de notre algo.
# liste vide pour aucun texte.
textes = textes_critiques

#TLG : TOO_LONG
# TM : TIME
TLG_TM = 2.5 # en secondes
# MSG : MESSAGE
TLG_MSG = "A CALCULER"



"""
        # commentaire multiligne pour débuguer la fonction getAjout de diff_versifie.py


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
                            print("scripture[-1] = [" + scripture[-1][0:j] + "]" + scripture[-1][j:-1])
                            print("scripture[-2] = [" + scripture[-2][0:i] + "]" + scripture[-2][i:-1])
                            print("scripture[-1][j(" + str(j) + ")] = " + scripture[-1][j])
                            print("scripture[-2][i(" + str(i) + ")] = " + scripture[-2][i])
                            print("scripture[-1] = [" + scripture[-1][0:j+1] + "]" + scripture[-1][j+1:-1])
                            print("scripture[-2] = [" + scripture[-2][0:i+1] + "]" + scripture[-2][i+1:-1] + "\n")
                            chaine += scripture[-1][j]
                        else:
                            while(scripture[-1][j] != scripture[-2][i]):
                                print("scripture[-1] = [" + scripture[-1][0:j] + "]" + scripture[-1][j:-1])
                                print("scripture[-2] = [" + scripture[-2][0:i] + "]" + scripture[-2][i:-1])
                                if (scripture[-1][j] == '_'):
                                    print("scripture[-1][j(" + str(j) + ")] = " + scripture[-1][j])
                                    print("scripture[-2][i(" + str(i) + ")] = " + scripture[-2][i])
                                    print("scripture[-1] = [" + scripture[-1][0:j+1] + "]" + scripture[-1][j+1:-1])
                                    print("scripture[-2] = [" + scripture[-2][0:i+1] + "]" + scripture[-2][i+1:-1])
                                    j += 1
                                    print("scripture[-1][j(" + str(j) + ")] = " + scripture[-1][j])
                                    print("scripture[-2][i(" + str(i) + ")] = " + scripture[-2][i])
                                else:
                                    print("scripture[-1][j(" + str(j) + ")] = " + scripture[-1][j])
                                    print("scripture[-2][i(" + str(i) + ")] = " + scripture[-2][i])
                                    print("scripture[-1] = [" + scripture[-1][0:j+1] + "]" + scripture[-1][j+1:-1])
                                    print("scripture[-2] = [" + scripture[-2][0:i+1] + "]" + scripture[-2][i+1:-1])
                                    i += 1
                                    print("scripture[-1][j(" + str(j) + ")] = " + scripture[-1][j])
                                    print("scripture[-2][i(" + str(i) + ")] = " + scripture[-2][i])
                            print("scripture[-1] = [" + scripture[-1][0:j+1] + "]" + scripture[-1][j+1:-1])
                            print("scripture[-2] = [" + scripture[-2][0:i+1] + "]" + scripture[-2][i+1:-1])
                            print("j: " + str(j) + "\n")
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


    # à propos de la fonction getAjout()	

    # les points d'interrogations se placent
    # en fonction de la majorité :
    # si la majorité des manuscrits ont une lettre : ?
    # ou si 30% ? non je pense que 50% c'est mieux.
    # sinon rien.
    # finalement je pense que je ne vais pas mettre de ?
    # car ça pourrait induire en erreur je trouve
    # par exemple : ??ee??
    # on pourrait penser qu'il y a des manuscrits qui ont 
    # deux caractères puis ee puis deux caractères
    # alors qu'il serait alors possible qu'il n'y ait aucun 
    # manuscrit de la sorte, exemple :
    # manuscrit A = zzee
    # manuscrit B = eeff
    # de plus dans ce cas ça rallonge notre texte.
    # je trouve que les ? créer de l'incertitude

    """
