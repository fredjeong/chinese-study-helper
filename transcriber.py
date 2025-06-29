from google import genai
from google.genai import types
import os


def transcribe_video(video_url):
    """
    유튜브 영상의 스크립트를 추출하는 함수
    
    Args:
        video_url (str): 유튜브 영상 URL
        
    Returns:
        str: 영상 스크립트
    """
    try:
        client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
        
        response = client.models.generate_content(
            model='models/gemini-2.5-flash',
            contents=types.Content(
                parts=[
                    types.Part(
                        file_data=types.FileData(file_uri=video_url)
                    ),
                    types.Part(text='Transcribe the audio from this video, without any timestamps.')
                ]
            )
        )
        
        return response.text
        
    except Exception as e:
        print(f"스크립트 추출 중 오류 발생: {e}")
        return None

# 테스트
if __name__ == "__main__":
    video_url = 'https://youtu.be/i-IUu1yyZcs?feature=shared'
    script = transcribe_video(video_url)
    print(script)

