from urllib.parse import urlencode
import requests
import math
import time


class VkWorker:
    api_url = 'https://api.vk.com/method'
    params = {
        'access_token': '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b' \
            '480b7d9fb59859870658c4a0b8fdc4dd494db19099',
        'v': '5.74',
    }

    def __init__(self, user_id):
        self.user_id = user_id


    def formatted_url(self, method_name):
        return f'{self.api_url}/{method_name}'


    def make_get_request(self, method_name):
        method_url = self.formatted_url(method_name)

        params = self.params.copy()
        params['user_id'] = self.user_id

        return requests.get(method_url, params=params).json()


    def get_friends(self):
        return self.make_get_request('friends.get')


    def get_groups(self):
        return self.make_get_request('groups.get')


    def detect_friend(self, group_id, user_ids):
        method_url = self.formatted_url('groups.isMember')
        params = self.params.copy()
        params['group_id'] = group_id
        per_request_ids_count = 250
        result = False

        iterations = math.ceil(len(user_ids) / per_request_ids_count)

        for i in range(iterations):
            count_start = i * per_request_ids_count
            count_finish = (i + 1) * per_request_ids_count
            params_of_part = params.copy()
            user_ids_part = user_ids[count_start:count_finish]

            params_of_part['user_ids'] = ','.join(map(str, user_ids_part))

            detect_response = requests.get(method_url, params=params_of_part).json()
            detect__users = detect_response['response']

            friends_in_group = [*filter(
                lambda item: item['member'] == 1,
                detect__users
            )]

            if len(friends_in_group) > 0:
                result = True
                time.sleep(0.35)
                break

            elif i < iterations - 1:
                time.sleep(0.35)

        return result