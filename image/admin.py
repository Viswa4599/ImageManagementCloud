from django.contrib import admin
from django.contrib import messages
from image.models import Image
from pymongo import MongoClient
import os
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['testdb']

# Register your models here.

class ImageAdmin(admin.ModelAdmin):

    def delete_cascade_meta(modeladmin, request, queryset): 
        row  = list(queryset.values_list())
        for i in range(0,len(row)):
            image_id = row[i][0]
            image_table = db.image_image
            metacollection = db.metacollection

            #deleting file
            file_path = 'media/'+image_table.find_one({"id":image_id})['image']
            if os.path.exists(file_path):
                os.remove(file_path)

            image_table.delete_one({"id":image_id}) # deleting data in image model
            metacollection.delete_one({"id":image_id})# deleting metadata
            
            messages.success(request, "Image and metadata succesfully deleted")

            def has_delete_permission(self, request, obj = None): 
                return False

    admin.site.add_action(delete_cascade_meta,'Delete with Meta') 


admin.site.register(Image,ImageAdmin)