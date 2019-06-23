from app import create_app, db

app = create_app()

#when you run flask shell the model objects will be instantiated for you
with app.app_context():
    #it seems you need to wrap it inside with app.app_context otherwise current_app is null?
    from app.models import User, Role, Tagged, Post, Tag, Comment, Contact, Images, Content, Page
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Post': Post, 'Tagged': Tagged, 'Role': Role,
                'Tag': Tag, 'Comment' : Comment, 'Contact' : Contact, 'Images' : Images,
                'Content' : Content, 'Page' : Page}
