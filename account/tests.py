from datetime import date
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase


from django.contrib.auth.models import Group
from .models import ExtUser


class AccounTestClass(TestCase):


    @classmethod
    def setUpTestData(cls):
        Group.objects.get_or_create(name='User')

        super().setUpTestData()

    def test_create_and_login(self):
        usr_data = { 'login': 'test-account@test.ru', 'password': '123'}
        usr = ExtUser.objects.create_user(**usr_data)
        self.assertIs(type(usr), ExtUser)

        res = self.client.login(**usr_data)
        self.assertTrue(res)
        self.client.logout()

        usr_data['password'] = 'SuperPuper'
        usr.set_password(usr_data['password'])
        usr.save()

        res = self.client.login(**usr_data)
        self.assertTrue(res)
        self.client.logout()


    def test_load_forms(self):
        resp = self.client.get(reverse('account:login'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('account:signup'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse('account:restore'))
        self.assertEqual(resp.status_code, 200)



class AccountTestApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.get_or_create(name='User')

        super().setUpTestData()


    def test_create_account(self):

        '''
        account/ ^api/$ [name='extuser-list']
        account/ ^api/login/$ [name='extuser-login']
        account/ ^api/logout/$ [name='extuser-logout']
        account/ ^api/restore_access/$ [name='extuser-restore-access']
        account/ ^api/(?P<pk>[^/.]+)/$ [name='extuser-detail']
        '''

        # bad reg user
        usr_data = { 'login': 'test-account-api@test.ru', 'password': 'test-account-api'}
        response = self.client.post(reverse('account:extuser-list'), usr_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content.decode("utf-8"))

        # good reg user
        ext_usr_data = usr_data
        ext_usr_data.update({'password_confirm': usr_data['password'], 'name': 'Вася', 'balance': 1000})
        response = self.client.post(reverse('account:extuser-list'), ext_usr_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.content.decode("utf-8"))
        self.assertEqual(response.data['name'], 'Вася')
        good_user_id = response.data['id']

        #open profile page
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test load no own account
        usr_data_more = { 'login': 'test-account-more@test.ru', 'password': 'more'}
        usr_more = ExtUser.objects.create_user(**usr_data_more)
        self.assertIs(type(usr_more), ExtUser)
        response = self.client.get(reverse('account:extuser-detail', args=[usr_more.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content.decode("utf-8"))

        # load user data
        url_api = reverse('account:extuser-detail', args=[good_user_id])
        response = self.client.get(url_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content.decode("utf-8"))


        # patch data
        data = {'id': 100, 'name': 'Петя', 'birthday': '25/09/1975', 'balance': 1000}
        response = self.client.patch(url_api, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content.decode("utf-8"))
        self.assertEqual(response.data['name'], 'Петя')
        self.assertEqual(response.data['id'], good_user_id)
        self.assertFalse('balance' in response.data)


        good_usr = ExtUser.objects.get(pk=good_user_id)
        self.assertEqual(good_usr.birthday, date(1975, 9, 25))
        self.assertEqual(good_usr.balance, 0)







