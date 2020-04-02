import csv


def basic_exporter(queryset, output, fieldnames):
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=",")
    writer.writeheader()
    items = 0
    for model in queryset.iterator():
        row = dict()
        for field_name in fieldnames:
            row[field_name] = getattr(model, field_name)
        writer.writerow(row)
        items += 1
    return items
