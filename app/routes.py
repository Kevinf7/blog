from app import app, db
from flask import render_template, redirect, url_for, flash, request, send_from_directory, jsonify, session
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from datetime import datetime
import os
from app.email import send_password_reset_email, send_contact_email
from werkzeug.urls import url_parse
from operator import itemgetter
from PIL import Image

##############################################################################
# Main pages
##############################################################################

# check for new page anchor so only summary is shown
# new page anchor must be an anchor entered in a paragraph <p>br<a id="br"></a></p>
# expects a SQLalchemy pagination object
def getSummaryPosts(posts):
    for index, post in enumerate(posts.items):
        # split first occcurence of below string and keep everything on the left
        p = post.post.split('<p>br<a id="br"></a></p>',1)[0]
        # add a more... to the end of the post
        if p != post.post:
            p += '<p>...</p>'
        posts.items[index].post = p
    return posts

@app.route('/')
@app.route('/index')
def index():
    # check if there is tag in url, get the id given the tag name
    tag_id = Tag.getTagId(request.args.get('tag'))
    if tag_id == -1:
        # get page number from url. If no page number use page 1
        page = request.args.get('page',1,type=int)
        # True means 404 error is returned if page is out of range. False means an empty list is returned
        posts = Post.query.filter(Post.current==True).order_by(Post.create_date.desc()) \
                .paginate(page,app.config['POSTS_PER_PAGE'],False)
        posts = getSummaryPosts(posts)
    else:
        # get page number from url. If no page number use page 1
        page = request.args.get('page',1,type=int)
        # True means 404 error is returned if page is out of range. False means an empty list is returned
        posts = Post.query.filter(Post.current==True,Post.tags.any(tag_id=tag_id)) \
                .order_by(Post.create_date.desc()) \
                .paginate(page,app.config['POSTS_PER_PAGE'],False)
        posts = getSummaryPosts(posts)

    # get all tags and count of how many times its been tagged
    # similar to this select statement
    # SELECT a.name, count(*)
    # FROM TAG a
    # INNER JOIN TAGGED b ON (b.tag_id = a.id)
    # GROUP BY a.name
    tag_list = db.session.query(Tag, db.func.count(Tagged.tag_id)) \
                        .join(Tagged).group_by(Tagged.tag_id).all()

    return render_template('index.html',posts=posts,tag_list=tag_list)

@app.route('/about', methods=['GET'])
def about():
    about_html = db.session.query(Content).join(Page).filter(Page.name=='about',Content.name=='content1').first()
    return render_template('about.html',about_html=about_html)

@app.route('/contact', methods=['GET','POST'])
def contact():
    contact_html = db.session.query(Content).join(Page).filter(Page.name=='contact',Content.name=='content1').first()
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, email=form.email.data, \
                        message=form.message.data)
        db.session.add(contact)
        db.session.commit()
        if send_contact_email(contact):
            flash('Message has been sent!')
        else:
            flash('Sorry system error')
        return redirect(url_for('index'))
    return render_template('contact.html',form=form, contact_html=contact_html)

##############################################################################
# User routes
##############################################################################

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # username/password is valid. sets current_user to the user
        login_user(user, remember=form.remember_me.data)

        # Parameter is added by flask-login.
        # It tells you where user was trying to go to.
        next_page = request.args.get('next')

        # in case url is absolute we will ignore, we only want a relative url
        # netloc returns the www.website.com part
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('edit_post',None)
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, firstname=form.firstname.data, \
                    lastname=form.lastname.data, )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

##############################################################################
# Post routes
##############################################################################

def processTags(tags_new,post):
    changed=False
    # get all current tags for post
    tags_current = post.getTagNames()
    # check if any tags should be deleted
    for tag in tags_current:
        if tag not in tags_new:
            # tag has been deleted, delete from Tagged table
            id = Tag.getTagId(tag)
            Tagged.query.filter_by(post_id=post.id,tag_id=id).delete()
            changed=True

    # is there tags to add?
    if not(len(tags_new) == 1 and tags_new[0] == ''):
        # if tag doesn't exist create it in Tags table
        for tag in tags_new:
            if Tag.getTagId(tag) == -1:
                t = Tag(name=tag)
                db.session.add(t)
                changed=True

        #check if any tags should be added
        for tag in tags_new:
            if tag not in tags_current:
                # tag is new, add to Tagged table
                id = Tag.getTagId(tag)
                t = Tagged(post_id=post.id, tag_id=id)
                db.session.add(t)
                changed=True
    # maybe better, just call commit once
    if changed:
        db.session.commit()

# add a new post
@app.route('/add_post/',methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        # write post to db
        post = Post(heading=form.heading.data,post=form.post.data,author=current_user)
        db.session.add(post)
        db.session.commit()

        # tags should be separated by commas (,) and start with hash (#)
        tags = form.tags.data
        tag_list = [t.strip() for t in tags.split(',')]
        processTags(tag_list,post)

        flash('Your post has been published!')
        return redirect(url_for('index'))
    return render_template('add_post.html',form=form)

# edit an existing post which you posted
@app.route('/edit_post/<id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    # keeps track of whether user came from home page or detail page
    if request.method == 'GET':
        session['edit_post'] = request.referrer
    post = Post.getPost(id)
    # id is wrong
    if post is None:
        flash('No such post exists.')
        return redirect(url_for('index'))
    # users's cannot edit other user's post, not needed in this blog but there anyways
    if post.author.id != current_user.id:
        flash("You are not authorised to edit someone else's post")
        return redirect(url_for('index'))

    form = PostForm()
    if form.validate_on_submit():
        post.heading = form.heading.data
        post.post = form.post.data
        post.update_date = datetime.utcnow()
        db.session.add(post)
        db.session.commit()

        # tags should be separated by commas (,) and start with hash (#)
        tags = form.tags.data
        tag_list = [t.strip() for t in tags.split(',')]
        processTags(tag_list,post)

        flash('Your post has been updated!')
        if session['edit_post'] is not None:
            return redirect(session['edit_post'])
        else:
            return redirect(url_for('index'))

    tags = post.getTagNamesStr()
    return render_template('edit_post.html',form=form,post=post,tags=tags)

# delete an existing post - only admin can perform
@app.route('/del_post/<id>',methods=['GET','POST'])
@login_required
def del_post(id):
    post = Post.getPost(id)
    # id is wrong
    if post is None:
        flash('No such post exists.')
        return redirect(url_for('index'))
    # only admin can delete post
    if not current_user.is_admin():
        flash("You do not have permission to perform this function")
        return redirect(url_for('index'))

    # user confirms he wants to delete
    if request.method == 'POST':
        #we want to do a soft delete only
        post.current=False
        db.session.add(post)
        #also delete all the tag links associated to this post
        tagged = Tagged.query.filter_by(post_id=post.id).all()
        for t in tagged:
            db.session.delete(t)
        db.session.commit()
        flash('The post has been deleted')
        return redirect(url_for('index'))
    form = DeletePostForm()
    tags = post.getTagNamesStr()
    return render_template('del_post.html',form=form,post=post,tags=tags)

@app.route('/post_detail/<id>', methods=['GET','POST'])
def post_detail(id):
    post = Post.query.filter_by(id=id).first()
    post.post = post.post.replace('<p>br<a id="br"></a></p>','')
    comments = post.comments.all()
    if current_user.is_authenticated:
        form = CommentFormReg()
    else:
        form = CommentFormAnon()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(comment=form.comment.data,commenter=current_user,post=post)
        else:
            if form.email.data == '':
                comment = Comment(comment=form.comment.data,name=form.name.data,post=post)
            else:
                comment = Comment(comment=form.comment.data,name=form.name.data,\
                                email=form.email.data,post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comments have been posted')
        return redirect(url_for('post_detail',id=id))
    return render_template('post_det.html',post=post, form=form, comments=comments)

##############################################################################
# Admin routes - Content Management
##############################################################################

@app.route('/manage_content',methods=['GET'])
@login_required
def manage_content():
    contents = Content.query.all()
    return render_template('manage_content.html',contents=contents)

@app.route('/edit_content/<id>',methods=['GET','POST'])
@login_required
def edit_content(id):
    content = Content.query.filter_by(id=id).first()
    if content is None:
        flash('No such content exists.')
        return redirect(url_for('index'))
    form=ContentManageForm()
    if form.validate_on_submit():
        # update db
        content.content = form.post.data
        content.update_date = datetime.utcnow()
        db.session.add(content)
        db.session.commit()
        flash('The content has been updated!')
        return redirect(url_for('manage_content'))
    return render_template('edit_content.html',form=form,content=content)

##############################################################################
# Admin routes - Images
##############################################################################

@app.route('/manage_images',methods=['GET'])
@login_required
def manage_images():
    # get page number from url. If no page number use page 1
    page = request.args.get('page',1,type=int)
    # True means 404 error is returned if page is out of range. False means an empty list is returned
    images = Images.query.order_by(Images.create_date.desc()) \
                        .paginate(page,app.config['IMAGES_PER_PAGE'],False)
    return render_template('manage_images.html',images=images)

@app.route('/del_image/<id>',methods=['GET','POST'])
@login_required
def del_image(id):
    form = DeleteImageForm()
    image = Images.getImage(id)
    # id is wrong
    if image is None:
        flash('No such image.')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        img_fullpath = os.path.join(app.config['UPLOADED_PATH'], image.filename)
        tmb_fullpath = os.path.join(app.config['UPLOADED_PATH_THUMB'], image.thumbnail)
        try:
            # delete image and thumbnail from file system
            os.remove(img_fullpath)
            os.remove(tmb_fullpath)
            # delete from db
            db.session.delete(image)
            db.session.commit()
            flash('The image has been successfully deleted')
            return redirect(url_for('manage_images'))
        except OSError:
            flash('System error deleting image.')
            return redirect(url_for('manage_images'))
    return render_template('del_image.html',form=form,img=image)

##############################################################################
# Admin routes - Messages
##############################################################################

@app.route('/manage_messages',methods=['GET','POST'])
@login_required
def manage_messages():
    page = request.args.get('page',1,type=int)
    contacts = Contact.query.order_by(Contact.create_date.desc()) \
    .paginate(page,app.config['MESSAGES_PER_PAGE'],False)

    return render_template('manage_message.html',contacts=contacts)

##############################################################################
# Admin routes - Tags
##############################################################################

@app.route('/manage_tags',methods=['GET'])
@login_required
def manage_tags():
    # get tags being are used only
    tag_used = db.session.query(Tag).join(Tagged).all()
    # get tags not being used
    tag_all = Tag.query.all()
    tag_notused = []
    for t in tag_all:
        if t not in tag_used:
            tag_notused.append(t)

    return render_template('manage_tags.html',tag_used=tag_used, tag_notused=tag_notused)

@app.route('/edit_tag/<id>',methods=['GET','POST'])
@login_required
def edit_tag(id):
    form = EditTagForm()
    tag = Tag.getTag(id)
    if form.validate_on_submit():
        tag.name = form.tag_name.data
        tag.update_date = datetime.utcnow()
        db.session.add(tag)
        db.session.commit()
        flash('The tag has been successfully updated')
        return redirect(url_for('manage_tags'))
    return render_template('edit_tag.html',form=form,tag=tag)

@app.route('/del_tag/<id>',methods=['GET','POST'])
@login_required
def del_tag(id):
    form = DeleteTagForm()
    tag = Tag.getTag(id)
    if tag is None:
        flash('No such tag.')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        db.session.delete(tag)
        db.session.commit()
        flash('The tag has been successfully deleted')
        return redirect(url_for('manage_tags'))
    return render_template('del_tag.html',form=form,tag=tag)

##############################################################################
# search routes
##############################################################################

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_str = request.form['search_txt']
        posts = Post.query.filter(Post.current==True). \
                            filter(Post.post.like('%'+search_str+'%') | \
                            Post.heading.like('%'+search_str+'%')).all()
        results = []
        # create a list of dictionaries of posts and number of occurrence of search string
        for p in posts:
            # only keep if search text is in content not tags
            if p.is_txtinHTML(search_str) or search_str.lower() in p.heading.lower():
                # add to results
                d = {"post":p,"count":p.occurrences(search_str)}
                results.append(d)
        # now sort the results and only keep the first n elements
        results = sorted(results, key=itemgetter('count'), reverse=True)[:app.config['SEARCH_RESULTS_RETURN']]

    return render_template('search.html',results=results)

##############################################################################
# tinyMCE file upload routes
##############################################################################

# Handles javascript image uploads from tinyMCE
@app.route('/imageuploader', methods=['POST'])
@login_required
def imageuploader():
    file = request.files.get('file')
    if file:
        filename = file.filename.lower()
        fn, ext = filename.split('.')
        # truncate filename (excluding extension) to 30 characters
        fn = fn[:30]
        filename = fn + '.' + ext
        if ext in ['jpg', 'gif', 'png', 'jpeg']:
            try:
                # everything looks good, save file
                img_fullpath = os.path.join(app.config['UPLOADED_PATH'], filename)
                file.save(img_fullpath)
                # get the file size to save to db
                file_size = os.stat(img_fullpath).st_size
                size = 160, 160
                # read image into pillow
                im = Image.open(img_fullpath)
                # get image dimension to save to db
                file_width, file_height = im.size
                # convert to thumbnail
                im.thumbnail(size)
                thumbnail = fn + '-thumb.jpg'
                tmb_fullpath = os.path.join(app.config['UPLOADED_PATH_THUMB'], thumbnail)
                # PNG is index while JPG needs RGB
                if not im.mode == 'RGB':
                    im = im.convert('RGB')
                # save thumbnail
                im.save(tmb_fullpath, "JPEG")

                # save to db
                img = Images(filename=filename, thumbnail=thumbnail, file_size=file_size, \
                            file_width=file_width, file_height=file_height)
                db.session.add(img)
                db.session.commit()
            except IOError:
                output = make_response(404)
                output.headers['Error'] = 'Cannot create thumbnail for ' + filename
                return output
            return jsonify({'location' : filename})

    # fail, image did not upload
    output = make_response(404)
    output.headers['Error'] = 'Filename needs to be JPG, JPEG, GIF or PNG'
    return output

##############################################################################
# Forgot password routes
##############################################################################

# User to enter email address to send forgot password link to
@app.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if send_password_reset_email(user):
                flash('Check your email for instructions to reset your password')
            else:
                flask('Sorry system error')
        else:
            flash('Email does not exist in our database')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html',form=form)

# Allow users to create new password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Token has expired or is no longer valid')
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('index'))
    return render_template('reset_password.html', form=form)

##############################################################################
# Miscellaneous
##############################################################################

@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html')

# checks this before any function, updates last seen with current time
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
