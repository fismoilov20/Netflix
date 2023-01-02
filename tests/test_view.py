from filmapp.views import *
from unittest import TestCase
from rest_framework.test import APIClient


class TestActorsView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()


        return super().setUp()

    def test_get_actors(self):
        result = self.client.get('/actors/')
        assert result.status_code == 200

    def test_get_actor(self):
        result = self.client.get('/actors/2/')
        assert result.status_code == 200


class TestMoviesView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        return super().setUp()

    def test_get(self):
        result = self.client.get('/movies/')
        assert result.status_code == 200