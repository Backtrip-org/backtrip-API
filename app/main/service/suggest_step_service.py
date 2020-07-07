from collections import Counter

from app.main.model.step.step_leisure import StepLeisure
from app.main.model.user import User


def suggest_step(user_id):
    steps_by_users = get_steps_by_users()

    requesting_user_steps = steps_by_users[user_id]
    del steps_by_users[user_id]

    similar_users_steps = get_similar_user_steps(steps_by_users, requesting_user_steps)
    steps = combine_steps(similar_users_steps)
    remove_requesting_user_steps(steps, requesting_user_steps[0: 3])

    steps = sort_user_steps_by_occurrence(steps)

    return convert_step(steps)

def get_steps_by_users():
    steps_by_users = count_step_occurrence_by_users()
    steps_by_users = sort_users_steps_by_occurrence(steps_by_users)
    steps_by_users = get_top_4(steps_by_users)

    return steps_by_users

def count_step_occurrence_by_users():
    users = User.query.all()
    leisure_steps_by_users = get_leisure_steps_by_users(users)
    leisure_steps_occurrence_by_users = get_leisure_steps_occurrence_by_users(leisure_steps_by_users)

    return leisure_steps_occurrence_by_users

def get_leisure_steps_by_users(users):
    leisure_steps_by_users = dict()
    for user in users:
        leisure_steps_by_users[user.id] = get_leisure_steps(user.users_steps)
    return leisure_steps_by_users

def get_leisure_steps(steps):
    leisure_steps = list(filter(step_is_leisure, steps))
    leisure_steps_name = list(map(lambda step: step.name, leisure_steps))
    return leisure_steps_name

def step_is_leisure(step):
    return isinstance(step, StepLeisure)

def get_leisure_steps_occurrence_by_users(leisure_steps_by_users):
    for user in leisure_steps_by_users.keys():
        leisure_steps_by_users[user] = Counter(leisure_steps_by_users[user])
    return leisure_steps_by_users

def sort_users_steps_by_occurrence(steps_by_users):
    for user in steps_by_users.keys():
        steps_by_users[user] = sort_user_steps_by_occurrence(steps_by_users[user])
    return steps_by_users

def sort_user_steps_by_occurrence(steps_by_user):
    sorted_occurrence = sorted(list(steps_by_user.items()), key=lambda t: t[1], reverse=True)
    return sorted_occurrence

def get_top_4(steps_by_users):
    for user in steps_by_users.keys():
        steps_by_users[user] = steps_by_users[user][0:4]
    return steps_by_users

def get_similar_user_steps(steps_by_users, requesting_user):
    similar_users = []
    for user in steps_by_users.keys():
        if user_is_similar(steps_by_users[user], requesting_user):
            similar_users.append(steps_by_users[user])
    return similar_users

def user_is_similar(user_to_check, reference_user):
    reference_user_steps = list(map(get_step_occurrence_step_name, reference_user))[0:3]
    user_to_check_steps = list(map(get_step_occurrence_step_name, user_to_check))[0:3]
    intersection = list(set(reference_user_steps).intersection(user_to_check_steps))

    return len(intersection) > 1

def get_step_occurrence_step_name(step_occurrence):
    return step_occurrence[0]

def combine_steps(similar_users_steps):
    combined_steps = dict()
    for steps_occurrence in similar_users_steps:
        for step_occurrence in steps_occurrence:
            step = step_occurrence[0]
            occurrence = step_occurrence[1]
            if step not in combined_steps.keys():
                combined_steps[step] = 0
            combined_steps[step] = combined_steps[step] + occurrence
    return combined_steps

def remove_requesting_user_steps(steps, steps_to_remove):
    for step in steps_to_remove:
        del steps[step[0]]

def convert_step(steps):
    result = []
    for step in steps:
        result.append({'name': step[0], 'occurrence': step[1]})
    return result
