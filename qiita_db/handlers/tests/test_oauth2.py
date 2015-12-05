# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from unittest import main
from json import loads
from qiita_pet.test.tornado_test_base import TestHandlerBase


class OAuth2BaseHandlerTests(TestHandlerBase):
    def test_login_client(self):
        pass


class OAuth2HandlerTests(TestHandlerBase):
    def test_authenticate_client(self):
        # Authenticate using header
        obs = self.post(
            '/qiita_db/authenticate/', {'grant_type': 'client'}, {
                'Authorization': 'Basic MTluZGtPM29NS3NvQ2hqVlZXbHVGN1FreEhSZl'
                                 'loVEtTRmJBVnQ4SWhLN2daZ0RhTzQ6SjdGZlE3Q1FkT3'
                                 'h1S2hRQWYxZW9HZ0JBRTgxTnM4R3UzRUthV0ZtM0lPMk'
                                 'pLaEFtbUNXWnVhYmUwTzVNcDI4czE='})
        obs_info = loads(obs.body)
        exp = {'access_token': 'token',
               'token_type': 'Bearer',
               'expires_in': '3600'}
        self.assertItemsEqual(obs_info.keys(), exp.keys())
        self.assertEqual(obs_info['token_type'], exp['token_type'])
        self.assertEqual(obs_info['expires_in'], exp['expires_in'])
        self.assertEqual(len(obs_info['access_token']), 55)
        self.assertEqual(type(obs_info['access_token']), unicode)

        # Authenticate using post only
        obs = self.post(
            '/qiita_db/authenticate/', {
                'grant_type': 'client',
                'client_id': '19ndkO3oMKsoChjVVWluF7QkxHRfYhTKSFbAVt8IhK7gZgDa'
                             'O4',
                'client_secret': 'J7FfQ7CQdOxuKhQAf1eoGgBAE81Ns8Gu3EKaWFm3IO2J'
                                 'KhAmmCWZuabe0O5Mp28s1'})
        obs_info = loads(obs.body)
        exp = {'access_token': 'placeholder',
               'token_type': 'Bearer',
               'expires_in': '3600'}
        self.assertItemsEqual(obs_info.keys(), exp.keys())
        self.assertEqual(obs_info['token_type'], exp['token_type'])
        self.assertEqual(obs_info['expires_in'], exp['expires_in'])
        self.assertEqual(len(obs_info['access_token']), 55)
        self.assertEqual(type(obs_info['access_token']), unicode)

    def test_authenticate_client_bad_info(self):
        # Authenticate using bad header
        obs = self.post(
            '/qiita_db/authenticate/', {'grant_type': 'client'}, {
                'Authorization': 'Basic MTluZGtPM29NS3NvQ2hqVlZXbHVGN1FreEhSZl'
                                 'loVEtTRmJBVnQ4SBADN2daZ0RhTzQ6SjdGZlE3Q1FkT3'
                                 'h1S2hRQWYxZW9HZ0JBRTgxTnM4R3UzRUthV0ZtM0lPMk'
                                 'pLaEFtbUNXWnVhYmUwTzVNcDI4czE='})
        obs_info = loads(obs.body)
        exp = {'error': 'Invalid request'}
        self.assertEqual(obs_info, exp)

        obs = self.post(
            '/qiita_db/authenticate/', {'grant_type': 'client'}, {
                'Authorization': 'WRONG MTluZGtPM29NS3NvQ2hqVlZXbHVGN1FreEhSZl'
                                 'loVEtTRmJBVnQ4SWhLN2daZ0RhTzQ6SjdGZlE3Q1FkT3'
                                 'h1S2hRQWYxZW9HZ0JBRTgxTnM4R3UzRUthV0ZtM0lPMk'
                                 'pLaEFtbUNXWnVhYmUwTzVNcDI4czE='})
        obs_info = loads(obs.body)
        exp = {'error': 'Invalid request'}
        self.assertEqual(obs_info, exp)

        # Test with bad client ID
        obs = self.post(
            '/qiita_db/authenticate/', {
                'grant_type': 'client',
                'client_id': 'BADdkO3oMKsoChjVVWluF7QkxHRfYhTKSFbAVt8IhK7gZgDa'
                             'O4',
                'client_secret': 'J7FfQ7CQdOxuKhQAf1eoGgBAE81Ns8Gu3EKaWFm3IO2J'
                                 'KhAmmCWZuabe0O5Mp28s1'})
        obs_info = loads(obs.body)
        exp = {'error': 'Invalid request'}
        self.assertEqual(obs_info, exp)

        # Test with bad client secret
        obs = self.post(
            '/qiita_db/authenticate/', {
                'grant_type': 'client',
                'client_id': '19ndkO3oMKsoChjVVWluF7QkxHRfYhTKSFbAVt8IhK7gZgDa'
                             'O4',
                'client_secret': 'BADfQ7CQdOxuKhQAf1eoGgBAE81Ns8Gu3EKaWFm3IO2J'
                                 'KhAmmCWZuabe0O5Mp28s1'})
        obs_info = loads(obs.body)
        exp = {'error': 'Invalid request'}
        self.assertEqual(obs_info, exp)

    def test_authenticate_password(self):
        # Authenticate with client_id of a non-user
        obs = self.post(
            '/qiita_db/authenticate/', {
                'grant_type': 'password',
                'client_id': 'DWelYzEYJYcZ4wlqUp0bHGXojrvZVz0CNBJvOqUKcrPQ5p4U'
                             'qE',
                'username': 'test@foo.bar',
                'password': 'password'})
        obs_info = loads(obs.body)
        exp = {'access_token': 'placeholder',
               'token_type': 'Bearer',
               'expires_in': '3600'}
        self.assertItemsEqual(obs_info.keys(), exp.keys())
        self.assertEqual(obs_info['token_type'], exp['token_type'])
        self.assertEqual(obs_info['expires_in'], exp['expires_in'])
        self.assertEqual(len(obs_info['access_token']), 55)
        self.assertEqual(type(obs_info['access_token']), unicode)

    def test_authenticate_password_bad_info(self):
        # Authenticate with client_id of a non-user
        obs = self.post(
            '/qiita_db/authenticate/', {
                'grant_type': 'password',
                'client_id': '19ndkO3oMKsoChjVVWluF7QkxHRfYhTKSFbAVt8IhK7gZgDa'
                             'O4',
                'username': 'test@foo.bar',
                'password': 'password'})
        obs_info = loads(obs.body)
        exp = {'error': 'Invalid request'}
        self.assertEqual(obs_info, exp)

        # Authenticate with bad client_id
        # Authenticate with client_id of a non-user
        obs = self.post(
            '/qiita_db/authenticate/', {
                'grant_type': 'password',
                'client_id': 'WAAAAAAAAAARG',
                'username': 'test@foo.bar',
                'password': 'password'})
        obs_info = loads(obs.body)
        exp = {'error': 'Invalid request'}
        self.assertEqual(obs_info, exp)

        # Authenticate with bad username
        obs = self.post(
            '/qiita_db/authenticate/', {
                'grant_type': 'password',
                'client_id': 'DWelYzEYJYcZ4wlqUp0bHGXojrvZVz0CNBJvOqUKcrPQ5p4U'
                             'qE',
                'username': 'BROKEN@FAKE.COM',
                'password': 'password'})
        obs_info = loads(obs.body)
        exp = {'error': 'Invalid request'}
        self.assertEqual(obs_info, exp)

        # Authenticate with bad password
        obs = self.post(
            '/qiita_db/authenticate/', {
                'grant_type': 'password',
                'client_id': 'DWelYzEYJYcZ4wlqUp0bHGXojrvZVz0CNBJvOqUKcrPQ5p4U'
                             'qE',
                'username': 'test@foo.bar',
                'password': 'NOTAReALPASSworD'})
        obs_info = loads(obs.body)
        exp = {'error': 'Invalid request'}
        self.assertEqual(obs_info, exp)

if __name__ == "__main__":
    main()
