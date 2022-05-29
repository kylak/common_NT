import re

# Script pour ne conserver que la dernière version des manuscrits sur tel ou tel passage.
# Exemple : Si en Mt 1:1 nous avons Sinaïticus A et Sinaïticus B, on ne garde que Sinaïticus B.
# Ne fonctionne pas avec les manuscrits de A.Bunning il me semble.

nom = "chosen_db.txt"
manuscrit = open(nom, "r")
new = []

last_ref = ""
last_version = ""
for line in manuscrit:
	if(line != "\n"):
		new_ref = re.search("^([0-9]+:){3}", line).group()
		new_version = re.search("^([0-9]+:){3}[A-Z|0-9]+(:[0-9]+){3}:([A-Z|0-9]*)" , line)
		if new_version == None :
        		print(line) # Pour débuguer.
        		break
		else:
            		new_version = new_version.group(3)
		if (new_version == last_version and new_ref == last_ref):
			new.pop()
		last_ref = new_ref
		last_version = new_version
	new.append(line)
manuscrit.close()

manuscrit_final = open("lastOnes_" + nom, "w")
for line in new:
    manuscrit_final.write(line)
manuscrit_final.close()
