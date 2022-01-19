using System;
using System.IO;
using DiffMatchPatch;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace intersectionnel
{
    class Program
    {

        // 0 : brute, 1 : NS_explicited_but_not_removed/
        // 2 : NS_replaced_by_content/
        public static List<Tuple<string, string>>[] data = new List<Tuple<string, string>>[3];

        public static int DATA_TYPE = Parametres.DATA_TYPE;


        public static string base_chemin = "/Users/gustavberloty/Documents/GitHub/Sébastien LAST/";

        public static void getData(string path0, List<Tuple<string, string>> data)
        {
            string path = string.Concat(base_chemin, path0);
            string[] filenames = Directory.GetFiles(path);
            for (int i = 0; i < filenames.Length; i++)
            {
                string filename = Regex.Match(filenames[i], ".*/(.*).txt").Groups[1].Value;

                // permet de sélectionner les textes que l'on veut
                // notamment utile pour pouvoir évincer les textes critiques
                if (!Parametres.textes.Contains(filename))
                {
                    string text = File.ReadAllText(filenames[i]);
                    data.Add(new Tuple<string, string>(filename, text));
                }
            }
        }


        public static int nb_livre = Infos.book.Length;
        public static int nb_chapitre = 30;
        public static int nb_verset = 70;

        public static diff_match_patch dmp = new diff_match_patch();


        // fonction qui compare une liste de chaîne.
        // codée en itérative dû au coût pour python.
        public static string compare(List<string> strings)
        {
            string retour = "";
            int nb_chaine = strings.Count;
            while (nb_chaine > 1)
            {
                List<string> common = new List<string>();
                for (int x = 0; x < nb_chaine; x++)
                {
                    for (int y = x + 1; y < nb_chaine; y++)
                    {
                        List<Diff> tmp = dmp.diff_main(strings[x], strings[y]);
                        string tmp2 = "";
                        for (int i = 0; i < tmp.Count; i++)
                        {
                            if (tmp[i].operation == Operation.EQUAL)
                            {
                                tmp2 = string.Concat(tmp2, tmp[i].text);
                            }
                        }
                        if (!common.Contains(tmp2))
                        {
                            common.Add(tmp2);
                        }
                    }
                }
                strings = new List<string>(common);
                nb_chaine = strings.Count;
                if (nb_chaine == 1)
                {
                    retour = strings[0];
                }
                else
                {
                    if (nb_chaine == 0)
                    {
                        retour = "";
                    }
                }
            }
            return retour;
        }

        public static string getManuscrit(string refe, string string0)
        {
            string manuscrit = "";
            string0 = string0.Replace(@"|", @"\|");
            string0 = string0.Replace("_", ".");
            string stringRef = string.Concat("^", refe);
            stringRef = string.Concat(stringRef, " ");
            stringRef = string.Concat(stringRef, string0);
            stringRef = string.Concat(stringRef, "$");
            for (int x = 0; x < data[DATA_TYPE].Count; x++)
            {
                if (Regex.Match(data[DATA_TYPE][x].Item2, stringRef, RegexOptions.Multiline).Success)
                {
                    manuscrit = string.Concat(manuscrit, ":");
                    manuscrit = string.Concat(manuscrit, data[DATA_TYPE][x].Item1);
                }
            }
            return manuscrit;
        }

        // On indique les ajouts communs des manuscrits :
        // _ implique que tous les manuscrits ont un caractère à cet endroit
        // mais qu'il n'y a pas unanimité quant à l'identication du caractère.
        public static string getAjout(string string0, string refe)
        {
            List<string> scripture = new List<string>();
            for (int x = 0; x < data[DATA_TYPE].Count; x++)
            {
                string tmp = string.Concat(refe, " (.*)$");
                Match tmpAj = Regex.Match(data[DATA_TYPE][x].Item2, tmp, RegexOptions.Multiline);
                if (tmpAj.Success)
                {
                    List<Diff> modifs = dmp.diff_main(string0, tmpAj.Groups[1].Value);
                    string texte = "";
                    for (int j = 0; j < modifs.Count; j++)
                    {
                        Diff z = modifs[j];
                        Operation c = z.operation;
                        string d = z.text;
                        if (c == Operation.INSERT)
                        {
                            for (int taille = d.Length; taille > 0; taille--) {
                                texte = string.Concat(texte, "_");
                            }
                        }
                        else
                        {
                            if (c == Operation.EQUAL)
                            {
                                texte = string.Concat(texte, d);
                            }
                        }
                    }
                    if (!scripture.Contains(texte))
                    {
                        scripture.Add(texte);
                    }
                }
            }
            if (scripture.Count > 1)
            {
                // Je n'ai pas réussi à faire fonctionner l'algo de Google correctement
                // pour cette fonctionnalité, alors j'utlise un que j'ai fais.
                for (int j = 0; j < scripture.Count; j++)
                {
                    if (!scripture[j].Contains('_'))
                    {
                        return scripture[j];
                    }
                }
                while (scripture.Count > 1)
                {
                    string chaine = "";
                    int i = 0; int j = 0;
                    while (j != scripture.Last().Length && i != scripture[scripture.Count - 2].Length)
                    {
                        if (scripture.Last()[j] == scripture[scripture.Count - 2][i])
                        {
                            chaine = string.Concat(chaine, scripture.Last()[j]);
                        }
                        else
                        {
                            while (scripture.Last()[j] != scripture[scripture.Count - 2][i])
                            {
                                if (scripture.Last()[j] == '_')
                                {
                                    j++;
                                }
                                else
                                {
                                    i++;
                                }
                            }
                            chaine = string.Concat(chaine, scripture.Last()[j]);
                        }
                        i++;
                        j++;
                    }
                    if (!chaine.Contains('_'))
                    {
                        return chaine;
                    }
                    scripture.RemoveAt(scripture.Count - 1);
                    scripture[scripture.Count - 1] = chaine;
                }
                return scripture[0];
            }
            else
            {
                if (scripture.Count == 1)
                {
                    return scripture[0];
                }
            }
            return "";
        }


        static void Main(string[] args)
        {

            base_chemin = string.Concat(base_chemin, "nouveautestament.github.io/outil/bw/manuscrits/versifie/");

            dmp.Diff_Timeout = 0;

            data[0] = new List<Tuple<string, string>>();
            data[1] = new List<Tuple<string, string>>();
            data[2] = new List<Tuple<string, string>>();

            getData("brute/", data[0]);
            getData("NS_explicited_but_not_removed/", data[1]);
            getData("NS_replaced_by_content/", data[2]);

            int livres = nb_livre + 1;
            for (int livre = 1; livre < livres; livre++)
            {
                string nom_livre = Infos.book[livre];
                for (int chapitre = 1; chapitre < nb_chapitre; chapitre++)
                {
                    for (int verset = 1; verset < nb_verset; verset++)
                    {
                        string[] tt = { "^", livre.ToString(), ":", chapitre.ToString(), ":", verset.ToString(), ":.*" };
                        string refe2 = string.Concat(tt);

                        List<string> texte = new List<string>();
                        for (int i = 0; i < data[DATA_TYPE].Count; i++)
                        {
                            Tuple<string, string> z = data[DATA_TYPE][i];
                            string b = z.Item2;
                            Match tmp = Regex.Match(b, refe2, RegexOptions.Multiline);
                            if (tmp.Success)
                            {
                                string ref3 = string.Concat(refe2, " (.*)$");
                                tmp = Regex.Match(tmp.Value, ref3);
                                texte.Add(tmp.Groups[1].Value);
                            }
                        }
                        string resultat = compare(texte);
                        if (!resultat.Equals(""))
                        {
                            string refe3 = string.Concat(refe2.Substring(1, refe2.Length - 3), nom_livre);
                            resultat = getAjout(resultat, refe3);
                            string manuscrit = getManuscrit(refe3, resultat);
                            string tmp = string.Concat(refe3, manuscrit);
                            tmp = string.Concat(tmp, " ");
                            Console.WriteLine(string.Concat(tmp, resultat));
                        }
                    }
                }
            }

        }
    }
}
