import pytest

from src.common.settings import TG_URL_PATH, MS_REDIRECT_URI_PATH


@pytest.mark.parametrize('url, status', [
    ('/', 404),
    (TG_URL_PATH, 405),
    (MS_REDIRECT_URI_PATH, 200)
])
def test_get_paths(client, url, status):
    resp = client.get(url)
    assert resp.status_code == status


@pytest.mark.parametrize('url, status', [
    (TG_URL_PATH, 403)
])
def test_post_paths(client, url, status):
    resp = client.post(url)
    assert resp.status_code == status
