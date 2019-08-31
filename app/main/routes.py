from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user
from app import db
from app.main import bp
from app.main.forms import ContactForm
from app.models import Tag, Tagged, Post, Content, Page, Contact
from app.main.email import send_contact_email
from app.post.forms import CommentFormAnon, CommentFormReg

##############################################################################
# Main blueprint
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


@bp.route('/')
@bp.route('/index')
def index():
    # check if there is tag in url, get the id given the tag name
    tag_id = Tag.getTagId(request.args.get('tag'))
    if tag_id == -1:
        # get page number from url. If no page number use page 1
        page = request.args.get('page',1,type=int)
        # True means 404 error is returned if page is out of range. False means an empty list is returned
        posts = Post.query.filter(Post.current==True).order_by(Post.create_date.desc()) \
                .paginate(page,current_app.config['POSTS_PER_PAGE'],False)
        posts = getSummaryPosts(posts)
    else:
        # get page number from url. If no page number use page 1
        page = request.args.get('page',1,type=int)
        # True means 404 error is returned if page is out of range. False means an empty list is returned
        posts = Post.query.filter(Post.current==True,Post.tags.any(tag_id=tag_id)) \
                .order_by(Post.create_date.desc()) \
                .paginate(page,current_app.config['POSTS_PER_PAGE'],False)
        posts = getSummaryPosts(posts)

    # get all tags and count of how many times its been tagged
    # similar to this select statement
    # SELECT a.name, count(*)
    # FROM TAG a
    # INNER JOIN TAGGED b ON (b.tag_id = a.id)
    # GROUP BY a.name
    tag_list = db.session.query(Tag, db.func.count(Tagged.tag_id)) \
                        .join(Tagged).group_by(Tagged.tag_id).all()

    return render_template('main/index.html',posts=posts,tag_list=tag_list)


@bp.route('/about', methods=['GET'])
def about():
    about_html = db.session.query(Content).join(Page).filter(Page.name=='about',Content.name=='content1').first()
    return render_template('main/about.html',about_html=about_html)


@bp.route('/contact', methods=['GET','POST'])
def contact():
    contact_html = db.session.query(Content).join(Page).filter(Page.name=='contact',Content.name=='content1').first()
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, email=form.email.data, \
                        message=form.message.data)
        db.session.add(contact)
        db.session.commit()
        if send_contact_email(contact):
            flash('Message has been sent!', 'success')
        else:
            flash('Sorry system error', 'error')
        return redirect(url_for('main.index'))
    return render_template('main/contact.html',form=form, contact_html=contact_html)


@bp.route('/post_detail/<id>', methods=['GET','POST'])
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
        flash('Your comments have been posted','success')
        return redirect(url_for('post.post_detail',id=id))
    return render_template('post/post_det.html',post=post, form=form, comments=comments)
