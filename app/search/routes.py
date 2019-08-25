from flask import render_template, request, current_app
from app.search import bp
from operator import itemgetter
from app.models import Post
from sqlalchemy import or_, and_

##############################################################################
# Search blueprint
##############################################################################

@bp.route('/search', methods=['POST'])
def search():
    # get page number from url. If no page number use page 1
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        search_str = request.form['search_txt']
        '''posts = Post.query.filter(Post.current==True). \
                            filter(Post.post.like('%'+search_str+'%') | \
                            Post.heading.like('%'+search_str+'%')).all()
        '''
        posts = Post.query.filter(and_(Post.current==True),
                                      (or_(Post.post.like('%'+search_str+'%'),
                                           Post.heading.like('%'+search_str+'%')))).all()

        results = []
        # create a list of dictionaries of posts and number of occurrence of search string
        for p in posts:
            # only keep if search text is in content not tags
            if p.is_txtinHTML(search_str) or search_str.lower() in p.heading.lower():
                # add to results
                d = {"post":p,"count":p.occurrences(search_str)}
                results.append(d)
        # now sort the results and only keep the first n elements
        results = sorted(results, key=itemgetter('count'), reverse=True)[:current_app.config['SEARCH_RESULTS_RETURN']]

    return render_template('search/search.html',results=results)
