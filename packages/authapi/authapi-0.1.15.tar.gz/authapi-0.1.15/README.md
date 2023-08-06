# AuthAPI

A Simple Python API for Authenticated Operations.

![landing_img](https://raw.githubusercontent.com/manucalop/authapi/main/docs/img/landing.png)

## Quickstart:

Let's assume you want to interact with Google Ads API.

1. Create `my_secret.json` with the following information:

```json
{
    "client_id": "",
    "client_secret": "",
    "authorize_url": "",
    "access_token_url": "",
    "scopes": []
}

```

2. Create a `main.py` script and paste the following content.

```python
from authapi import AuthAPI, AuthData

class JsonSecret:
    def __init__(self, path: str):
        self.path = path

    def pull(self) -> dict:
        with open(self.path, "r") as f:
            return json.load(f)

    def push(self, payload: dict) -> None:
        with open(self.path, "w") as f:
            json.dump(payload, f)

app_secret = JsonSecret("my_secret.json")
app_token = JsonSecret("my_token.json")

auth_data = AuthData(**app_secret.pull())

app = AuthAPI(
    name="Auth API: My Auth API",
    auth_data=auth_data,
    token_secret=app_token,
)

app.debug = True


@app.route("/run", methods=["GET", "POST"])
def run():
    token = app.get_token()
    # Do your stuff here
    return "Done!"


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
```

3. Run `python main.py` and visit [https://127.0.0.1:5000/](https://127.0.0.1:5000/) to start the authentication process.
