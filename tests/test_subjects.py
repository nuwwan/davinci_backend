def test_create_subject(client):
    response = client.post(
        "/subjects/",
        json={"name": "Programming", "description": "Tech subjects"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Programming"


def test_list_subjects(client):
    response = client.get("/subjects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)