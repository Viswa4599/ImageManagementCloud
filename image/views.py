
from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
from PIL import Image
from PIL.ExifTags import TAGS
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['testdb']

# Create your views here. 
def image_view(request): 
  
    if request.method == 'POST': 
        form = ImageForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            print(form.cleaned_data)
            image_table = db.image_image
            filename = str(form.cleaned_data['image'])
            image_id = image_table.find_one({'image':'images'+'/'+filename})['id']
            path= 'media/images/'+filename
            image = Image.open(path)
            exifdata = image.getexif()
            metadata = {"name":filename,'id':image_id}
            for tag_id in exifdata:
           # get the tag name, instead of human unreadable tag id
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                # decode bytes 
                if isinstance(data, bytes):
                    data = data.decode()
                print(f"{tag}: {data}")
                metadata.update({tag:str(data)})
            metacollection = db.metacollection
            result  = metacollection.insert_one(metadata)
            print('One post: {0}'.format(result.inserted_id))
            data = {'success':True,'message': 'Upload and metadata extraction succesful','form':ImageForm()}
            return render(request,'upload.html',data)  
    else: 
        form = ImageForm() 
    data = {'form' : form,'success':False}
    return render(request, 'upload.html',data) 
  
def search_view():
    return 0
#def success(request): 
#    return HttpResponse('successfully uploaded') 
