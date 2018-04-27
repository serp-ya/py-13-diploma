from VkWorker import VkWorker
import json


def to_fixed(number):
    return'{:.2f}'.format(number)


def group_object_factory(group):
    return {
        'name': group['name'],
        'gid': group['id'],
        'members_count': group['members_count'],
    }


def core():
    result_file_name = 'groups.json'
    print('Введите желаемый id пользователя')
    print('(Для выхода введите C)')
    entered_value = input()

    if entered_value.lower() == 'c':
        return

    if entered_value and len(entered_value) > 1:
        vk_worker = VkWorker(entered_value)

        friends_response = vk_worker.get_friends()
        friends_list = friends_response['response']['items']

        victim_groups_response = vk_worker.get_groups()
        victim_groups_list = set(victim_groups_response['response']['items'])

        friends_groups = set()

        print('Идёт поиск групп...')

        for i, friend_id in enumerate(friends_list):
            print(f'Прогресс {to_fixed(i / len(friends_list) * 100)}%')

            resp = vk_worker.get_groups(friend_id)

            try:
                friend_groups = resp['response']['items']
                friends_groups.update(friend_groups)
            except:
                'do nothing'

        print('Подводим итоги...')
        intersection_groups = set.intersection(victim_groups_list, friends_groups)
        unique_groups = set.difference(victim_groups_list, intersection_groups)
        result = list()

        if len(unique_groups):
            unique_groups_full_info = vk_worker.get_groups_info(unique_groups)['response']

            for group in unique_groups_full_info:
                formated_group_info = group_object_factory(group)
                result.append(formated_group_info)

        with open(result_file_name, 'w', encoding='utf8') as res_file:
            res_file.write(json.dumps(result, ensure_ascii=False))

            print(f'Результат записан в файл {result_file_name}\n')


    else:
        print('Введены не корректные данные')


    return core()


if __name__ == '__main__':
    core()
