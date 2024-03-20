from django.shortcuts import render,redirect
from . import models
from . import forms
import stripe
from django.template.loader import get_template

def home(request):
    banners = models.Banners.objects.all()
    services = models.Service.objects.all()[:3]
    gimgs = models.GalleryImage.objects.all().order_by('-id')[:9]
    return render(request, 'main/home.html', {'banners': banners, 'services': services,
                                              'gimgs': gimgs})


def page_detail(request,id):
    page = models.Page.objects.get(id=id)
    return render(request, 'main/page.html', {'page': page})

def faq_list(request):
    faq = models.faq.objects.all()
    return render(request, 'main/faq.html', {'faq': faq})

def enquiry(request):
    msg = ''
    if request.method == "POST":
        form = forms.EnquiryForm(request.POST)
        if form.is_valid:
            form.save()
            msg = "Data is saved"
    form = forms.EnquiryForm
    return render(request, 'main/enquiry.html', {"form": form, "msg": msg})


def showGallery(request):
    gallerys = models.Gallery.objects.all().order_by('-id')
    return render(request, 'main/gallery.html',{'gallerys': gallerys})


#show gallery photos
def gallery_detail(request,id):
    gallery = models.Gallery.objects.get(id=id)
    gallery_imgs = models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    return render(request, 'main/gallery_imgs.html',{'gallery_imgs' :gallery_imgs,
                                                     'gallery':gallery})


#show pricing
def pricing(request):
    plans = models.SubPlan.objects.all().order_by('id')
    dfeature = models.SubPlanFeature.objects.all()
    return render(request, 'main/pricing.html', {'plans': plans,
                                                 'dfeature' : dfeature})

#signup
def signup(request):
    msg = None
    if request.method == "POST":
        form = forms.SignUp(request.POST)
        if form.is_valid():
            form.save()
            msg = "Thankyou for registering"

    form = forms.SignUp
    return render(request, 'registration/signup.html', {'form': form,
                                                        'msg':msg} )


#checkout
def checkout(request,plan_id):
    planDetail = models.SubPlan.objects.get(pk = plan_id)
    return render(request, 'main/checkout.html', {'plan': planDetail})


#stripe key
stripe.api_key = "sk_test_51NwLUESDysNFZsyaC2WMc2eEnnRAX9QxRR3oel0JxHaHuYZdfYCLVL7lODQ3bTLNI6B8xPH5Z2lSerjMFx1fOQhM00erEVGphO"

def checkout_session(request, plan_id):
    plan = models.SubPlan.objects.get(pk= plan_id)
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items=[
                {
                    'price_data':{
                        'currency': 'inr',
                        'product_data':{
                            'name': plan.title
                        },
                        'unit_amount':plan.price
                    },
                    'quantity': 1
                },
            ],
            mode='payment', 
            success_url= 'http://127.0.0.1.8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1.8000/pay_cancel',
            client_reference_id=plan_id
    )

    return redirect(session.url , code=303)

#success
from django.core.mail import EmailMessage

def pay_success(request):
    session =  stripe.checkout.Session.retrieve(request.GET['session_id'])
    plan_id = session.client_reference_id
    plan = models.SubPlan.objects.get(pk = plan_id)
    user = request.user
    models.Subscription.objects.ccreate(
        plan = plan,
        user = user,
        price = plan.price
    )
    subject = 'Order Email'
    html_content = get_template('main/orderemail.html').render({'title': plan.title})
    from_email = 'mayureshpisat18@gmail.com'
    msg = EmailMessage(subject, html_content, from_email, ['john@gmail.com'])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    return render(request, 'main/success.html')



#cancel
def pay_cancel(request):
    return render(request, 'main/cancel.html')

# User Dashboard Section Start
def user_dashboard(request):
	return render(request, 'user/dashboard.html')


#edit form
def update_profile(request):
    msg = ""
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            msg = "Data is saved"
    else:
        form = forms.ProfileForm(request.POST, instance = request.user)
    return render(request,'user/update-profile.html', {'form':form,
                                                       'msg':msg})