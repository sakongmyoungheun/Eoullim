#  Flask 모듈에서 Flask 클래스와 request 객체를 가져옵니다.
# request 객체는 클라이언트로부터 요청을 받은 정보를 담고 있습니다
from flask import Flask, request
from text_to_speach import reason_to_text
from speach_to_text import speach_to_text
from werkzeug.utils import secure_filename
import model

# Flask 애플리케이션을 생성합니다. __name__은 현재 모듈의 이름을 의미합니다.
app = Flask(__name__)

# /upload' 경로로의 POST 요청을 처리하는 데코레이터를 정의합니다.
# 즉, 클라이언트에서 '/upload' 경로로 POST 요청이 오면 upload_file 함수를 실행합니다.
@app.route('/file', methods=['POST'])
def upload_file():

    # 'video' 키에 해당하는 파일 가져오기
    if 'video' not in request.files:
        return 'No file part'

    file = request.files['video']
    
    # 파일 저장 경로 설정 (선택사항)
    # 파일명을 유일하게 만들어야 하므로 secure_filename을 사용하여 안전하게 파일명을 생성합니다.
    filename = secure_filename(file.filename)
    file.save('./' + filename)
    real_file_type = filename.split('.')[-1]

    if real_file_type == 'mp4':
        # 영상을 모델에 넣어 텍스트를 출력하는 과정
        ilist = model.video_landmark_dic('./' + filename)
        print('ilist', ilist)
        # 모델에서 나온 텍스트를 음성으로 변환하는 함수 적용
        sen_result = reason_to_text(ilist) # 일단 result 는 텍스트 파일
        return sen_result
        
    elif real_file_type == 'mp3':
        # 음성을 텍스트로 변환하는 함수 적용
        text_result = speach_to_text(filename) # 일단 resilt 는 텍스트 파일

    else:
        print('파일이 제대로 넘어오지 않았습니다')

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



