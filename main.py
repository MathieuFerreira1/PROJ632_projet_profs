import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# ouverture du driver sur le site de Polytech
login = ['femathie', 'Mf061102?intranet']
driver = webdriver.Chrome()
website = 'https://www.polytech.univ-smb.fr/'
driver.get(website)

# Scraping du site afin d'aller sur la page des cours
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/button[2]'))).click()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/header/div[1]/div[2]/div[1]/ul[2]/li/a'))).click()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '/html/body/section[3]/div/div/div/div/div/form/fieldset/input[1]'))).send_keys(login[0])
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '/html/body/section[3]/div/div/div/div/div/form/fieldset/input[2]'))).send_keys(login[1])
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '/html/body/section[3]/div/div/div/div/div/form/fieldset/input[3]'))).click()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[1]/ul/li[3]/a/div/div[2]'))).click()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/ul/li[3]/ul/li[2]/a'))).click()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            '/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div/form/ul/li[2]/div/input[11]'))).click()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[2]/div/div/form/div[2]/button[1]'))).click()

# récupération de la localisation des cours sur la page
elements = driver.find_elements(By.XPATH, '//*[@class="intitule"]/a')
for element in elements:
    element.send_keys(Keys.CONTROL + Keys.RETURN)
handles = driver.window_handles

# parcoure de tous ces cours afin de récupérer le nom des profs avec le mail et les matières dont il est reponsable
liste_profs = {}

for i in range(len(elements)):
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    matiere = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                              '/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[1]/div[2]/div[2]'))).text
    nom = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                          '/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[3]/div[1]/div[2]'))).text
    email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                            '/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[2]'))).text

    # On gère les exceptions notamment au niveau de l'écriture du nom et des mails des profs
    nom2 = str(nom)
    double = False
    for i in nom2:
        if i == ',' or i == ';' or i == '/':
            double = True
    nom2 = nom2.split()
    for i in nom2:
        if i == 'et' or i == '-':
            double = True
    for i in email:
        if i == ',' or i == ';' or i == '/':
            double = True

    if (double == False) and ('@' in str(email)):
        n_email = str(email)
        f_email = ''
        i = 0
        while n_email[i] != '@':
            if n_email[i] != ' ':
                f_email += n_email[i].lower()
            i += 1
        email = f_email + '@univ-smb.fr'

    if double == False:
        n_nom = str(nom)
        i_nom = ''
        for i in n_nom:
            if i == '-':
                i_nom += ' '
            else:
                i_nom += i.lower()
        i_nom = i_nom.split()
        f_nom = ''
        for i in i_nom:
            if i != 'mr' and i != 'mme' and i != 'm.' and i != 'mme.' and i != 'ms' and i != 'ms.':
                i = i.title()
                f_nom += i + ' '
        nom = f_nom

    if (double == False) and (nom != '') and (len(nom2) >= 2):
        if (email in liste_profs) and (matiere not in liste_profs[email][0]):
            liste_profs[email][0].append(matiere)
        else:
            liste_profs[email] = [[matiere], nom]

    if double == True:
        n_nom = str(nom)
        i_nom = []
        f_nom = []
        nombre_pers = n_nom.count(',') + n_nom.count(';') + n_nom.count('/') + (n_nom.split()).count('et') + (
            n_nom.split()).count('-') + 1
        for i in range(nombre_pers):
            i_nom.append('')
            f_nom.append('')
        i = 0
        if (',' in n_nom) or (';' in n_nom) or ('/' in n_nom):
            for lettre in n_nom:
                if (lettre == ',') or (lettre == ';') or (lettre == '/'):
                    i += 1
                elif lettre == '-':
                    i_nom[i] += ' '
                else:
                    i_nom[i] += lettre.lower()
            i = 0
            for personne in i_nom:
                personne = personne.split()
                for mot in personne:
                    if mot != 'mr' and mot != 'mme' and mot != 'm.' and mot != 'mme.' and mot != 'ms' and mot != 'ms.':
                        mot = mot.title()
                        f_nom[i] += mot + ' '
                i += 1
            nom = f_nom
        else:
            n_nom = n_nom.lower()
            n_nom = n_nom.split()
            for mot in n_nom:
                if mot == 'et' or mot == '-':
                    i += 1
                else:
                    i_nom[i] += mot + ' '
            i = 0
            for personne in i_nom:
                personne = personne.split()
                for mot in personne:
                    if mot != 'mr' and mot != 'mme' and mot != 'm.' and mot != 'mme.' and mot != 'ms' and mot != 'ms.':
                        mot = mot.title()
                        f_nom[i] += mot + ' '
                i += 1
            nom = f_nom

    if (double == True) and ('@' in str(email)):
        n_email = str(email)
        nombre_pers = n_email.count(',') + n_email.count(';') + n_email.count('/') + 1
        i_email = []
        f_email = []
        for i in range(nombre_pers):
            i_email.append('')
            f_email.append('')
        i = 0
        for lettre in n_email:
            if (lettre == ',') or (lettre == ';') or (lettre == '/'):
                i += 1
            else:
                i_email[i] += lettre
        j = 0
        for adresse in i_email:
            i = 0
            valide = '@' in adresse
            while valide and (adresse[i] != '@'):
                if adresse[i] != ' ':
                    f_email[j] += adresse[i].lower()
                i += 1
            if valide:
                f_email[j] = f_email[j] + '@univ-smb.fr'
            j += 1
        email = f_email

    if double == True:
        for i in range(len(email)):
            if (email[i] in liste_profs) and (matiere not in liste_profs[email[i]][0]):
                liste_profs[email[i]][0].append(matiere)
            else:
                if email[i] != '' and nom[i] != '':
                    liste_profs[email[i]] = [[matiere], nom[i]]

    driver.close()

# On récupère les noms des profs
liste_nom = []
for personne in liste_profs.values():
    liste_nom.append(personne[1])

# Ouverture d'une nouvelle fenêtre pour récupérer les articles écris par les profs
dico = {}
for i in liste_nom:
    dico[i] = []
driver = webdriver.Chrome()
website = 'https://hal.archives-ouvertes.fr/'
driver.get(website)

# Scraping de la première page d'articles pour chacun des profs
for prof in liste_nom:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/main/section[2]/form/div/div/div/input'))).send_keys(prof)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/main/section[2]/form/div/div/div/button/i'))).click()
    texte = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="results-header"]/div[1]/span'))).text
    if texte != '':
        elements = driver.find_elements(By.XPATH, '//*[@class="title-results"]')
        for element in elements:
            dico[prof].append(element.text)
    driver.back()

for adresse in liste_profs.values():
    for nom in liste_nom:
        if nom == adresse[1]:
            adresse.append(dico[nom])

# On reformate le nouveau dictionnaire contenant toutes les infos sur les profs afin d'avoir le nom comme clé principale
dico = {}
for i, j in liste_profs.items():
    dico[str(j[1])] = {'email': i, 'responsable matieres': j[0], 'articles': j[2]}

# Écriture du fichier json
with open("profs.json", "w", encoding="utf8") as f:
    json.dump(dico, f, indent=2)

# Écriture du fichier texte
with open("text.txt", "w", encoding="utf8") as f:
    for i, j in liste_profs.items():
        f.write(str(j[1]))
        f.write('\n')
        f.write('responsable matieres : ')
        f.write(str(j[0]))
        f.write('\n')
        f.write('email : ')
        f.write(str(i))
        f.write('\n')
        f.write('article : ')
        f.write(str(j[2]))
        f.write('\n')
        f.write('\n')
