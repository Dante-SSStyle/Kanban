import {Card, refresh, resultToast} from "./requests.js";
const card = new Card();

const modals = document.querySelectorAll('.modal');
const modalInstances = M.Modal.init(modals, {});
const elems = document.querySelectorAll('select');
const instances = M.FormSelect.init(elems, {});
const deleteCardButton = document.querySelector('.button-card-delete');

deleteCardButton.addEventListener('click', async (e) => {
    const cardId = deleteCardButton.dataset.id;
    const dId = deleteCardButton.dataset.dId
    if (cardId && e.target.classList.contains('button-card-delete')) {
        const delCard = await card.remove(cardId);
        resultToast({successMessage: 'Карточка удалена!', result: delCard.ok});
        window.location.replace("http://localhost:8022/"+dId);
    }
});


// update card
document.addEventListener('click', async (e) => {
    const cardId = e.target.dataset.cardId;
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

        if (cardTitle.length > 50 || cardTitle.length < 1) {
        resultToast({failMessage: 'Имя должно содержать от 1 до 50 символов', result: false});
        }

        else if (cardText.length > 1000) {
        resultToast({failMessage: 'Не более 1000 символов', result: false});
        }

        else if (cardId, cardTitle, cardText, cardCategory, cardEstimate) {
            const updCard = await card.update(cardId, cardTitle, cardText, cardCategory, cardEstimate);
            resultToast({successMessage: 'Карточка изменена!', result: updCard.ok});
            refresh();
        }
        else if (cardId, cardTitle, cardText, cardCategory) {
            const updCard = await card.update(cardId, cardTitle, cardText, cardCategory, null);
            resultToast({successMessage: 'Карточка изменена!', result: updCard.ok});
            refresh();
        }

    }

})
