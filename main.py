import vk, datetime, matplotlib.pyplot as plt, time


def read_token():
    f = open('token.txt', 'r')
    token = f.read().rstrip('\n')
    f.close()
    return token


def get_age(bday, bmonth, byear):
    now = datetime.datetime.now()
    if bmonth < now.month or (bmonth == now.month and bday <= now.day):
        return now.year-byear
    else:
        return now.year-byear-1


def get_members_info(members, ages, sex):
    for i in range(len(members)):
        user = members[i]
        sex[user['sex']] += 1
        try:
            day, month, year = [int(item) for item in user['bdate'].split('.')]
        except:
            continue
        age = get_age(day, month, year)
        ages[age] = ages.get(age, 0) + 1


def get_data(api, _group_id):
    ages = {}
    sex = [0,0,0]
    _offset = 0
    members_count = api.groups.getById(group_id=_group_id, fields='members_count', v=5.73)[0]['members_count']

    for i in range(members_count//1000 + 1):
        current_members = api.groups.getMembers(group_id=_group_id, offset=_offset, fields='bdate, sex', v=5.73)
        get_members_info(current_members['items'], ages, sex)
        _offset += 1000
        time.sleep(0.2)

    return [ages, sex]


def draw_diagram(ages, sex, group_name):
    pieces = [ages[key] for key in ages]
    _labels = [key for key in ages]
    plt.pie(pieces, labels=_labels, shadow=1, radius=1, startangle=90, autopct='%1.1f%%')
    plt.text(-1.55,-1.5,
             'Number of women: {}\nNumber of men: {}\nGender is not specified: {}'.format(sex[1],sex[2],sex[0]),
             size='large',
             bbox={'fill': False, 'boxstyle': 'round', 'linestyle': 'solid', 'linewidth': 1}
             )
    plt.title('The chart of ages for the members of\n"{}" group'.format(group_name))
    plt.show()


if __name__ == '__main__':

    token = read_token()
    session = vk.Session(access_token=token)
    vk_api = vk.API(session)

    _group_id = input("Enter public's ID or short name: ")
    group_name = vk_api.groups.getById(group_id=_group_id, v=5.73)[0]['name']
    ages, sex = get_data(vk_api, _group_id)
    draw_diagram(ages, sex, group_name)