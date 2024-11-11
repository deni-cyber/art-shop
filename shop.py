from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from models import Message,Blog,Art
import random
import os
from werkzeug.utils import secure_filename

#here we define other required variables
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


#app configuration
app = Flask(__name__)
#the app setttings go here.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'this_string_is_sacred'


#here other requred functions are defined.
#########
#########
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


##########
##########
#url routing starts here 

@app.route("/")
def home ():
    art_list=Art.get_from_db()
    if not art_list:
        flash('no art available')
    return render_template('landingpage.html',art_list=art_list)

@app.route("/uploaded_file/<filename>/")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/admin/', methods=["POST","GET"])
def admin ():
    art_category_list=['Digital','Posta', 'logo', 'drawing', 'painting', ]
    messages_list=Message.get_from_db()
    blog_list=Blog.get_from_db()
    art_list=Art.get_from_db()
    if not messages_list:
        flash('no messages to show')
    if not blog_list:
        flash ('no blogs to show')
    if not art_list:
        flash ('no art to show')
    return render_template('admin.html',messages_list=messages_list, blog_list=blog_list, art_category_list=art_category_list, art_list=art_list)
    

@app.route('/add_art/',methods=['POST', 'GET'])
def add_art():
    if request.method =="POST":
        if not request.form['name'] or not request.form['category'] or not request.form['description']:
            flash('Please enter all the fields', 'error')

        else:

            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)  

                name=(request.form['name'])
                category=(request.form['category'])
                description=(request.form['description'])
                price=(request.form['price'])
                art_image_url=url_for('uploaded_file', filename=filename)
                art_image_filename=filename

                art=Art(name, category, description , price, art_image_url, art_image_filename)
                art.save_to_db()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
                flash(f'Art-{art} added to the Arts & Graphics successfuly')
                return redirect(request.url)
            else:
                flash('ivalid image file')
                return redirect(request.url)
        return redirect(url_for('admin'))
    else:
        # Redirect GET requests to admin page
        return redirect(url_for('admin'))

@app.route('/amodify_art/', methods=["POST", "GET"])
def modify_art():
    if request.method == 'POST':
        # Get the 'project' value from the form
        art = request.form.get('art')

        if not art:
            flash('No Art has been selected')
            return redirect(url_for('admin'))

        # Split the 'project' value assuming it's formatted as "<project_id> <filename>"
        try:
            art_parts = art.split()
            print(art_parts)
            if len(art_parts) >= 2:
                art_id, filename = art_parts[0], art_parts[1]

                # Remove the file associated with the project
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

                # Remove project from the database
                Art.remove_from_db(art_id)

                flash('Art deleted successfully')
            else:
                flash('Invalid Art selection format')

        except FileNotFoundError:
            flash(f'File not found: {filename}')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            print(e)

        return redirect(url_for('admin'))

    else:
        # Redirect GET requests to admin page
        return redirect(url_for('admin'))



@app.route('/message/', methods=["POST"])
def message ():
    if request.method == "POST":
        if not request.form['username'] or not request.form['useremail'] or not request.form['message'] :
            flash('Please fill in all the fields', 'error')

        else:
            username=request.form['username']
            useremail=request.form['useremail']
            subject=request.form['subject']
            message=request.form['message']
            message_part=Message(username,useremail,subject,message)
            message_part.add_to_db()
            flash(f'message has been sent, thanks for contacting Denis.')
        return redirect(url_for('contacts'))

@app.route('/delete_message/', methods=['post','get'])
def delete_message():
    if request.method == "POST":
        message_id = request.form.get('message_id')

        if not message_id:  
            flash('No message has been selected', 'error')
        else:
            if Message.delete_message(message_id):
                flash('Message deleted successfully', 'success')
            else:
                flash('Failed to delete the message', 'error')

        return redirect(url_for('admin')) 

@app.route('/contacts/')
def contacts ():
    return render_template('contacts.html')


@app.route('/cart/')
def cart ():
    return render_template('cart.html')

@app.route('/blog/', methods=['post', 'get'])
def blog():
    blog_list=Blog.get_from_db()
    blog_list.reverse()
    return render_template('blogs.html', blog_list=blog_list)

@app.route('/add-blog/' , methods=['POST', 'GET'])
def add_blog():
    if request.method =='POST':
        if not request.form['title'] or not request.form['outhor'] or not request.form['description']:
            flash('fill in all the areas')
        else:
            try:
                blog=request.form
                blog_to_save=Blog(blog['title'], blog['outhor'], blog['description'])
                blog_to_save.save_to_db()
                flash('blog posted succesfully')
            except:
                flash('an error occured')
            return render_template('admin.html')
    return render_template('admin.html')
@app.route('/delet_blog/' , methods=['POST', 'GET'])
def delete_blog():
    if request.method == "POST":
        blog_id = request.form.get('blog_id')
        if not blog_id:  
            flash('No blog has been selected', 'error')
        else:
            Blog.remove_from_db(blog_id)
            flash('Blog deleted successfully', 'success')
        return redirect(url_for('admin')) 

if __name__ =='__main__':
    app.run(debug=True)