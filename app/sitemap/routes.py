from flask import render_template, current_app, make_response, url_for
from app.sitemap import bp
from datetime import datetime, timedelta
from app.models import Post


@bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []

    # get static routes
    # use arbitary 10 days ago as last modified date
    lastmod = datetime.now() - timedelta(days=10)
    lastmod = lastmod.strftime('%Y-%m-%d')
    for rule in current_app.url_map.iter_rules():
        # omit auth and admin routes and if route has parameters. Only include if route has GET method
        if 'GET' in rule.methods and len(rule.arguments) == 0 \
                and not rule.rule.startswith('/admin') \
                and not rule.rule.startswith('/auth'):
            pages.append(['https://www.kevin7.net' + rule.rule, lastmod])

    # get dynamic routes
    posts = Post.query.order_by(Post.update_date).all()
    for post in posts:
        url = 'https://www.kevin7.net' + url_for('main.post_detail', id=post.id)
        last_updated = post.update_date.strftime('%Y-%m-%d')
        pages.append([url, last_updated])

    sitemap_template = render_template('sitemap/sitemap_template.xml', pages=pages)
    response = make_response(sitemap_template)
    response.headers['Content-Type'] = 'application/xml'
    return response
