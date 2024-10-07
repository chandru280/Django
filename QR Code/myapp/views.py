from .models import *
from myapp.forms import *
from django.shortcuts import get_object_or_404, render, redirect

from django.urls import reverse
from django.core.files import File
from io import BytesIO
from PIL import Image
import qrcode


def add_qrcode(request):
    form = SampleForm()

    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            sample_instance = form.save()
            sample_url = request.build_absolute_uri(reverse('sample_detail', args=[sample_instance.id]))
            qr_image = qrcode.make(sample_url)
            qr_offset = Image.new('RGB', (410, 410), 'white')
            qr_offset.paste(qr_image)
            stream = BytesIO()
            qr_offset.save(stream, 'PNG')
            qr_offset.close()
            Qrcode.objects.create(
                name=sample_instance,
                code=File(stream, name=f'{sample_instance.name}_{sample_instance.id}_qr.png')
            )
            return redirect('qrcode_detail', qrcode_id=Qrcode.objects.get(name=sample_instance).id)

    return render(request, 'add_qrcode.html', {
        'form': form
    })



def sample_detail(request, pk):
    qrcode_instance = get_object_or_404(Sample, id=pk)
    return render(request, 'sample_detail.html', {'qrcode': qrcode_instance})


def qrcode_detail(request, qrcode_id):
    qrcode_instance = get_object_or_404(Qrcode, id=qrcode_id)
    return render(request, 'qrcode_detail.html', {'qrcode': qrcode_instance})
