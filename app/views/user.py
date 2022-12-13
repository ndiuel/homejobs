from asyncio import proactor_events
from email.utils import unquote
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session, abort
from flask_login import current_user, login_required
from ..decorators import roles_required
from . import csrf
from ..forms.user import AboutForm, ChangeImageForm, PersonalInfoForm, AddressForm, VerificationForm, ChangePersonalInfoForm, ReviewForm
from ..utils import upload_file
from ..models import Provider, User, Service, ProviderService, Review, Rating, Chat, ChatViews, ChatMessages

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
    provider = None
   
    if current_user.is_authenticated:
        if current_user.first_name is None:
            return redirect(url_for('.upload_personal_info'))
    if current_user.is_authenticated and current_user.has_role("provider"):
        provider = Provider.query.filter_by(user_id=current_user.id).first()
        if provider and provider.identification_doc_url is None:
            return redirect(url_for("user.upload_identity_info"))
        if provider and provider.address is None:
            return redirect(url_for("user.upload_address_info"))
        if provider and provider.about is None:
            return redirect(url_for("user.upload_about_info"))
    providers, searched, form_used = search_providers()
    return render_template("index.html", form_used=form_used, providers=providers, searched=searched, services=Service.query.all(), locations=['Lagos', 'Akwa Ibom'], selected_location=selected_location, selected_services=selected_services, provider=provider)


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
@login_required
def change_personal_info():
    form = ChangePersonalInfoForm(obj=current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_no = form.phone_no.data
        current_user.save()
        flash("Personal Information Saved")
        return redirect(url_for(".profile"))
    return render_template("form.html", form=form, form_title="Personal Information")


@user.route("/upload_personal_info", methods=["POST", "GET"])
@login_required
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
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_no = form.phone_no.data
        current_user.save()
        flash("Personal Information Saved")
        return redirect(url_for(".index"))
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


@user.route("/chat/<int:id>", methods=["POST", "GET"])
@login_required
def chat(id):
    user = User.query.get_or_404(id)
    
    chat = Chat.query.filter((Chat.user_1_id == user.id) | (Chat.user_2_id == user.id))
    chat = chat.filter((Chat.user_1_id == current_user.id) | (Chat.user_2_id == current_user.id)).first()
    if chat is None:
        chat = Chat()
        chat.user_1_id = user.id
        chat.user_2_id = current_user.id 
        chat.save()
    
    if chat.user_1_id != current_user.id and chat.user_2_id != current_user.id:
        abort(403)
    
    if id == current_user.id:
        abort(403)
    chatview = ChatViews()
    chatview.chat_id = chat.id 
    chatview.user_id = current_user.id 
    chatview.save()
    other = chat.user_1_id
    if other == current_user.id:
        other = chat.user_2_id
    other = User.query.filter_by(id=id).first()
    return render_template('chat.html', chat=chat, other=other)
    
    
@user.route("/chats/<int:id>")    
@login_required
def chats(id):
    chat = Chat.query.get_or_404(id)
    msgs = ChatMessages.query.filter_by(chat_id=chat.id).order_by(ChatMessages.date_created.desc())
    html = render_template('_chat.html', chats=msgs)
    return {'html': html}


@user.route("/chat/new/<int:id>", methods=["POST"])
@login_required
@csrf.exempt
def new_chat(id):
    chat = Chat.query.get_or_404(id)
    data = request.get_json(force=True)
    msg = data.get('msg', '')
    print(msg)
    if msg:
        chat_msg = ChatMessages()
        chat_msg.sender_id = current_user.id 
        chat_msg.message = msg 
        chat_msg.chat_id = chat.id
        chat_msg.save()
        chat.updated += 1
        chat.save()
    return ''
    
def other(chat):
    id = chat.user_1_id if current_user.id == chat.user_2_id else chat.user_2_id
    return User.query.filter_by(id=id).first()

def last_msg(chat):
    chat = ChatMessages.query.filter_by(chat_id=chat.id).order_by(ChatMessages.date_created.desc()).first()
    if chat:
        return chat.message 
    else:
        return ''
    
def is_new_chat(chat):
    view = ChatViews.query.filter_by(user_id=current_user.id).order_by(ChatViews.date_created.desc()).first()
    return view and view.date_created < chat.date_modified

@user.route("/messages")
@login_required
def messages():
    return render_template("messages.html", chats=Chat.query.filter((Chat.user_1_id == current_user.id) | (Chat.user_2_id == current_user.id)), other=other, last_msg=last_msg,
                           is_new_chat=is_new_chat)


@user.route("/reviews")
@roles_required('provider')
def reviews():
    provider = Provider.query.filter_by(user_id=current_user.id).first()
    return render_template("reviews.html", provider=provider)



    
    
    
        