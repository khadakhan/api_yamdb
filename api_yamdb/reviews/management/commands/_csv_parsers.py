import csv


def csv_parse(file, row_parser, *args):
    with open(file[0].name, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_parser(row, *args)


def standart_row_parse(row, foreign_keys, model):
    for foreign_key, model_foreign_key in foreign_keys.items():
        row[foreign_key] = model_foreign_key.objects.get(
            pk=row[foreign_key])
    model.objects.get_or_create(**row)


def many_to_many_row_parse(row, foreign_keys, model):
    base_instanse = model.objects.get(pk=row[foreign_keys['base_key']])
    connecting_instanse = foreign_keys['connected_model'].objects.get(
        pk=row[foreign_keys['connected_key']])
    getattr(base_instanse, foreign_keys['field']).add(connecting_instanse)
