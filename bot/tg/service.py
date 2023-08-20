from collections import namedtuple
from goals.models import BoardParticipant, Goal, GoalCategory, GoalPriority, GoalStatus
from goals.serializers import GoalCategorySerializer, GoalSerializer

GoalData = namedtuple('GoalData', ['title', 'due_date', 'priority', 'status'])
GoalCategoryData = namedtuple('GoalCategoryData', ['cat_id', 'title'])


def get_goals_from_db(user_id: int) -> str:
    """
       Get user goals, filter it by main fields and return it to User Chat

       Args:
           user_id (int): User ID
       Returns:
           str: A message with goals to be sent back to the user.
       """

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

    # Data about goals
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

    # Output a list of goals to the user
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
    """
       Get categories where the user is owner or writer,
       filter them by 'title' and return them to the user chat.

       After the user selects a category by index, prompt the user to enter goal details.

       Args:
           'user_id' (int): User ID
           'chat_id' (int): Telegram Chat ID
       Returns:
           str: A message with categories to be sent back to the user.
       """

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

    # Data about categories
    data = []
    serializer = GoalCategorySerializer(categories, many=True)
    for item in serializer.data:
        category = GoalCategoryData(cat_id=item['id'], title=item['title'])
        data.append(category)

    # Changing the handler
    users_data[chat_id] = {index: item.cat_id for index, item in enumerate(data, start=1)}
    users_data[chat_id]['next_handler'] = choose_category

    # Output a list of categories to the user
    message = [f'{index}) {item.title}' for index, item in enumerate(data, start=1)]

    response = '\n'.join(message)
    return 'Выберите категорию:\n' + response


def choose_category(**kwargs) -> str:
    """
        Handle the user's choice of category by index.

        Args:
            **kwargs: A dictionary containing keyword arguments:
                - chat_id (int): The Telegram chat ID.
                - message (str): The user's message.
                - users_data (Dict[int, Dict[str, Any]]): A dictionary containing user-specific data.

        Returns:
            str: A message to be sent back to the user.
        """
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


def create_goal(**kwargs) -> str:
    """
        Create a new goal based on the user's input.

        Args:
            **kwargs: A dictionary containing keyword arguments:
                - user_id (int): The ID of the user creating the goal.
                - chat_id (int): The Telegram chat ID.
                - message (str): The user's message containing the title of the goal.
                - users_data (Dict[int, Dict[str, Any]]): A dictionary containing user-specific data.

        Returns:
            str: A message to be sent back to the user.
        """

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
