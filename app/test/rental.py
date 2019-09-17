from flask import render_template, redirect, url_for, flash, request, current_app
from app.test import bp
from app.test.forms import SearchForm
from authlib.client import OAuth2Session


# oauth2 domain
scope='api_listings_read'
domain = OAuth2Session(current_app.config['DOMAIN_CLIENT_ID'], current_app.config['DOMAIN_CLIENT_SECRET'], scope=scope)
token = domain.fetch_access_token('https://auth.domain.com.au/v1/connect/token', grant_type='client_credentials')


@bp.route('/rental', methods=['GET','POST'])
def rental():
    form=SearchForm()
    if form.validate_on_submit():
        resp=domain.post('https://api.domain.com.au/v1/listings/residential/_search',\
            json={\
                'minBedrooms':int(form.min_bedrooms.data),\
                'maxBedrooms':int(form.max_bedrooms.data),\
                'locations':[\
                {\
                    'postcode':form.postcode.data\
                }\
                ]\
            })
        print(resp.json())
        return render_template('test/rental_results.html',data=resp.json())
    return render_template('test/rental.html',form=form)
