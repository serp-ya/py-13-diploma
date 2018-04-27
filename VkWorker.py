import requests
import math
import time


class VkWorker:
    api_url = 'https://api.vk.com/method'
    params = {
        'access_token': '1fba8861513553efb45c7951a97ddeffb3b5534097126ca538b93' \
                        'fd5f32d80818ac9b2a1972b5971c0e41',
        'v': '5.74',
    }

    def __init__(self, dirty_user_id):
        striped_user_id = dirty_user_id.strip()
        valid_user_id = striped_user_id

        if not valid_user_id.isdecimal():
            params = self.params.copy()
            params['user_ids'] = valid_user_id

            valid_user_id = requests.get(
                self.formatted_url('users.get'),
                params=params
            ).json()['response'][0]['id']

        self.user_id = valid_user_id


    def formatted_url(self, method_name):
        return f'{self.api_url}/{method_name}'


    def make_get_request(self, method_name, user_id=None):
        method_url = self.formatted_url(method_name)

        params = self.params.copy()
        params['user_id'] = user_id or self.user_id

        result = requests.get(method_url, params=params).json()
        time.sleep(0.35)

        return result


    def get_friends(self,):
        return self.make_get_request('friends.get')


    def get_groups(self, user_id=None):
        return self.make_get_request('groups.get', user_id)

    def get_groups_info(self, group_ids):
        method_url = self.formatted_url('groups.getById')
        params = self.params.copy()
        params['fields'] = 'members_count'
        params['group_ids'] = ','.join(map(str, group_ids))

        result = requests.get(method_url, params=params).json()
        time.sleep(0.35)

        return result
