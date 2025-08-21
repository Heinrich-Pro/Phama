from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import InventoryLog

@login_required
def inventory_log_list(request):
    if not request.user.is_staff:
        return render(request, 'inventory/permission_denied.html')
    logs = InventoryLog.objects.all().order_by('-date')
    return render(request, 'inventory/log_list.html', {'logs': logs})