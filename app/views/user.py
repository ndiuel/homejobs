from asyncio import proactor_events
from email.utils import unquote
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session, abort
from flask_login import current_user, login_required
from ..decorators import roles_required
from . import csrf
from ..forms.user import AboutForm, ChangeImageForm, PersonalInfoForm, AddressForm, VerificationForm, ChangePersonalInfoForm, ReviewForm
from ..utils import upload_file
from ..models import Provider, User, Service, ProviderService, Review, Rating

user = Blueprint('user', __name__)

            
@user.route("/settimezone", methods=['POST'])
@csrf.exempt
def timezone():
    timezone = request.get_json(force=True).get('timezone', 0)
    session['timezone'] = timezone
    return "ok"


def search_providers():
    form_used = True
    print(request.args)
    sq = request.args.getlist('services')
    location = request.args.get('location')
    services = sq
    if not location and not services:
        form_used = False
    s_query = Service.query.filter(Service.name.in_(services))
    providers = ProviderService.query.filter(ProviderService.service_id.in_([s.id for s in s_query]))
    query = Provider.query.filter(Provider.id.in_([p.id for p in providers]))
    query = query.filter_by(state=location)
    if query.count() > 0:
        return query, True, form_used
    return Provider.query, False, form_used


@user.route("/")
def index():
    sq = request.args.getlist('services')
    selected_location = request.args.get('location')
    selected_services = sq
   
    if current_user.is_authenticated and current_user.has_role("provider"):
        if current_user.firstname is None:
            return redirect(url_for('.upload_personal_info'))
        provider = Provider.query.filter_by(user_id=current_user.id).first()
        if provider and provider.identification_doc_url is None:
            return redirect(url_for("user.upload_identity_info"))
        if provider and provider.address is None:
            return redirect(url_for("user.upload_address_info"))
        if provider and provider.about is None:
            return redirect(url_for("user.upload_about_info"))
    providers, searched, form_used = search_providers()
    return render_template("index.html", form_used=form_used, providers=providers, searched=searched, services=Service.query.all(), locations=['Lagos', 'Akwa Ibom'], selected_location=selected_location, selected_services=selected_services)


@user.route("/profile")
@login_required
def profile():
    provider = Provider.query.filter_by(user_id=current_user.id).first()
    services = None
    if provider:
        services = ", ".join(service.name for service in provider.services)
    return render_template("profile.html", services=services, provider=provider) 

@user.route("/change_image", methods=["POST", "GET"])
@roles_required("normal")
def change_image():
    form = ChangeImageForm()
    if form.validate_on_submit():
        f = form.image.data
        url = upload_file(f)
        if url:
            current_user.image_url = url 
        else:
            flash("Error occured image could not be uploaded")
            return request(redirect.referrer)
        current_user.save()
        flash("Image Changed")
        return redirect(url_for(".profile"))
    return render_template("form.html", form=form, form_title="Change Profile Image")


@user.route("/change_personal_info", methods=["POST", "GET"])
@roles_required("provider")
def change_personal_info():
    form = ChangePersonalInfoForm(obj=current_user)
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.phone_no = form.phone_no.data
        current_user.save()
        flash("Personal Information Saved")
        return redirect(url_for(".profile"))
    return render_template("form.html", form=form, form_title="Personal Information")


@user.route("/upload_personal_info", methods=["POST", "GET"])
@roles_required("provider")
def upload_personal_info():
    form = PersonalInfoForm()
    if form.validate_on_submit():
        f = form.image.data
        url = upload_file(f)
        if url:
            current_user.image_url = url 
        else:
            flash("Error occured image could not be uploaded")
            return request(redirect.referrer)
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.phone_no = form.phone_no.data
        current_user.save()
        flash("Personal Information Saved")
        return redirect(url_for(".upload_address_info"))
    return render_template("form.html", form=form, form_title="Personal Information")


@user.route("/change_address_info", methods=["POST", "GET"])
@roles_required("provider")
def change_address_info():
    provider = Provider.query.filter_by(user_id=current_user.id).first()
    if provider is None:
        flash("User not found", category='error')
        return redirect(request.referrer)
    
    form = AddressForm(obj=provider)
    if form.validate_on_submit():
        provider.state = form.state.data
        provider.lga = form.lga.data
        provider.address = form.address.data
        provider.save()
        flash("Address Information Changed")
        return redirect(url_for(".profile"))
    return render_template("form.html", form=form, form_title="Change Address Information")

    
@user.route("/upload_address_info", methods=["POST", "GET"])
@roles_required("provider")
def upload_address_info():
    provider = Provider.query.filter_by(user_id=current_user.id).first()
    if provider is None:
        flash("User not found", category='error')
        return redirect(request.referrer)
    
    form = AddressForm()
    if form.validate_on_submit():
        provider.state = form.state.data
        provider.lga = form.lga.data
        provider.address = form.address.data
        provider.save()
        flash("Address Information Saved")
        return redirect(url_for(".upload_about_info"))
    return render_template("form.html", form=form, form_title="Address Information")


@user.route("/change_about_info", methods=["POST", "GET"])
@roles_required("provider")
def change_about_info():
    provider = Provider.query.filter_by(user_id=current_user.id).first()
    if provider is None:
        flash("User not found", category='error')
        return redirect(request.referrer)
    form = AboutForm()(about=provider.about)
    if request.method == "GET":
        form.skills.data = [(s.id) for s in provider.services]
    if form.validate_on_submit():
        provider.about = form.about.data
        for skill in form.skills.data:
            provider.services.append(Service.query.get_or_404(skill))
        provider.save()
        flash("Information About Your Services Saved")
        return redirect(url_for(".profile"))
    return render_template("form.html", form=form, form_title="Edit Services Information")
        
        
@user.route("/upload_about_info", methods=["POST", "GET"])
@roles_required("provider")
def upload_about_info():
    provider = Provider.query.filter_by(user_id=current_user.id).first()
    if provider is None:
        flash("User not found", category='error')
        return redirect(request.referrer)
    form = AboutForm()()
    if form.validate_on_submit():
        provider.about = form.about.data
        for skill in form.skills.data:
            provider.services.append(Service.query.get_or_404(skill))
        provider.save()
        flash("Information About Your Services Saved")
        return redirect(url_for(".upload_identity_info"))
    return render_template("form.html", form=form, form_title="Services Information")


@user.route("/upload_identity_info", methods=["POST", "GET"])
@roles_required("provider")
def upload_identity_info():
    provider = Provider.query.filter_by(user_id=current_user.id).first()
    if provider is None:
        flash("User not found", category='error')
        return redirect(request.referrer)
    form = VerificationForm()
    if form.validate_on_submit():
        f = form.identification.data
        url = upload_file(f)
        if url:
            provider.identification_doc_url = url 
        else:
            flash("Error occured image could not be uploaded")
            return request(redirect.referresr)
        provider.save()
        flash("Verification Information Saved, Verification Will Be Processed Shortly")
        return redirect(url_for("user.index"))
    return render_template("form.html", form=form, form_title="Verification Information")
        
        
@user.route("/provider/<int:id>")
def provider(id):
    provider = Provider.query.get_or_404(id)
    provider.profile_views = provider.profile_views or 0
    provider.profile_views += 1
    provider.save()
    return render_template("provider.html", provider=provider)


@user.route("/review/provider/<int:id>", methods=["POST", "GET"])
@roles_required("normal")
def review(id):
    provider = Provider.query.get_or_404(id)
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review()
        review.content = form.content.data
        review.user = current_user
        review.provider = provider
        review.save()
        flash("Your review has been saved")
        return redirect(url_for('.provider', id=provider.id))
    return render_template("form.html", form=form, form_title="Review Service Provider")


@user.route("/rating/provider/<int:id>", methods=["POST", "GET"])
@roles_required("normal")
def rate(id):
    provider = Provider.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('rating.html')
    rating = request.form.get('rating')
    try:
        rating = int(rating)
    except:
        rating = 1 
    rate = Rating()
    rate.provider = provider
    rate.user = current_user
    rate.rating = rating
    rate.save()
    ratings = provider.ratings
    provider.rating = (sum(r.rating for r in ratings)/len(ratings))
    provider.save()
    flash("Your rating has been saved")
    return redirect(url_for('.provider', id=provider.id))
    
    
    
        