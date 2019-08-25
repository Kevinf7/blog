from flask import render_template, redirect, url_for, flash, request, session, make_response, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.post import bp
from app.post.forms import PostForm, CommentFormAnon, CommentFormReg, DeletePostForm
from app.models import Post, Tag, Tagged, Images, Comment
from werkzeug.urls import url_parse
import os
from PIL import Image
from datetime import datetime

##############################################################################
# Post blueprint
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
@bp.route('/add_post/',methods=['GET','POST'])
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

        flash('Your post has been published!','success')
        return redirect(url_for('main.index'))
    return render_template('post/add_post.html',form=form)

# edit an existing post which you posted
@bp.route('/edit_post/<id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    # keeps track of whether user came from home page or detail page
    if request.method == 'GET':
        session['edit_post'] = request.referrer
    post = Post.getPost(id)
    # id is wrong
    if post is None:
        flash('No such post exists.','error')
        return redirect(url_for('index'))
    # users's cannot edit other user's post, not needed in this blog but there anyways
    if post.author.id != current_user.id:
        flash("You are not authorised to edit someone else's post",'error')
        return redirect(url_for('main.index'))

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

        flash('Your post has been updated!','success')
        if session['edit_post'] is not None:
            return redirect(session['edit_post'])
        else:
            return redirect(url_for('main.index'))

    tags = post.getTagNamesStr()
    return render_template('post/edit_post.html',form=form,post=post,tags=tags)

# delete an existing post - only admin can perform
@bp.route('/del_post/<id>',methods=['GET','POST'])
@login_required
def del_post(id):
    post = Post.getPost(id)
    # id is wrong
    if post is None:
        flash('No such post exists.','error')
        return redirect(url_for('index'))
    # only admin can delete post
    if not current_user.is_admin():
        flash('You do not have permission to perform this function','error')
        return redirect(url_for('main.index'))

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
        flash('The post has been deleted','error')
        return redirect(url_for('main.index'))
    form = DeletePostForm()
    tags = post.getTagNamesStr()
    return render_template('post/del_post.html',form=form,post=post,tags=tags)

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

##############################################################################
# tinyMCE file uploader
##############################################################################

# Handles javascript image uploads from tinyMCE
@bp.route('/imageuploader', methods=['POST'])
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
                img_fullpath = os.path.join(current_app.config['UPLOADED_PATH'], filename)
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
                tmb_fullpath = os.path.join(current_app.config['UPLOADED_PATH_THUMB'], thumbnail)
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
