const HOST = "http://localhost:8022"

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
        return await response.json();
    }

    async remove(deskId) {
        const response = await fetch(this.url,
            {
                method: 'delete',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"id": deskId})
            }
        );
        return await response.json();
    }

    async update(deskId, deskTitle) {
        const response = await fetch(this.url,
            {
                method: 'put',
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify({"id": deskId, "title": deskTitle})
            }
        );
        return await response.json();
    }
}

