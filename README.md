# novaposhta-api-client

Python client for Nova Poshta company's API.


## Configuration

#### Environment variables

If not using django, set `NOVAPOSHTA_API_KEY` and `NOVAPOSHTA_API_POINT` (optional)


#### Django
Add to `settings.py`:
```
NOVAPOSHTA_API_SETTINGS = {
    'api_key': '12345', # your api key, required
    'api_point': 'https://api.novaposhta.ua/v2.0/json/', # default, not required
}
```


## Testing

```
# install deps and enable virtualenv
pipenv shell
# run tests
python setup.py test
```
