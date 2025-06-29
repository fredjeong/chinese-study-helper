from google import genai
from google.genai import types

from googleapiclient.discovery import build
# from dotenv import load_dotenv
import os


# load_dotenv()

# YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def extract_title(video_url):
    """
    유튜브 영상의 제목을 추출하는 함수
    
    Args:
        video_url (str): 유튜브 영상 URL
        
    Returns:
        str: 영상 제목
    """
    try:
        # URL에서 video_id 추출
        if "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[1].split("?")[0]
        elif "youtube.com/watch?v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        else:
            raise ValueError("지원하지 않는 유튜브 URL 형식입니다.")

        # 동영상 정보 요청
        youtube = build('youtube', 'v3', developerKey=os.environ['YOUTUBE_API_KEY'])
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        
        if response['items']:
            return response['items'][0]['snippet']['title']
        else:
            raise ValueError("영상을 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"제목 추출 중 오류 발생: {e}")
        return None

if __name__ == "__main__":
    video_url = 'https://youtu.be/i-IUu1yyZcs?feature=shared'
    title = extract_title(video_url)
    print(title)