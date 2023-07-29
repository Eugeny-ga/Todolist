from collections import namedtuple
from goals.models import BoardParticipant, Goal, GoalCategory, GoalPriority, GoalStatus
from goals.serializers import GoalCategorySerializer, GoalSerializer

GoalData = namedtuple('GoalData', ['title', 'due_date', 'priority', 'status'])
GoalCategoryData = namedtuple('GoalCategoryData', ['cat_id', 'title'])


def get_goals_from_db(user_id: int) -> str:

    priority = dict(GoalPriority.choices)
    status = dict(GoalStatus.choices)

    goals = (
        Goal.objects.select_related('user')
        .filter(category__board__participants__user_id=user_id, category__is_deleted=False)
        .exclude(status=GoalStatus.archived)
        .all()
    )

    if not goals.exists():
        return "Цели еще не созданы"

    # Данные о целях
    data = []
    serializer = GoalSerializer(goals, many=True)
    for item in serializer.data:
        filtered_dict = GoalData(
            title=item['title'],
            due_date=item['due_date'] if item['due_date'] else '',
            priority=priority[item['priority']],
            status=status[item['status']],
        )
        data.append(filtered_dict)

    # Вывод списка целей юзеру
    message = []
    for index, item in enumerate(data, start=1):
        goal = (
            f'{index}) {item.title}, статус: {item.status}, приоритет: {item.priority}, '
            f"{'Срок выполнения: ' + item.due_date if item.due_date else 'не задан'}"
        )
        message.append(goal)

    response = '\n'.join(message)
    return response


def get_categories_from_db(user_id: int, chat_id: int, users_data: dict[int, dict[str | int, ...]]) -> str:
    categories = (
        GoalCategory.objects.select_related('user')
        .filter(
            board__participants__user_id=user_id,
            board__participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        )
        .exclude(is_deleted=True)
    )

    if not categories.exists():
        return "Нет категорий. Создайте новую"

    # Данные о целях
    data = []
    serializer = GoalCategorySerializer(categories, many=True)
    for item in serializer.data:
        category = GoalCategoryData(cat_id=item['id'], title=item['title'])
        data.append(category)

    # Смена хендлера
    users_data[chat_id] = {index: item.cat_id for index, item in enumerate(data, start=1)}
    users_data[chat_id]['next_handler'] = choose_category

    # Вывод списка целей юзеру
    message = [f'{index}) {item.title}' for index, item in enumerate(data, start=1)]

    response = '\n'.join(message)
    return 'Выберите категорию:\n' + response


def choose_category(**kwargs):
    chat_id = kwargs.get('chat_id')
    message = kwargs.get('message')
    users_data = kwargs.get('users_data')

    if message.isdigit():
        value = int(message)
        category_id = users_data.get(chat_id, {}).get(value)
        if category_id is not None:
            users_data[chat_id]['next_handler'] = create_goal
            users_data[chat_id]['category_id'] = category_id
            return f'Вы выбрали {value}. Введите название цели.'
        else:
            return f'Такой категории нет. Попробуйте снова.'
    else:
        return f'Некорректно введен индекс'


def create_goal(**kwargs):
    user_id = kwargs.get('user_id')
    chat_id = kwargs.get('chat_id')
    message = kwargs.get('message')
    users_data = kwargs.get('users_data')
    try:
        category_id = users_data.get(chat_id, {}).get('category_id')
        Goal.objects.create(title=message, user_id=user_id, category_id=category_id)
        users_data.pop(chat_id, None)
        return f'Успешно добавлена цель:"{message}"'

    except Exception as e:
        return f'Произошла ошибка: {str(e)}. Попробуйте создать цель заново.'
