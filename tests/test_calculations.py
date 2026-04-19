def test_create_calculation_success(client):
    payload = {
        "expression": "2 + 2",
        "result": 4.0,
    }

    response = client.post("/calculations", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["expression"] == "2 + 2"
    assert data["result"] == 4.0
    assert data["owner_id"] is None


def test_browse_calculations_returns_list(client):
    client.post("/calculations", json={"expression": "5 * 5", "result": 25.0})
    client.post("/calculations", json={"expression": "10 / 2", "result": 5.0})

    response = client.get("/calculations")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(item["expression"] == "5 * 5" for item in data)
    assert any(item["expression"] == "10 / 2" for item in data)


def test_read_calculation_success(client):
    create_response = client.post(
        "/calculations",
        json={"expression": "9 - 4", "result": 5.0},
    )
    calculation_id = create_response.json()["id"]

    response = client.get(f"/calculations/{calculation_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == calculation_id
    assert data["expression"] == "9 - 4"
    assert data["result"] == 5.0


def test_read_calculation_not_found(client):
    response = client.get("/calculations/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Calculation not found"


def test_put_update_calculation_success(client):
    create_response = client.post(
        "/calculations",
        json={"expression": "3 + 3", "result": 6.0},
    )
    calculation_id = create_response.json()["id"]

    update_response = client.put(
        f"/calculations/{calculation_id}",
        json={"expression": "3 + 4", "result": 7.0},
    )

    assert update_response.status_code == 200
    updated = update_response.json()

    assert updated["id"] == calculation_id
    assert updated["expression"] == "3 + 4"
    assert updated["result"] == 7.0


def test_patch_update_calculation_success(client):
    create_response = client.post(
        "/calculations",
        json={"expression": "8 / 2", "result": 4.0},
    )
    calculation_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/calculations/{calculation_id}",
        json={"result": 10.5},
    )

    assert patch_response.status_code == 200
    updated = patch_response.json()

    assert updated["id"] == calculation_id
    assert updated["expression"] == "8 / 2"
    assert updated["result"] == 10.5


def test_update_calculation_not_found(client):
    response = client.put(
        "/calculations/999999",
        json={"expression": "1 + 1", "result": 2.0},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Calculation not found"


def test_delete_calculation_success(client):
    create_response = client.post(
        "/calculations",
        json={"expression": "8 / 2", "result": 4.0},
    )
    calculation_id = create_response.json()["id"]

    delete_response = client.delete(f"/calculations/{calculation_id}")
    assert delete_response.status_code == 204
    assert delete_response.text == ""

    get_response = client.get(f"/calculations/{calculation_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Calculation not found"


def test_delete_calculation_not_found(client):
    response = client.delete("/calculations/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Calculation not found"


def test_create_calculation_invalid_missing_result_returns_422(client):
    response = client.post(
        "/calculations",
        json={"expression": "1 + 1"},
    )

    assert response.status_code == 422


def test_create_calculation_invalid_empty_expression_returns_422(client):
    response = client.post(
        "/calculations",
        json={"expression": "", "result": 2.0},
    )

    assert response.status_code == 422


def test_patch_calculation_invalid_empty_expression_returns_422(client):
    create_response = client.post(
        "/calculations",
        json={"expression": "6 - 1", "result": 5.0},
    )
    calculation_id = create_response.json()["id"]

    response = client.patch(
        f"/calculations/{calculation_id}",
        json={"expression": ""},
    )

    assert response.status_code == 422