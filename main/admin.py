from django.contrib import admin
from . import models
import stripe


class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')
admin.site.register(models.Banners,BannerAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(models.Service,ServiceAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display=('title',)
admin.site.register(models.Page)

class faqAdmin(admin.ModelAdmin):
    list_display=('quest',)
admin.site.register(models.faq)

class EnquiryAdmin(admin.ModelAdmin):
    list_display= ('full_name','email','details', 'send_time')
admin.site.register(models.Enquiry, EnquiryAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(models.Gallery,GalleryAdmin)

class GalleryImageAdmin(admin.ModelAdmin):
    list_display=('alt_text', 'image_tag')

admin.site.register(models.GalleryImage,GalleryImageAdmin)


#subplan admin
class SubPlanAdmin(admin.ModelAdmin):
    list_editable = ('highlight_status','max_member')
    list_display= ('title', 'price','highlight_status','max_member')
admin.site.register(models.SubPlan, SubPlanAdmin)

#subplan features admin
class SubPlanFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'subplans',)
    def subplans(self,obj):
        return " | ".join([sub.title for sub in obj.subplan.all()])
admin.site.register(models.SubPlanFeature, SubPlanFeatureAdmin)

#discount 
class PlanDiscountAdmin(admin.ModelAdmin):
    list_display = ('total_months', 'total_discount',)
admin.site.register(models.PlanDiscount, PlanDiscountAdmin)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_tag','mobile',)
admin.site.register(models.Subscriber, SubscriberAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user','plan', 'price',)
admin.site.register(models.Subscription, SubscriptionAdmin)


    

# Register your models here.
