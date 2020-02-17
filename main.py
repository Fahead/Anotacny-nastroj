from flask import Flask, render_template, request
import os
import random
import json


app = Flask(__name__)

images = []
save_path = 0 


@app.route('/', methods=['GET', 'POST'])
def hello():
    ############################################
    # Ked je vyvolany POST request
    ############################################      
   
    if request.method == 'POST':
        global images
        #print(images)
        
        global save_path       
        #print(save_path)

        ulozena_cesta = save_path 
        pom_list = request.form.getlist('mycheckbox')       
        #print(pom_list)
  
        # final_images je vsetky obrazky - obrazky ktore boli odskrtnute
        final_images = [x for x in images if x not in pom_list]
        #print("FINALNE OBRAZKKY KTORE TREBA ANOTOVAT")
        #print(final_images)

        if request.form['submit_value'] == 'bus':
            annote(ulozena_cesta, final_images, 'bus')                    
            pass
        elif request.form['submit_value'] == 'truck':
            annote(ulozena_cesta, final_images, 'truck') 
            pass        
        elif request.form['submit_value'] == 'minitruck':
            annote(ulozena_cesta, final_images, 'minitruck')
            pass
        elif request.form['submit_value'] == 'car':
            annote(ulozena_cesta, final_images, "car")
            pass
        elif request.form['submit_value'] == 'van':
            annote(ulozena_cesta, final_images, 'van')
            pass
        elif request.form['submit_value'] == 'minivan':
            annote(ulozena_cesta, final_images, 'minivan')
            pass
        
        save_path = load_path()
        images = os.listdir(save_path)
        # v pom je napisana iba cesta "static\obrazky\.."
        # pom odstranuje nepotrebne pismena cesty
        pom = save_path[59:] + "/"          

        # nacitanie pomocneho aby sa odstranili uz vytvorene anotacie
        return render_template('main.html', images=images, pathh=pom)

    else:
        #print("PRVE SPUSTENIE NIE JE REQUEST ESTE VYZIADANY")
        save_path = load_path()        
        images = os.listdir(save_path)
        # v pom je napisana iba cesta "static\obrazky\.."
        # pom odstranuje nepotrebne pismena cesty
        pom = save_path[59:] + "/"
        # textak kde sa budu ukladat pole obrazkov + cesta
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
    final.update({"path": cesta})
    for item in images:
        final.update({item: name_type})
    # Zapisanie dict do jsonu v tvare {'nazov_obrazka': 'nazov_typu'}
    with open(cesta + 'annot.json', 'w') as fp:
        json.dump(final, fp)
    return

if __name__ == "__main__":
    app.run(threaded=True)
