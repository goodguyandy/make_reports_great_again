from django.shortcuts import render

# Create your views here.
import csv
import datetime
import io
import json
import os
import uuid
import zipfile
from tempfile import TemporaryFile, NamedTemporaryFile

import pdfkit
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView

from core.models import Project, Report, Entry, DomainCredentials
from weasyprint import CSS, HTML
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from martor.utils import LazyEncoder


@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)



            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))





class ProjectListView(ListView):
    model = Project

    def get_queryset(self):
        filtered_projects = Project.objects.filter(owner=self.request.user)
        return filtered_projects


def report_to_pdf_text(report):
    template_pdfRenderer = "export_report.html"  # Refer to the html file I want to render at my PDF at.
    html_string = render_to_string(
        template_pdfRenderer,
        {"report": report},
    )
    f = io.BytesIO()
    html = HTML(string=html_string).write_pdf(
        target=f,
        # stylesheets=[
        #     CSS("core\static\css\material.min.css"),
        #     CSS("core\static\css\sc_require-min.css"),
        # ],
    )
    f.seek(0)
    return f.read()


@login_required
def export_to_pdf(request, pk):
    context = {}
    user = request.user
    queryset = Report.objects.filter(pk=pk, project__owner=user)
    report = get_object_or_404(queryset)
    context["report"] = report
    template_pdfRenderer = "core/report_detail.html"  # Refer to the html file I want to render at my PDF at.

    # Create a Filename of the PDF.
    pdfFileName = "%s_%s" % (
        report.name,
        datetime.datetime.now().strftime("%H%M%S%m%d%Y"),
    )

    # Renders The HTML with Model's Content.
    html_string = render_to_string(
        template_pdfRenderer,
        {"report": report},
    )

    # Let WeasyPrint Get HTML String of ml_string.
    # Input the location from where it would be saved (in server's part / perspective)
    # Add some stylesheets incorporated with the HTMLs. DO NOT INCLUDE CSS INSIDE THESE TEMPLATES AS THEY WON'T WORK.

    f = io.BytesIO()
    html = HTML(string=html_string).write_pdf(
        target=f,
        # stylesheets=[
        #     CSS("core\static\css\material.min.css"),
        #     CSS("core\static\css\sc_require-min.css"),
        # ],
    )
    f.seek(0)
    response = HttpResponse(f.read(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="%s.pdf"' % (pdfFileName)
    return response


# Once we're done, returning to a particular URL.


@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    context["project_list"] = Project.objects.filter(owner=user)
    context["entries"] = Entry.objects.filter(project__owner=user)
    context["high_entries"] = Entry.objects.filter(project__owner=user, risk_score__gte=7)
    context["medium_entries"] = Entry.objects.filter(project__owner=user, risk_score__range=[4, 6])
    context["low_entries"] = Entry.objects.filter(project__owner=user, risk_score__range=[1, 3])
    found_creds =  DomainCredentials.objects.filter(project__owner=user).exclude(data=None).values_list(
        'data', flat=True)
    count = 0
    if found_creds:
        for creds in found_creds:
            count += len(creds)
    context["found_credentials"] = count
    return render(request, 'core/dashboard.html', context=context)


@login_required
def project_detail(request, pk):
    context = {}
    user = request.user
    queryset = Project.objects.filter(pk=pk, owner=user)
    project = get_object_or_404(queryset)
    entries = Entry.objects.filter(project=project)
    domain_creds = DomainCredentials.objects.filter(project=project)
    context["generate_table_report"] = True if entries else False
    context["generate_domain_cred_report"] = True if domain_creds else False
    context["reports"] = Report.objects.filter(project=project)
    context["project"] = project

    return render(request, 'core/project_detail.html', context=context)


@login_required
def report_detail(request, pk):
    context = {}
    user = request.user
    queryset = Report.objects.filter(pk=pk, project__owner=user)
    report = get_object_or_404(queryset)
    context["report"] = report
    return render(request, 'core/report_detail.html', context=context)


@login_required
def project_general_report(request, pk):
    context = {}
    user = request.user
    queryset = Project.objects.filter(pk=pk, owner=user)
    project = get_object_or_404(queryset)
    context["entries"] = project.entry_set.all()
    return render(request, 'core/project_general_report.html', context=context)


@login_required
def download_all_from_project(request, pk):
    queryset = Project.objects.filter(pk=pk, owner=request.user)
    project = get_object_or_404(queryset)
    credentials = DomainCredentials.objects.filter(project=project).exclude(data=None).values_list(
        'data', flat=True)
    credentials = [cred for sublist in credentials for cred in sublist]
    entries = Entry.objects.filter(project=project)

    reports = Report.objects.filter(project=project)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        if reports:
            for report in reports:
                zf.writestr(report.name + ".pdf", report_to_pdf_text(report))
        if credentials:
            writer_file = io.StringIO()
            writer = csv.writer(writer_file)
            writer.writerow(credentials[0].keys())
            for cred in credentials:
                values = list(cred.values())
                writer.writerow(values)
            zf.writestr(project.name + "_credentials" +".csv", writer_file.getvalue())
        if entries:
            html_string = render_to_string(
                "core/project_general_report.html",
                {"entries": entries},
            )

            writer_file = io.BytesIO()
            writer_file.write(html_string.encode())
            writer_file.seek(0)
            zf.writestr(project.name + "_general_report.html", writer_file.read())
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename=f'reports_%s.zip' % (datetime.datetime.now().strftime("%H%M%S%m%d%Y")))


@login_required()
def credentials_table(request, pk ):
    queryset = Project.objects.filter(pk=pk, owner=request.user)
    project = get_object_or_404(queryset)
    credentials = DomainCredentials.objects.filter(project=project).exclude(data=None).values_list(
        'data', flat=True)
    credentials = [cred for sublist in credentials for cred in sublist]
    context = {}
    context["credentials"] = credentials
    context["project"] = project

    return render(request, 'core/credentials_table.html', context=context)


@login_required()
def export_table_as_csv(request, pk):
    queryset = Project.objects.filter(pk=pk, owner=request.user)
    project = get_object_or_404(queryset)
    credentials = DomainCredentials.objects.filter(project=project).exclude(data=None).values_list(
        'data', flat=True)
    credentials = [cred for sublist in credentials for cred in sublist]
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="credentials.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(credentials[0].keys())
    for cred in credentials:
        values = list(cred.values())
        writer.writerow(values)
    return response


def export_general_report(request, pk):
    queryset = Project.objects.filter(pk=pk, owner=request.user)
    project = get_object_or_404(queryset)
    entries = Entry.objects.filter(project=project)
    html_string = render_to_string(
        "core/project_general_report.html",
        {"entries": entries},
    )

    writer_file = io.BytesIO()
    writer_file.write(html_string.encode())
    writer_file.seek(0)
    return FileResponse(writer_file, as_attachment=True,
                        filename=f'report_generale.html')
