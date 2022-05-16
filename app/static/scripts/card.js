import {Card, refresh, resultToast} from "./requests.js";
const card = new Card();

const elems = document.querySelectorAll('select');
const instances = M.FormSelect.init(elems, {});
const deleteCardButton = document.querySelector('.card-delete');

deleteCardButton.addEventListener('click', async (e) => {
    const cardId = deleteCardButton.dataset.id;
    await card.remove(cardId);
    window.location.replace("http://localhost:8022/");
})

document.addEventListener('change', (e) => {
    const columnId = e.target.value;
    if(columnId) {
        card.update({})
    }

})