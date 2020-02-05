#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:15:40 2020

@author: 3970730
"""

# Question 3
def read_pref_etu():
	pref = dict()                    #  Dictionnaire {'etu_number':'[[pref_list],affected_spe_name]'} 									
	f = open("FichierPrefEtu.txt", "r")
	next(f)                                 # Sauter nb etudiants
	for i in f:                             # Pour chaque ligne
		i = i.split()                       # Recuperer la pref_list
		pref[i.pop(0)[3:]] = [i, ""]        
	f.close
	return pref

def read_pref_spe():
	pref = dict()               # Dictionnaire {'spe_name': '[[pref_list], [affected_student_list, position_in_pref_list], size]'}
	f = open("FichierPrefSpe.txt", "r")
	next(f)                     # Saute nb etudiants
	tmp = f.readline().split()  # Recuperer liste taille

	for i in f:                 # Pour chaque ligne
		i = i.split()           # Recuperer la pref_list
		pref[i.pop(0)] = [i, [[], []], tmp.pop(0)]
	f.close
	return pref

def all_affected(pref_etu):                     # Retourne numero du premier etudiant sans spe, ou -1
	for i in range(1, len(pref_etu) + 1):
		if(pref_etu[str(i)][1] == ""):          # Si Etudiant est sans spe
			return i                            # Numero de l'etudiant
	return -1                                   # code -1 : Tout les étudiants ont une spe

def all_full(dicoMaster):                     # Retourne numero du premier master pas full, ou -1
	for i in range(dicoMaster):
		if(is_full(dicoMaster[i][1]),dicoMaster[i][2]):          # Si le master n'est pas full
			return i                            # Numero du master
	return -1  

def is_full(spe, pref_spe):                             # Spe full ?
	return len(pref_spe[spe][1]) == pref_spe[spe][2]

def assign_stu(etu, index_spe_etu, list_affected_student):
    index = 0
    while((index_spe_etu > list_affected_student[1][index]) and (index < len(list_affected_student) - 1)):    # Tant que etu est moins prefere que celui dans la liste.
        print("test")
        index += 1                                                # Examine l'etudiant suivant dans la liste
    list_affected_student[0].insert(index, "Etu"+str(etu))
    list_affected_student[1].insert(index, index_spe_etu)
    return

def gs_etudiants():
    pref_etu = read_pref_etu()
    pref_spe = read_pref_spe()
    etu = all_affected(pref_etu)                      # -1 si tout les etudiants affecte, sinon numero de l'etudiant que l'on va affecter(!!!!!!! Voir si on peut caster en str ici au lieu de partout)
    while(etu != -1):                                 # Tant qu'il y a des etudiants sans spe                       
        index_etu_spe = 0                             # Index pour pref_list de l'etudiant
        while(pref_etu[str(etu)][1] == "" ):          # Tant que l'etudiant considere n'a pas de spe
            spe = pref_etu[str(etu)][0][index_etu_spe]                    # Master choisi (ordre de pref)
            print("Etudiant ", etu, " veut " , spe)
            index_spe_etu = 0                                             # Position de l'etudiant dans la pref_list du master      
            while(pref_spe[spe][0][index_spe_etu] != str(etu)):    # On parcourt la liste du master tant qu'on ne tombe pas sur l'etudiant
                index_spe_etu += 1
            if(not(is_full(spe, pref_spe))):            # Si y'a de la place
                pref_etu[str(etu)][1] = spe                 # Affecter a affected_spe_name
                if(not pref_spe[spe][1][0]):                    # Si aucun etudiant affecte
                    pref_spe[spe][1][0].append("Etu"+str(etu))       # Ajouter etu a affected_student_list
                    pref_spe[spe][1][1].append(index_spe_etu)   # Ajouter sa position dans la pref_list du master
                else:
                    assign_stu(etu, index_spe_etu, pref_spe[spe][1])    # Ajouter etu a affected_student_list
            else:		                       # Si le master est full	
                if(index_spe_etu < pref_spe[spe][1][1][-1]):     # Si l'etudiant qui postule est prefere a l'etudiant le moins prefere, deja affecte
                    pref_etu[pref_spe[spe][1][1][-1]][1] = ""    # Retirer l'affection du master a l'etudiant
                    pref_spe[spe][1][1].pop()                    # Retire l'etudiant le moins prefere de la liste
                    assign_stu(etu, index_spe_etu, pref_spe[spe][1])    # Ajouter etu a affected_student_list
            index_etu_spe += 1
        etu = all_affected(pref_etu)
    return pref_etu, pref_spe		

# TEST gs_etudiants()

etu, spe = gs_etudiants()

#for item in etu.items():
#    print(item)
#for key, value in etu.items():
#    print(key, " : ", value[1])

for key, value in spe.items():
    print(key, " : ", value[1])

#pref_etu = read_pref_etu()
#pref_spe = read_pref_spe()
#print(pref_spe)

# FIN TEST


#def gs_master():
#	pref_etu = read_pref_etu()
#	pref_spe = read_pref_spe()	
#	allMasterFull = all_full(pref_spe)
#	masterIndex = 0
#	while(!allMasterFull != -1):				#Tant que tout les  masters n'est pas complet
#		indexEtu = 0
#
#		while(pref_spe[str(allMasterFull)][1]< len(pref_spe[str(allMasterFull)])): #Tant que le master n'a pas attein sa capacité max
#			pref_spe[masterIndex][1] = pref_etu[indexEtu]
#
#		if(is_full(pref_spe[str(allMasterFull)], pref_spe)):
#			for i in range(pref_spe[str(allMasterFull)][1]):
#				j = 0
#				k = 0
#
#				for i in range(len(pref_spe[str(allMasterFull)][2])):
#					for j in range(len(pref_spe[str(allMasterFull)][2])):
#						if(pref_spe[str(allMasterFull)][2][i] == pref_spe[str(allMasterFull)][1][j]):
#							minJ = j
#
#				while(pref_spe[str(allMasterFull)][2][i] != pref_spe[str(allMasterFull)][1][j]:
#					newEtu = j++
#
#				while(pref_spe[str(allMasterFull)][2][len(pref_spe[str(allMasterFull)][2]-1)] != pref_spe[str(allMasterFull)][1][j]:
#					dernierEtu = k++
#				
#				if(newEtu<dernierEtu):
#					
#
#					
#					
#
#	allMasterFull = all_full(pref_spe)
#	return pref_etu, pref_spe
#	
#
#		
			


				
	

	
