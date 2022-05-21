import {Column, Card, refresh, resultToast} from "./requests.js";

const card = new Card();
const column = new Column();

const modals = document.querySelectorAll('.modal');
const modalInstances = M.Modal.init(modals, {});

const selects = document.querySelectorAll('select');
const selectInstances = M.FormSelect.init(selects, {});

const drops = document.querySelectorAll('.dropdown-trigger');
const dropInstances = M.Dropdown.init(drops);

const currentDesk = document.querySelector('.col-id-btn');
const currentColumn = document.querySelector('.current_column');

//columns focus
document.addEventListener('click', (e) => {
    const columnId = e.target.dataset.columnId;
    if (columnId) {
        currentColumn.dataset.columnId = columnId;
    }
})


// create column
const createColumnButton = document.querySelector('.button-column-create');
createColumnButton.addEventListener('click', async (e) => {
    const deskId = currentDesk.dataset.deskId;
    // const deskId = e.target.dataset.deskId;
    const columnTitleInput = document.querySelector('#modal-column-create input');
    const title = columnTitleInput.value;

    if (deskId && title) {
        const newColumn = await column.create(title, deskId);
        resultToast({successMessage: 'Категория созданна!', result: newColumn.ok});
        refresh();
    }

});

//rename column
document.addEventListener('click', async (e) => {
    const columnId = currentColumn.dataset.columnId;
    if (columnId && e.target.classList.contains('button-col-rename')) {
        const modal = e.target.closest('.modal');
        const colTitleInput = modal.querySelector('input')
        const colTitle = colTitleInput.value;

        if (colTitle) {
            const updCol = await column.update(columnId, colTitle);
            resultToast({successMessage: 'Столбец переименован!', result: updCol.ok});
            refresh();
        }

    }

})

// delete column
document.addEventListener('click', async (e) => {
    const columnId = currentColumn.dataset.columnId;
    if (columnId && e.target.classList.contains('button-col-delete')) {
        const delCol = await column.remove(columnId);
        resultToast({successMessage: 'Столбец удалён!', result: delCol.ok});
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

// update card
document.addEventListener('click', async (e) => {
    const cardId = currentColumn.dataset.columnId;
    if (cardId && e.target.classList.contains('button-card-upd')) {
        const modal = e.target.closest('.modal');
        const cardTitleInput = modal.querySelector('#title-rename')
        const cardTitle = cardTitleInput.value;
        const cardTextInput = modal.querySelector('#text-upd')
        const cardEstimateInput = modal.querySelector('#estimate')
        const cardCategoryUpdate = modal.querySelector('#col-upd')
        const cardText = cardTextInput.value;
        const cardEstimate = cardEstimateInput.value;
        const cardCategory = cardCategoryUpdate.value;

        console.log(cardId, cardCategory, cardEstimate, cardText, cardTitle)
        if (cardId, cardTitle, cardText, cardCategory, cardEstimate) {
            const updCard = await card.update(cardId, cardTitle, cardText, cardCategory, cardEstimate);
            resultToast({successMessage: 'Карточка изменена!', result: updCard.ok});
            refresh();
        }
        if (cardId, cardTitle, cardText, cardCategory) {
            const updCard = await card.update(cardId, cardTitle, cardText, cardCategory, null);
            resultToast({successMessage: 'Карточка изменена!', result: updCard.ok});
            refresh();
        }

    }

})

// delete card
document.addEventListener('click', async (e) => {
    const cardId = currentColumn.dataset.columnId;
    if (cardId && e.target.classList.contains('button-card-delete')) {
        const delCard = await card.remove(cardId);
        resultToast({successMessage: 'Карточка удалена!', result: delCard.ok});
        refresh();
    }
});
