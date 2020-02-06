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
		i = i.split()                   # Recuperer la pref_list
		pref[i.pop(0)[3:]] = [i, ""]        
	f.close
	return pref

def read_pref_spe():
	pref = dict()                # Dictionnaire {'spe_name': '[[pref_list], [affected_student_list], size]'}
	f = open("FichierPrefSpe.txt", "r")
	next(f)                     # Saute nb etudiants
	tmp = f.readline().split()  # Recuperer liste taille

	for i in f:                 # Pour chaque ligne
		i = i.split()           # Recuperer la pref_list
		pref[i.pop(0)] = [i, [], tmp.pop(0)]
	f.close
	return pref

def all_affected(pref_etu):                     # Retourne numero du premier etudiant sans spe, ou -1
	for i in range(1, len(pref_etu) + 1):
		if(pref_etu[str(i)][1] == ""):          # Si Etudiant est sans spe
			return i                            # Numero de l'etudiant
	return -1                                   # code -1 : Tout les étudiants ont une spe

def all_full(dicoMaster):  
    tab = []
    for key in dicoMaster:   #On ajoute à un tab les différentes valeurs possibles des spe de master
        tab.append(key)          
        
    for x in range(len(dicoMaster)): #On parcours toutes les spé puis on voit si elle sont full ou non
        
        if not (is_full(tab[x],dicoMaster)):          # Si le master n'est pas full
            print("enter")
            return x                        # Numero du master
    return -1  

def is_full(spe, pref_spe):                             # Spe full ?
    return len(pref_spe[spe][1]) == pref_spe[spe][2]



def gs_etudiants():
	pref_etu = read_pref_etu()
	pref_spe = read_pref_spe()
	index = all_affected(pref_etu)
	while(index != -1):                                 # Tant qu'il y a des etudiants sans spe
		spe_list_index = 0                              # Index pour pref_list de l'etudiant
		j = 0
		while(pref_etu[str(index)][1] == "" ):          # Tant que l'etudiant considere n'a pas de spe
			spe = pref_etu[str(index)][0][j]            # Spe choisi (ordre de pref)
			if(not(is_full(spe, pref_spe))):            # Si y'a de la place
				pref_etu[str(index)][1] = spe           # Affecter a affected_spe_name
				pref_spe[spe][1].append("Etu"+index)    # Ajouter etu a affected_student_list
			if(is_full(spe, pref_spe)):			# Si le master est full
				indiceNewEtu = 0
				for i in range(len(pref_spe[spe])):     # on parcourt la liste du classement du master
					if(pref_spe[spe][i] == pref_etu[str(index)]): # Si l'etudiant appartient a la liste 
						indiceNewEtu = i                      # On sauvegarde son index
					if(i>len(pref_spe[spe][1][i])):                    # Si le classement de l'étudiant est superieur à celui du dernier, on les échange
						tmpIndex = pref_spe[spe][1][len(pref_spe[1])]	   #On stocke l'id étudiant du sortant (le dernier de la liste)
						pref_etu[tmpIndex][1] = '' # On enlève le sortant du master
						pref_etu[str(index)][1] = spe # On ajoute l'entrant au master
		spe_list_index += 1
	return pref_etu, pref_spe		

def gs_master():
    pref_etu = read_pref_etu()
    pref_spe = read_pref_spe()	
    allMasterFull = all_full(pref_spe)
    masterIndex = 0
    while(allMasterFull != -1):				#Tant que tout les  masters n'est pas complet
        print("ok1")
        indexEtu = 0
        
        while(pref_spe[str(allMasterFull)][1]< len(pref_spe[str(allMasterFull)])): #Tant que le master n'a pas attein sa capacité max
            indexEtu += 1
            pref_spe[masterIndex][1] = pref_etu[indexEtu]                #On affecte à un master des étudiants jusqu'à ce qu'il soit plein            
            pref_etu[indexEtu][1] =  pref_spe[masterIndex]                  # On ajoute l'entrant au master

        if(is_full(pref_spe[str(allMasterFull)], pref_spe)):              #Si le master est plein on enlève l'étudiant plus "mauvais" et on y insert le nouveau
            
            iEtuInMaster = 0
            betterRanked = 0
            worstRanked = 1000000
            posMasterRankedEtu = 1
            
            for i in range(pref_spe[str(allMasterFull)][2]):	#On parcourt les étudiant présent dans le master
                
                for j in range(len(pref_spe[str(allMasterFull)][1])): #On parcours la liste des étudiants préférés du master
                    
                    if(pref_spe[str(allMasterFull)][2][i] == pref_spe[str(allMasterFull)][1][j]): #On cherche l'étudiant actuellement dans le master ayant le pire classement
                        
                        if(j<worstRanked):
                            worstRanked = j                          #Indice du pire étudiant présent du master dans la liste de pref du master
                            iEtuInMaster = i                         #Indice du pire étudiant dans la liste actuel du master
                    else:
                        betterRanked += 1
            iNewEtu = 0
            while(iNewEtu<worstRanked):  #On parcours maintenant la listes des étudiant jusqu'à celui le moins bien classé dans le master
                
                while(pref_etu[0][str(allMasterFull)] != pref_spe[posMasterRankedEtu]): #On trouve la position du master dans la liste de l'etu
                    posMasterRankedEtu += 1 
                
                if(pre_etu[iNewEtu][2] == ''):  #Si l'étudiant n'a pas de master on lui affecte l'actuel
                    pre_etu[iNewEtu][2] = allMasterFull
                
                else:                       #Sinon on compare le classement de l'actuel avec le nouveau
                    posCurrentMaster = 0
                    while(pref_etu[cpt][0] != pref_spe[posCurrentMaster]): # On récupère l'indice du master actuel de l'étu dans sa liste de pref
                        posCurrentMaster += 1                              
                if(posMasterRankedEtu>posCurrentMaster):                   #Si le master actuel est moins désiré que le nouveau alors on échange
                    pre_etu[iNewEtu][2] = allMasterFull
                    break
                iNewEtu += 1
                        
                
            
            pref_spe[str(allMasterFull)][2][iEtuInMaster] = pref_spe[str(allMasterFull)][1][iNewEtu] # On remplace le pire étudiant j actuellement dans le master par l'étudiant i de la liste des pref du master  
            allMasterFull = all_full(pref_spe)                      #Actualisation de la situation des master(tous complets ou non)
	
    return pref_etu, pref_spe
	

		
			
gs_master()

				
	

	
