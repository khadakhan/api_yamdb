from reviews import models

USER_SETTINGS = {
    'model': models.User,
    'is_many_to_many': False,
    'foreign_keys': {},
    'redirect': {}
}

CATEGORY_SETTINGS = {
    'model': models.Category,
    'is_many_to_many': False,
    'foreign_keys': {},
    'redirect': {}
}

COMMENT_SETTINGS = {
    'model': models.Comment,
    'is_many_to_many': False,
    'foreign_keys': {
        'review': models.Review,
        'author': models.User
    },
    'redirect': {'review': 'review_id'}
}

GENRE_SETTINGS = {
    'model': models.Genre,
    'is_many_to_many': False,
    'foreign_keys': {},
    'redirect': {}
}

REVIEW_SETTINGS = {
    'model': models.Review,
    'is_many_to_many': False,
    'foreign_keys': {
        'title': models.Title,
        'author': models.User
    },
    'redirect': {'title': 'title_id'}
}

TITLE_SETTINGS = {
    'model': models.Title,
    'is_many_to_many': False,
    'foreign_keys': {
        'category': models.Category
    },
    'redirect': {}
}

TITLE_GENRE_SETTINGS = {
    'model': models.Title,
    'is_many_to_many': True,
    'foreign_keys': {
        'base_key': 'title_id',
        'connected_key': 'genre_id',
        'connected_model': models.Genre,
        'field': 'genre'
    },
    'redirect': {}
}

NAME_TO_SETTINGS = {
    'category': CATEGORY_SETTINGS,
    'comments': COMMENT_SETTINGS,
    'genre': GENRE_SETTINGS,
    'review': REVIEW_SETTINGS,
    'titles': TITLE_SETTINGS,
    'users': USER_SETTINGS,
    'genre_title': TITLE_GENRE_SETTINGS
}
