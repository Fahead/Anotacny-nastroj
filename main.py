from flask import Flask, render_template, request
import os
import random
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    save_path = load_path()
    print(save_path)
    images = os.listdir(save_path)
    # v pom je napisana iba cesta "static\obrazky\.."
    # pom odstranuje nepotrebne pismena cesty
    pom = save_path[59:] + "/"


    if request.method == 'POST':
        print(images)
        pom_list = request.form.getlist('mycheckbox')
        print(pom_list)
        final_images = [x for x in images if x not in pom_list]
        print("TOTO JE FINAL OBRAZKY KTORE SOM ONANOTOVAL")
        print(final_images)

        if request.form['submit_value'] == 'bus':
            print('Stlacil si bus tlacidlo')
            annote(save_path, final_images, 'bus')

        elif request.form['submit_value'] == 'truck':
            print('Stlacil si TRUCK tlacidlo')
            annote(save_path, final_images, 'truck')

        elif request.form['submit_value'] == 'minitruck':
            print('Stlacil si MINITRUCK tlacidlo')
            annote(save_path, final_images, 'minitruck')

        elif request.form['submit_value'] == 'car':
            print('Stlacil si CAR tlacidlo')
            annote(save_path, final_images, "car")

        elif request.form['submit_value'] == 'van':
            print('Stlacil si VAN tlacidlo')
            annote(save_path, final_images, 'van')

        elif request.form['submit_value'] == 'minivan':
            print('Stlacil si MINIVAN tlacidlo')
            annote(save_path, final_images, 'minivan')
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
        print("Teraz som spracuvava priecinok:" + random_lines.strip('\n'))
        if 'annot.json' in pom_list:
            print("V TOMTO PRIECINKU SI UZ BOL REKURZIVNE VOLAM TU ISTU FUNKCIU")
            return True
        else:
            print(pom_list)
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
    app_json = json.dumps(final)
    print(app_json)
    # Zapisanie dict do jsonu v tvare {'nazov_obrazka': 'nazov_typu'}
    with open(cesta + 'annot.json', 'w') as fp:
        json.dump(final, fp)
    return

if __name__ == "__main__":
    app.run()
