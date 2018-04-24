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



    try:
        if entered_value and len(entered_value) > 1:
            vk_worker = VkWorker(entered_value)

            friends_response = vk_worker.get_friends()
            friends_list = friends_response['response']['items']

            groups_response = vk_worker.get_groups()
            groups_list = groups_response['response']['items']

            # Для демонстрации
            # START
            print('\n############### Для демонстрации')
            friends_count = friends_response['response']['count']
            groups_count = groups_response['response']['count']
            print('friends_count', friends_count)
            print('groups_count', groups_count)
            print('############### Для демонстрации\n')
            # END
            # Для демонстрации

            result = list()

            for i, group in enumerate(groups_list):
                group_id = group['id']

                print(f'Прогресс {to_fixed(i / len(groups_list) * 100)}%')
                print(f'Группа {group_id} на проверке')
                has_friends = vk_worker.detect_friend(group_id, friends_list)

                if not has_friends:
                    group_object = group_object_factory(group)
                    result.append(group_object)

            with open(result_file_name, 'w', encoding='utf-8') as res_file:
                print(json.dumps(result), file=res_file)
                print(f'Результат записан в файл {result_file_name}\n')


        else:
            print('Введены не корректные данные')


    except:
        print('Возникла ошибка, попробуйте ещё раз')


    return core()


if __name__ == '__main__':
    core()
