from app import db
from app.main import bp
from app.main.email import send_contact_email, send_comment_email
from app.main.forms import ContactForm
from app.models import Tag, Tagged, Post, Content, Page, Contact, Comment
from app.post.forms import CommentFormAnon, CommentFormReg
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user

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
        # add a Read more... to the end of the post
        if p != post.post:
            p += '<p><a href="' + url_for('main.post_detail',slug=post.slug) + '">Read more</a> ...</p>'
        posts.items[index].post = p
    return posts


@bp.route('/')
@bp.route('/index')
def index():
    # check if there is tag in url, get the id given the tag name
    tag_name = request.args.get('tag')
    tag_id = Tag.getTagId(tag_name)
    if tag_id == -1:
        # get page number from url. If no page number use page 1
        page = request.args.get('page',1,type=int)
        # True means 404 error is returned if page is out of range. False means an empty list is returned
        posts = Post.query.filter(Post.current==True).order_by(Post.create_date.desc()) \
                .paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
        posts = getSummaryPosts(posts)
    else:
        # get page number from url. If no page number use page 1
        page = request.args.get('page',1,type=int)
        # True means 404 error is returned if page is out of range. False means an empty list is returned
        posts = Post.query.filter(Post.current==True,Post.tags.any(tag_id=tag_id)) \
                .order_by(Post.create_date.desc()) \
                .paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
        posts = getSummaryPosts(posts)

    # get all tags and count of how many times its been tagged
    # similar to this select statement
    # SELECT a.name, count(*)
    # FROM TAG a
    # INNER JOIN TAGGED b ON (b.tag_id = a.id)
    # GROUP BY a.name
    tag_list = db.session.query(Tag, db.func.count(Tagged.tag_id)) \
                        .join(Tagged).group_by(Tagged.tag_id).all()

    return render_template('main/index.html',posts=posts,tag_list=tag_list,tag_name=tag_name)


@bp.route('/about', methods=['GET'])
def about():
    about_html = db.session.query(Content).join(Page).filter(Page.name=='about',Content.name=='content1').first()
    return render_template('main/about.html',about_html=about_html)


@bp.route('/projects', methods=['GET'])
def projects():
    projects_html = db.session.query(Content).join(Page).filter(Page.name=='projects',Content.name=='content1').first()
    return render_template('main/projects.html',projects_html=projects_html)


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
            flash('Sorry system error', 'danger')
        return redirect(url_for('main.index'))
    return render_template('main/contact.html',form=form, contact_html=contact_html)


@bp.route('/post_detail/<slug>', methods=['GET','POST'])
def post_detail(slug):
    post = Post.getPostBySlug(slug)
    if post is None:
        flash('This post does not exist', 'danger')
        return redirect(url_for('main.index'))
    comments = post.comments.order_by(Comment.create_date.desc()).all()
    if current_user.is_authenticated:
        form = CommentFormReg()
    else:
        form = CommentFormAnon()
    if form.validate_on_submit():
        comment_data = form.comment.data
        if any(b in comment_data for b in current_app.config['BANNED_LIST']) or comment_data.isspace():
            flash('Sorry your comments was not accepted','danger')
            return redirect(url_for('main.post_detail',slug=slug))
        if current_user.is_authenticated:
            comment = Comment(comment=comment_data,commenter=current_user,post=post)
        else:
            if form.email.data == '':
                comment = Comment(comment=comment_data,name=form.name.data,post=post)
            else:
                comment = Comment(comment=comment_data,name=form.name.data,\
                                email=form.email.data,post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comments have been posted','success')

        #send email to admin that someone has commented
        send_comment_email(post, comment)

        return redirect(url_for('main.post_detail',slug=slug))
    post.post = post.post.replace('<p>br<a id="br"></a></p>','')
    return render_template('main/post_det.html',post=post, form=form, comments=comments)


# Simple route to display p5.js sketches
@bp.route('/processing/<name>', methods=['GET'])
def processing(name):
    script_name = name + '.js'
    return render_template('main/processing.html', script_name=script_name)


# ads.txt for adsense
@bp.route('/ads.txt', methods=['GET'])
def ads():
    return current_app.send_static_file('ads.txt')