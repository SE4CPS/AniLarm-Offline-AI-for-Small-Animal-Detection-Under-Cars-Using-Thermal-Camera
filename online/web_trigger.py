from flask import Flask, render_template, request, send_file
import subprocess
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>Animal Detection Trigger</h1>
        <form action="/run-detect" method="post">
            <button type="submit">Run Animal Detection</button>
        </form>
    '''

@app.route('/run-detect', methods=['POST'])
def run_detect():
    try:
        captured_images = []
        start_time = time.time()
        image_count = 0
        
        while time.time() - start_time < 10:
            image_path = f"output_{image_count}.png"
            subprocess.run(['sudo', './seek_snapshot', '-o', image_path], check=True)
            captured_images.append(image_path)
            image_count += 1
            time.sleep(1)  

        
        result = subprocess.run(['python3', '/home/animal/libseek-thermal/build/examples/detect.py'] + captured_images,
                                capture_output=True, text=True) #change the path here to your directory where your script is , as it is my raspberry pi directory location for all scripts.

        images_html = ""
        for image in captured_images:
            color_image_path = f"color_{os.path.basename(image)}"
            if os.path.exists(color_image_path):
                images_html += f'<img src="/image?name={color_image_path}" alt="Captured Image" width="500"><br>'
        
        return f'''
            <h2>Animal Detection Results</h2>
            <pre>{result.stdout}</pre>
            {images_html}
            <a href="/">Go Back</a>
        '''
    except Exception as e:
        return f'<h2>Error Occurred</h2><p>{str(e)}</p><a href="/">Go Back</a>'

@app.route('/image')
def image():
    image_name = request.args.get("name")
    image_path = os.path.join(os.getcwd(), image_name)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        return '<h2>No Image Found</h2><a href="/">Go Back</a>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
