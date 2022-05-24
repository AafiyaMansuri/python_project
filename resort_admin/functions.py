def handle_uploaded_file(f):
    with open('resort_admin/static/imgs/'+f.name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def gst(a):
    g = a*(5/100)
    return (g)