from .data.mock_data import *
from api.common_views import get_qs_role, prices_f
class TestPriceMock(TestCase):
    fixtures = ['myCustomUsers.json']
    @mock.patch('main.test_mock.CustomUserRepository.read_filtered')
    @mock.patch('main.test_mock.CustomersRepository.read_filtered')
    @mock.patch('main.test_mock.SpecialOffersRepository.read_all')
    @mock.patch('main.test_mock.PricesRepository.read_all')
    def test_price_mock(self, prices_rep, offers_rep, customers_rep, custom_user_rep):

        prices_rep.return_value = prices_qs
        offers_rep.return_value = offers_qs
        customers_rep.return_value = customer_qs_for_read_filtered
        custom_user_rep.return_value = customer_users_list_for_read_filtered

        request_mock = mock.Mock(user=super_user)
        request_mock.return_value = 200

        result_data = prices_f(request_mock)

        self.assertEqual(len(result_data['special_offers']), len(offers_qs))
        self.assertEqual(len(result_data['prices']), len(prices_qs))

        for i in range(len(offers_qs)):
            self.assertEqual(result_data['special_offers'][i], offers_qs[i])

        for i in range(len(prices_qs)):
            self.assertEqual(result_data['prices'][i], prices_qs[i])

    @mock.patch('main.test_mock.CustomUserRepository.read_filtered')
    @mock.patch('main.test_mock.CustomersRepository.read_filtered')
    def test_role_customer_mock(self, customers_rep, users_rep):
        customers_rep.return_value = customer_qs_for_read_filtered
        users_rep.return_value = customer_users_list_for_read_filtered
        request_mock = mock.Mock(user=customer_user)
        request_mock.return_value = 200
        right_answer = (True, customer, False, None, False, None, False, customer_user)

        result_data = get_qs_role(request_mock)

        self.assertEqual(result_data, right_answer)

    @mock.patch('main.test_mock.CustomUserRepository.read_filtered')
    @mock.patch('main.test_mock.InstructorsRepository.read_filtered')
    def test_role_instructor_mock(self, instructors_rep, users_rep):
        instructors_rep.return_value = instructor_qs_for_read_filtered
        users_rep.return_value = instructor_users_qs_for_read_filtered
        request_mock = mock.Mock(user=instructor_user)
        request_mock.return_value = 200
        right_answer = (False, None, True, instructor, False, None, False, instructor_user)

        result_data = get_qs_role(request_mock)

        self.assertEqual(result_data, right_answer)

    @mock.patch('main.test_mock.CustomUserRepository.read_filtered')
    @mock.patch('main.test_mock.AdministratorsRepository.read_filtered')
    def test_role_admin_mock(self, admins_rep, users_rep):
        admins_rep.return_value = admin_qs_for_read_filtered
        users_rep.return_value = admin_users_qs_for_read_filtered
        request_mock = mock.Mock(user=admin_user)
        request_mock.return_value = 200
        right_answer = (False, None, False, None, True, admin, False, admin_user)

        result_data = get_qs_role(request_mock)

        self.assertEqual(result_data, right_answer)



