from reviews import models

USER_SETTINGS = {
    'model': models.User,
    'is_many_to_many': False,
    'foreign_keys': {}
}

CATEGORY_SETTINGS = {
    'model': models.Category,
    'is_many_to_many': False,
    'foreign_keys': {}
}

COMMENT_SETTINGS = {
    'model': models.Comment,
    'is_many_to_many': False,
    'foreign_keys': {
        'rewiew': models.Review,
        'author': models.User
    }
}

GENRE_SETTINGS = {
    'model': models.Genre,
    'is_many_to_many': False,
    'foreign_keys': {}
}

REVIEW_SETTINGS = {
    'model': models.Review,
    'is_many_to_many': False,
    'foreign_keys': {
        'title_id': models.Title,
        'author': models.User
    }
}

TITLE_SETTINGS = {
    'model': models.Title,
    'is_many_to_many': False,
    'foreign_keys': {
        'category': models.Category
    }
}

TITLE_GENRE_SETTINGS = {
    'model': models.Title,
    'is_many_to_many': True,
    'foreign_keys': {
        'base_key': 'title_id',
        'connected_key': 'genre_id',
        'connected_model': models.Genre,
        'field': 'genre'
    }
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
