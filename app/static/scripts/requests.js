const HOST = "http://localhost:8022"

export function resultToast({successMessage = 'Успешно!', failMessage = 'Ошибка!', result = true}) {
    const toastClass = result ? 'toast-success' : 'toast-fail';
    const message = result ? successMessage : failMessage;
    M.toast({html: message, classes: toastClass})
}

export function refresh(delay = 500) {
    setTimeout(() => {
        document.location.reload();
    }, delay)

}

export class Desk {

    url = HOST + "/desks/"

    async create(deskTitle) {
        const response = await fetch(this.url,
            {
                method: 'post',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"title": deskTitle})
            }
        );
        return response;
    }

    async remove(deskId) {
        const response = await fetch(this.url,
            {
                method: 'delete',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"id": deskId})
            }
        );
        return response;
    }

    async update(deskId, title) {
        const response = await fetch(this.url,
            {
                method: 'put',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"id": deskId, "title": title})
            }
        );
        return response;
    }
}

export class Column {

    url = HOST + "/columns/"

    async create(title, deskId) {
        const response = await fetch(this.url,
            {
                method: 'post',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"title": title, "desk_id": deskId})
            }
        );
        return response;
    }

    async remove(columnId) {
        const response = await fetch(this.url,
            {
                method: 'delete',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"id": columnId})
            }
        );
        return response;
    }

    // async update(columnId, title, order) {
    async update(columnId, title) {

        const response = await fetch(this.url,
            {
                method: 'put',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"id": columnId, "title": title})
            }
        );
        return response;
    }
}


export class Card {

    url = HOST + "/cards/"

    async create(cardTitle, deskId, columnId) {
        const response = await fetch(this.url,
            {
                method: 'post',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"desk_id": deskId, "column_id": columnId, "title": cardTitle})
            }
        );
        return response;
    }

    async remove(cardId) {
        const response = await fetch(this.url,
            {
                method: 'delete',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"id": cardId})
            }
        );
        return response;
    }

    async update(cardId, title, text, columnId, estimate) {
        const response = await fetch(this.url,
            {
                method: 'put',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"id": cardId, "title": title, "text":text, "column_id": columnId, "estimate":estimate})
            }
        );
        return response;
    }
}

