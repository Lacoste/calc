from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render

from .common import (add_generic_form_error,
                     get_nested_item, get_deserialized_gleaned_data)
from .. import forms
from ..decorators import handle_cancel
from ..management.commands.initgroups import ANALYZE_PRICES_PERMISSION
from frontend import ajaxform
from frontend.steps import Steps
from ..schedules import registry
from ..analysis.core import analyze_gleaned_data
from ..analysis.export import AnalysisExport
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage



@login_required
@permission_required(ANALYZE_PRICES_PERMISSION, raise_exception=True)
@require_http_methods(["GET","POST"])
def add_capability_statment(request):
    form_submitted = 0
    #print(request.FILES['capability_file'])
    if request.method == 'POST' and request.FILES['capability_file']:
        myfile = request.FILES['capability_file']
        fs = FileSystemStorage()

        #deleting if the contract number alreay there
        if os.path.exists(os.getcwd()+"/calc/capability_statement_files/"+str(request.POST['contract_number'])+".pdf"):
            os.remove(os.getcwd()+"/calc/capability_statement_files/"+str(request.POST['contract_number'])+".pdf")
        if os.path.exists(os.getcwd()+"/calc/capability_statement_files/"+str(request.POST['contract_number'])+".docx"):
            os.remove(os.getcwd()+"/calc/capability_statement_files/"+str(request.POST['contract_number'])+".docx")

        filename_arry = myfile.name.split('.')
        file_extension = filename_arry[-1]
        filename = fs.save(os.getcwd()+"/calc/capability_statement_files/"+str(request.POST['contract_number']+"."+file_extension), myfile)
        try:
            uploaded_file_status = "File Uploaded Successfully"
            form_submitted = 1
        except:
            uploaded_file_status = "Error While File Uploading"
            form_submitted = 2
        return render(request, '../../data_explorer/templates/step_cap.html', {
            'uploaded_file_status': uploaded_file_status,
            'form_submitted' : form_submitted
        })
    return render(request,'../../data_explorer/templates/step_cap.html',{'uploaded_file_url':"Error While File Uploading",'form_submitted' : form_submitted})