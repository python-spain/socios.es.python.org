from celery.task import task


@task(serializer="json")
def import_consignments_task(consignment_import_pk):
    from pythonspain.banks.models import ConsignmentImport

    try:
        consignment_import = ConsignmentImport.objects.get(pk=consignment_import_pk)
    except ConsignmentImport.DoesNotExist:
        return False
    consignment_import.import_data(async_process=False)
    return consignment_import_pk
