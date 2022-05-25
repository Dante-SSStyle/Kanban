import {Card, refresh, resultToast} from "./requests.js";
const card = new Card();

const modals = document.querySelectorAll('.modal');
const modalInstances = M.Modal.init(modals, {});
const elems = document.querySelectorAll('select');
const instances = M.FormSelect.init(elems, {});
const deleteCardButton = document.querySelector('.card-delete');

deleteCardButton.addEventListener('click', async (e) => {
    const cardId = deleteCardButton.dataset.id;
    const dId = deleteCardButton.dataset.dId
    // await card.remove(cardId);
    // window.location.replace("http://localhost:8022/");
    if (cardId && e.target.classList.contains('card-delete')) {
        const delCard = await card.remove(cardId);
        resultToast({successMessage: 'Карточка удалена!', result: delCard.ok});
        window.location.replace("http://localhost:8022/"+dId);
    }
});

// document.addEventListener('change', (e) => {
//     const columnId = e.target.value;
//     if(columnId) {
//         card.update({})
//     }
//
// })

// update card
document.addEventListener('click', async (e) => {
    const cardId = e.target.dataset.cardId;
    console.log(cardId)
    if (cardId && e.target.classList.contains('button-card-update')) {
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