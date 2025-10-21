import random
from django.http import JsonResponse
from django.shortcuts import render

MAPS = [
    "契卡洛夫斯克空军基地",
    "里加机场",
    "波罗的斯克半岛",
    "死亡中心",
    "切尔尼亚霍夫斯克",
    "黑海岸",
    "考纳斯水坝",
    "死亡公路",
    "伊格纳利纳核电站",
    "叶尔加瓦",
    "加里宁格勒",
    "克莱佩达裂谷",
    "纳尔瓦冰雪城堡",
    "石油热潮",
    "风啸湾",
    "蜿蜒之河",
    "鲁达森林",
    "苏瓦乌基走廊",
    "寒水港",
]

CLASSES = [
    "美团-海军陆战队",
    "美团-装甲旅",
    "美团-空降部队",
    "美团-特种部队",
    "美团-斯崔克骑兵团",
    "饿了么-VDV旅",
    "饿了么-近卫坦克旅",
    "饿了么-海岸部队",
    "饿了么-摩托化部队",
    "饿了么-机械化部队",
]


def index(request):
    """Render the main UI."""
    return render(request, 'barandom/index.html')


def randomize(request):
    """Return a JSON payload with a random map and random classes for players.

    Query params:
      players - optional integer, default 3
    """
    try:
        players = int(request.GET.get('players', 3))
    except (ValueError, TypeError):
        players = 3

    players = max(1, min(10, players))

    # Parse 'unique' flag from query params. Default to True (enabled).
    unique_param = request.GET.get('unique')
    if unique_param is None:
        unique = True
    else:
        # Accept values like '1', 'true', 'yes' (case-insensitive) as True
        unique = str(unique_param).lower() in ('1', 'true', 'yes', 'on')

    result = {
        'map': random.choice(MAPS),
        'players': [],
        'unique': unique,
    }

    # If unique selection requested, ensure we don't pick more players than available classes.
    if unique:
        if players > len(CLASSES):
            # Limit players to number of classes and add a warning.
            warning = f"请求的玩家数({players})超过可用卡组数量({len(CLASSES)})；已限制为 {len(CLASSES)}。"
            players = len(CLASSES)
            result['warning'] = warning
        chosen = random.sample(CLASSES, players)
        for i, cls in enumerate(chosen):
            result['players'].append({'id': i + 1, 'class': cls})
    else:
        for i in range(players):
            result['players'].append({'id': i + 1, 'class': random.choice(CLASSES)})

    return JsonResponse(result)
