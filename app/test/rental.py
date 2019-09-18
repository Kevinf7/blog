from flask import render_template, redirect, url_for, flash, request, current_app
from app.test import bp
from app.test.forms import SearchForm
from authlib.client import OAuth2Session
import pandas as pd


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
                'page':1,\
                'pageSize':100,\
                'listingType':'Rent',\
                'minBedrooms':int(form.min_bedrooms.data),\
                'maxBedrooms':int(form.max_bedrooms.data),\
                'maxPrice':int(form.max_price.data),\
                'locations':[\
                {\
                    'postcode':form.postcode.data\
                }\
                ]\
            })
        data = []
        json_resp = resp.json()
        for j in json_resp:
            data.append(j['listing']['listingSlug'])
        df = pd.DataFrame(data)
        df.to_csv(current_app.config['RENTAL_FOLDER'] / 'test.csv', index=False)
        return render_template('test/rental_results.html',data=resp.json())
    return render_template('test/rental.html',form=form)
