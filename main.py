from VkWorker import VkWorker
import json
import os

def core():
    print('Введите желаемый id пользователя')
    print('(Для выхода введите C)')
    entered_value = input()

    print('entered_value', entered_value)
    print('entered_value', bool(entered_value))

    if entered_value.lower() == 'c':
        return

    try:
        if entered_value and len(entered_value) > 1 and entered_value.isdigit():
            vk_worker = VkWorker(int(entered_value))

        else:
            vk_worker = VkWorker(entered_value)

        friends_response = vk_worker.get_friends()
        friends_list = friends_response['response']['items']

        groups_response = vk_worker.get_groups()
        groups_list = groups_response['response']['items']

        result = list()

        for group_id in groups_list:
            print(f'Группа {group_id} на проверке')
            has_friends = vk_worker.detect_friend(group_id, friends_list)

            if not has_friends:
                result.append(group_id)

        with open('result.json', 'w', encoding='utf-8') as res:
            print(json.dumps(result), file=res)

    except:
        print('Не корректные данные')

    return core()


if __name__ == '__main__':
    core();
