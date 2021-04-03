from django.test import TestCase

from datetime import datetime

from scan.models import User

MAX_STRING_SIZE = 'a' * 250


def _create_user(**data):
    return User.objects.create(**data)


class UserTest(TestCase):
    def test_user_creation(self):
        data = {
            'id': 11,
            'login': 'login',
            'url':MAX_STRING_SIZE,
            'name': MAX_STRING_SIZE,
            'company': MAX_STRING_SIZE,
            'location': MAX_STRING_SIZE,
            'email': MAX_STRING_SIZE,
            'bio': '',
            'twitter_username': 'teste',
            'public_repos': 1,
            'public_gists': 2,
            'followers': 3,
            'following': 4,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        user = _create_user(**data)

        self.assertTrue(isinstance(user, User))
        self.assertEqual(str(user), data['login'])
