import {Desk} from "./requests.js";

const desk = new Desk();

const createDeskButton = document.querySelector('.create-desk');

createDeskButton.addEventListener('click', async () => {
    const deskTitle = prompt("Название доски", "Новая доска");
    const newDesk = await desk.create(deskTitle);
    console.log(newDesk) // todo проверять ошибки
    document.location.reload();
});

// delete desk
document.addEventListener('click', async(e) => {
    const deskId = e.target.dataset.id;

    if(deskId && e.target.classList.contains('desk-delete')) {

        const check = confirm('Вы уверены?')
        if (check) {
            const delDesk = await desk.remove(deskId);
            console.log(delDesk) // todo проверять ошибки
            document.location.reload();
        }
    }

})

// rename desk
document.addEventListener('click', async(e) => {
    const deskId = e.target.dataset.id;

    if(deskId && e.target.classList.contains('desk-rename')) {
        const deskNewTitle = prompt('Название доски', 'Новое имя');
        const updDesk = await desk.update(deskId, deskNewTitle);
        console.log(updDesk) // todo проверять ошибки
        document.location.reload();
    }

})
