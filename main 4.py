import os, random, string, json, requests, subprocess
from flask import Flask, render_template, request
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def run_bot():
    print("Bot started!")
    subprocess.Popen(['python', 'bot.py'])

def uploadfile(file:str):
    files = {'files[]': open(file, 'rb'),}
    response = requests.post('https://up1.fileditch.com/upload.php', files=files)

    if response.status_code == 200:
        print("File uploaded successfully!")
        return json.loads(response.text)["files"][0]["url"]
    else:
        print(f"Failed to upload. Status code: {response.status_code}")
    
def downloadimg(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        if img.format != 'PNG':
            img = img.convert('RGB')

        img_dir = 'img'
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)

        img_path = os.path.join(img_dir, random_string(10) + '.png')
        img.save(img_path, 'PNG')
        return img_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return 'fail'

def random_string(length:int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        img = downloadimg(request.form['url'])

        if img != 'fail':
            uploaded_url = uploadfile(img)
            os.remove(img)
            return render_template('index.html', message=f'Image uploaded to FileDitch: {uploaded_url}', url=uploaded_url), 200
        else:
            return render_template('index.html', message='Error: Unable to download the image.'), 400
        
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
        img = downloadimg(request.form['url'])

        if img != 'fail':
            uploaded_url = uploadfile(img)
            os.remove(img)
            return uploaded_url, 200
        else:
            return uploaded_url, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10588, debug=True)