// nazov obrazka
document.getElementById("list_images").getElementsByTagName("input").mycheckbox.value;

// nazov cesty priecinka
document.getElementById("list_images").getElementsByTagName("input").mycheckbox.id;

let pole = [];
let dlza = document.getElementsByTagName('input');
function load_images(){
    for(let i = 0; i < dlza.length; i++){
        pole.push(document.getElementById("list_images").getElementsByTagName("input").mycheckbox.value);
    }
}

console.log(pole);