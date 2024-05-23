from flask import Flask, render_template, flash, request, Response,redirect, url_for, render_template, request, session
import os
from moviepy.editor import VideoFileClip
from YOLO_Video import video_detection
import shutil
import os
import cv2
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


# def converter(input_path,output_path):j
#     # Open the MP4 file
#     clip = VideoFileClip(input_path)

#     clip.write_videofile(output_path, fps=clip.fps, codec='libx264')
#     # clip.write_videofile(output_path, fps=clip.fps, codec='mpeg4')  # Example using libx264 codec
#     print("Conversion complete!")


def converter(input_path, output_path):
    # Open the MP4 file
    clip = VideoFileClip(input_path)

    clip.write_videofile(output_path, fps=clip.fps, codec='libx264')
    print("Conversion complete!")


def move_image(source_path, destination_path):
    try:
        # Move the file
        shutil.move(source_path, destination_path)
        print(f"Image moved successfully from {source_path} to {destination_path}")
        
    except FileNotFoundError:
        print(f"File not found: {source_path}")
    except PermissionError:
        print(f"Permission error. Make sure you have the necessary permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")



# Define the upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/index2')
# def index():
#     return render_template('index.html')
def index2():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    else:
        return redirect(url_for("login"))

# @app.route('/login')
# def login():
#     return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    session_expired = False
    if 'user' in session:
        # Remove user information from session
        session.pop('user', None)  # Remove the user's name from the session
        session.pop('email', None)  # Remove the user's email from the session
        session_expired = True

    invalid_info = False
    invalid_required_field=False
    if request.method == "POST":
        print("post entered ::: ", request.method)
        email = request.form["email"]  # Assuming that the form field for username is called 'email'
        password = request.form["password"]  # Assuming the password field in the form is called 'password'
        if email and password:
            user = User.query.filter_by(email=email).first()  # Query the user by email
            if user and user.check_password(password):  # Check if user exists and password is correct
                session['user'] = user.name  # Store the user's name in the session
                session['email'] = user.email  # Store the user's email in the session
                return redirect(url_for("index"))  # Redirect to the index page
            else:
                invalid_info = True
        else:
             invalid_required_field=True  # Both fields are required

    if "user" in session:
        return redirect(url_for("index"))  # If already logged in, go to index

    session_ended = session.pop("_session_ended", False)

    return render_template("login.html", session_expired=session_expired , invalid_info=invalid_info,invalid_required_field=invalid_required_field)  # Show the login form


@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    
    return redirect('/login')
@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        session.pop("user", None)
        # flash("Your session has ended log in again")
        session["_session_ended"] = True  # Set session ended flag
        return redirect(url_for("login"))
    else:
        # Handle GET request for /logout route (optional)
        return redirect(url_for("login"))


@app.route('/register',methods=['GET','POST'])
def register():
    print("register enterd") 
    if request.method == 'POST':
        print("enter post")
        # handle request
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print("name ::: ", username)
        print("email ::: ", email)
        print("password ::: ", password)

        new_user = User(name=username,email=email,password=password)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    
    return render_template('register.html')

@app.route('/index')
def index():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            return render_template('index.html', user=user)
        else:
            return redirect(url_for('login'))  # Redirect to login if the user is not found
    return redirect(url_for('login'))

@app.route('/video_upload', methods=['GET','POST'])
def video_index():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            return render_template('upload_video.html')
        else:
            return redirect(url_for('login'))  # Redirect to login if the user is not found
    return redirect(url_for('login'))



@app.route('/upload_video', methods=['GET','POST'])
def video_upload_file():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            if 'video' not in request.files:
                return "No file part"
            file = request.files['video']
            if file.filename == '':
                return "No selected file"
            if file:
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                    
                video_path = file_path.split('\\')
                print(f"\n{video_path}\n")
                
                os.system(f"cd yolov5_video_upload/ && python detect_new.py --weights ./runs/train/yolov5s_results/weights/best.pt --img 416 --conf 0.4 --source ../{video_path[0]}/{video_path[1]}")
                # time.sleep(2)
                os.system("cd ..")

                # Example usage:
                source_directory = 'yolov5_video_upload/runs/detect/exp/'
                destination_directory = "static/processed_video/"
                image_filename = video_path[1]

                source_path = os.path.join(source_directory, image_filename)
                destination_path = os.path.join(destination_directory, image_filename)

                move_image(source_path, destination_path)
                shutil.rmtree(source_directory)

                processed_image_path = f'static/processed_video/{video_path[1]}'
                print(processed_image_path)
                print(os.getcwd())



                # Define the input and output paths
                input_path = processed_image_path
                output_path = f"static/out/{video_path[1][:-4]}.avi"
                converter(input_path, output_path)
                converter(output_path, f"static/processed_video/aaa{video_path[1]}")

                # print(video_path[1])


                return render_template('result_video_display.html', processed_video=video_path[1])
            else:
             return render_template('upload_video.html')
        else:
            redirect(url_for('login'))
    return redirect(url_for('login'))
    

if __name__ == '__main__':
    app.run(debug=True)



# cd yolov5/ && python detect.py --weights ./runs/train/yolov5s_results4/weights/best.pt --img 416 --conf 0.2 --source 0
