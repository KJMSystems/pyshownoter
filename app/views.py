from app import app

# static files
from app import static_files
from app.mongo import mongo
from app.mongo import db_stats

from app.views_helper import shownoter_wrapper

from app.forms import TextInput, DescInput, LoginForm

from datetime import datetime
from flask import render_template, url_for, redirect, session
from flask import Markup
from flask import flash
from flask import request
from flask import make_response

from functools import wraps
from markdown import markdown


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):

        if 'logged_in' in session:
            return test(*args, **kwargs)

        else:
            flash("You are currently not logged in")
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@app.route('/index')
def index():
    """This is the home page"""

    if 'logged_in' in session:
        return redirect(url_for('create_shownote'))

    else:
        return redirect(url_for('welcome'))


@app.route('/welcome')
def welcome():
    # Retrieves the Stats for the frontpage
    stats = {
        'total_shownotes': mongo.count_entries(
            mongo.shownotes_coll), 'total_links': mongo.count_entries(
            mongo.links_coll), 'item_count': [
                (result['title'],
                 result['_id']) for result in db_stats.last(20)
                ]
        }
    return render_template('welcome.html', stats=stats)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_shownote():
    form = TextInput()

    if form.validate_on_submit():

        if form.file_input.data:
            flash('file detected')
            flash('Enter any description or other text for your notes')
            file = request.files['file_input']
            chat_text = file.read().decode('utf-8')

        elif form.chat_input.data:
            chat_text = form.chat_input.data

        else:
            flash('no chat detected')
            return render_template('index.html')

        custom_title = form.custom_title.data
        links = shownoter_wrapper(chat_text,
                                  custom_title_enabled=custom_title)

        link_id = mongo.create_entry(value={
                                    'links': links,
                                    'created': datetime.utcnow()
                                    }, collection=mongo.shownotes_coll)

        if form.bypass_title_description.data:
            title = 'Untitled Shownotes'

            entry = {
                'title': title,
                'description': ''
                }
            mongo.append_to_entry(link_id, entry)
            return redirect(url_for('results', id=link_id))

        else:
            return redirect(url_for('get_links', id=link_id))

    return render_template('create.html', form=form)


@app.route('/links/<id>', methods=['GET', 'POST'])
def get_links(id):
    """This page is where the Title and Description are added"""

    form = DescInput()
    db_links = mongo.retrieve_from_db(value=id,
                                      collection=mongo.shownotes_coll)
    links = [link for link in db_links['links']]

    if form.validate_on_submit():
        title = form.title.data
        if not title:
            title = 'untitled shownotes'

        entry = {
                'title': title,
                'description': form.description.data
            }
        mongo.append_to_entry(id, entry)

        return redirect(url_for('results', id=id))
    return render_template('links.html', form=form, links=links)


@app.route('/results/<id>', methods=['GET', 'POST'])
def results(id):
    """The final result of creating Shownotes"""

    db_entry = mongo.retrieve_from_db(value=id,
                                      collection=mongo.shownotes_coll)
    description = Markup(markdown(db_entry['description']))
    links = [link for link in db_entry['links']]
    title = db_entry['title']
    if not title:
        title = 'Untitled'
    return render_template('results.html',
                           title=title,
                           description=description,
                           links=links,
                           id=id)


@app.route('/download/<id>', methods=['GET'])
def download_file(id):
    """Saves the file into a .txt file"""

    db_entry = mongo.retrieve_from_db(value=id,
                                      collection=mongo.shownotes_coll)
    description = db_entry['description']
    links = [link['markdown'] for link in db_entry['links']]
    link_text = ''

    for link in links:
        link_text += link + '\n'

    title = db_entry['title']
    file = '''#{title}
{description}
##Links
{links}'''.format(title=title, description=description, links=link_text)

    if title:
        filename = title + '.txt'
    else:
        filename = 'untitled.txt'

    response = make_response(file)
    response.headers[
        'Content-Disposition'] = 'attachment; filename={}'.format(filename)
    response.content_type = 'text/plain'
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.username.data != 'test' or form.password.data != 'password':
            flash('Invalid Credentials! Please Try Again')

        else:
            session['logged_in'] = True
            return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You have been successfully logged out')
    return redirect(url_for('index'))
