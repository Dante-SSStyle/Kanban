import {Desk, refresh, resultToast} from "./requests.js";

const desk = new Desk();

const modals = document.querySelectorAll('.modal');
const instances = M.Modal.init(modals, {});

const currentDesk = document.querySelector('.current_desk');

// desk focus
document.addEventListener('click', (e) => {
    const deskId = e.target.dataset.deskId;
    if (deskId) {
        currentDesk.dataset.deskId = deskId;
    }
})


// create desk
const createDeskButton = document.querySelector('.button-desk-create');
createDeskButton.addEventListener('click', async () => {
    const deskTitleInput = document.querySelector('#modal-desk-create input');
    const deskTitle = deskTitleInput.value;
    if (deskTitle) {
        const newDesk = await desk.create(deskTitle);
        resultToast({successMessage: 'Доска созданна!', result: newDesk.ok});
        refresh();
    }

});


// rename desk
document.addEventListener('click', async (e) => {
    const deskId = currentDesk.dataset.deskId;

    if (deskId && e.target.classList.contains('button-desk-rename')) {
        const modal = e.target.closest('.modal');
        const deskTitleInput = modal.querySelector('input')
        const deskTitle = deskTitleInput.value;

        if (deskTitle) {
            const updDesk = await desk.update(deskId, deskTitle);
            resultToast({successMessage: 'Доска переименованна!', result: updDesk.ok});
            refresh();
        }

    }

})


// delete desk
document.addEventListener('click', async (e) => {
    const deskId = currentDesk.dataset.deskId;

    if (deskId && e.target.classList.contains('button-desk-delete')) {
        const delDesk = await desk.remove(deskId);
        resultToast({successMessage: 'Доска удалена!', result: delDesk.ok});
        refresh();

    }

})
