from flask import Flask, render_template, request
import os
import random
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    save_path = load_path()
    images = os.listdir(save_path)
    # v pom je napisana iba cesta "static\obrazky\.."
    # pom odstranuje nepotrebne pismena cesty
    pom = save_path[59:] + "/"
    # textak kde sa budu ukladat pole obrazkov + cesta

    # subor kde sa uklada pomocna cesta
    with open("pomocna_cesta.txt", "a+") as f:
        f.writelines(save_path)
        f.writelines("\n")
        f.close()

    # pomocny subor do ktoreho sa ukladaju vsetky obrazky ktore sa anotuju
    with open("pomocny_file.txt", "a+") as file:
        file.writelines(["%s\n" % item  for item in images])
        file.writelines("koniec" + '\n')
        file.close()

    if request.method == 'POST':
        #print("TERAZ SOM PRECITAL PRVY DRUHY RIADOK-------------------------------------")
        list_druhy = []
        # nacitanie pomocneho filu
        with open("pomocny_file.txt", "r") as file:
            prvy_riadok = file.read().splitlines()
            file.close()
        for item in prvy_riadok:
            if item != 'koniec':
                list_druhy.append(item)
            else:
                break

        with open("pomocna_cesta.txt", "r") as file:
            ulozena_cesta_list = file.read().splitlines()
            ulozena_cesta = ulozena_cesta_list[0]
            file.close()

        #print(ulozena_cesta)
        #print(list_druhy)
        pom_list = request.form.getlist('mycheckbox')
        #print(pom_list)
        # final_images je vsetky obrazky - obrazky ktore boli odskrtnute
        final_images = [x for x in list_druhy if x not in pom_list]

        if request.form['submit_value'] == 'bus':
            annote(ulozena_cesta, final_images, 'bus')

        elif request.form['submit_value'] == 'truck':
            annote(ulozena_cesta, final_images, 'truck')

        elif request.form['submit_value'] == 'minitruck':
            annote(ulozena_cesta, final_images, 'minitruck')

        elif request.form['submit_value'] == 'car':
            annote(ulozena_cesta, final_images, "car")

        elif request.form['submit_value'] == 'van':
            annote(ulozena_cesta, final_images, 'van')

        elif request.form['submit_value'] == 'minivan':
            annote(ulozena_cesta, final_images, 'minivan')


        # nacitanie pomocneho aby sa odstranili uz vytvorene anotacie
        with open("pomocny_file.txt", "r+") as file:
            li = file.read().splitlines()
            del li[:li.index('koniec')+1]
            file.close()

        # prepisanie pomocneho suboru
        with open("pomocny_file.txt", "w") as file:
            file.writelines(["%s\n" % item for item in li])
            file.close()
        with open('pomocna_cesta.txt', 'r') as fin:
            data = fin.read().splitlines(True)
            fin.close()
        with open('pomocna_cesta.txt', 'w') as fout:
            fout.writelines(data[1:])
            fout.close()

        return render_template('main.html', images=images, pathh=pom)
    return render_template('main.html', images=images, pathh=pom)


# Nacitanie riadka zo suboru priecinky.txt kde sa nachadzaju vsetky priecinky z obrazkami
# Vyberie sa nahodne jeden riadok zo subora
# Nacita sa ten riadok a rovno sa pomoze otvori a vyhodnoti sa podmienka ci sa nachadza subor annot.txt v priecinku
# Funkcia vrati cestu priecinka
def load_path():
    try:
        # ulozenie textoveho suboru kde sa nachadzaju cesty k priecinkom
        filename = r'E:\VUT\7.semester(4 rocnik)\Python ucenie\Anotacny nastroj\priecinky.txt'
        random_lines = random.choice(open(filename).readlines())
        pom_list = os.listdir(random_lines.strip('\n'))
        #print("Teraz som spracuvava priecinok:" + random_lines.strip('\n'))
        if 'annot.json' in pom_list:
            print("V TOMTO PRIECINKU SI UZ BOL REKURZIVNE VOLAM TU ISTU FUNKCIU")
            return load_path()
        else:
            return random_lines.strip('\n')
    except Exception:
        return load_path()

# Funkcia ktora vytvori anotaciu ku obrazkom, a vytvori tak isto aj subor annot.txt
# Parametre
#   @patth - cesta do priecinka kde sa obrazky nachadzaju
#   @images - zoznam obrazkov ktore splnaju kriteria
#   @name_type - nazov typu vozidla
def annote(patth,images,name_type):
    final = {}
    cesta = patth + "\\"
    for item in images:
        final.update({item: name_type})
    # Zapisanie dict do jsonu v tvare {'nazov_obrazka': 'nazov_typu'}
    with open(cesta + 'annot.json', 'w') as fp:
        json.dump(final, fp)
    return

if __name__ == "__main__":
    app.run()
