import {Column, Card, refresh, resultToast} from "./requests.js";

const card = new Card();
const column = new Column();

const modals = document.querySelectorAll('.modal');
const modalInstances = M.Modal.init(modals, {});

const selects = document.querySelectorAll('select');
const selectInstances = M.FormSelect.init(selects, {});

const currentDesk = document.querySelector('.current_desk');


// create column
const createColumnButton = document.querySelector('.button-column-create');
createColumnButton.addEventListener('click', async (e) => {
    const deskId = currentDesk.dataset.deskId;
    const columnTitleInput = document.querySelector('#modal-column-create input');
    const title = columnTitleInput.value;

    if (deskId && title) {
        const newColumn = await column.create(title, deskId);
        resultToast({successMessage: 'Категория созданна!', result: newColumn.ok});
        refresh();
    }

});

// create card
const createCardButton = document.querySelector('.button-card-create');
createCardButton.addEventListener('click', async (e) => {
    const deskId = currentDesk.dataset.deskId;
    const titleInput = document.querySelector('#modal-card-create input');
    const categorySelect = document.querySelector('#modal-card-create select');
    const title = titleInput.value;
    const categoryId = categorySelect.value;

    if (deskId && title) {
        const newCard = await card.create(title, deskId, categoryId);
        resultToast({successMessage: 'Карточка созданна!', result: newCard.ok});
        refresh();
    }

});
