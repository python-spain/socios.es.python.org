from celery.task import task


@task(serializer="json")
def partner_export_task(partner_export_pk):
    from pythonspain.partners.models import PartnerExport

    try:
        partner_export = PartnerExport.objects.get(pk=partner_export_pk)
    except PartnerExport.DoesNotExist:
        return False
    partner_export.export_data(async_process=False)
    return partner_export_pk


@task(serializer="json")
def member_export_task(member_export_pk):
    from pythonspain.partners.models import MemberExport

    try:
        member_export = MemberExport.objects.get(pk=member_export_pk)
    except MemberExport.DoesNotExist:
        return False
    member_export.export_data(async_process=False)
    return member_export_pk
