from google import genai
from google.genai import types

from dotenv import load_dotenv
import os


load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def translate_script(script):
    """
    스크립트를 한국어로 번역하는 함수
    
    Args:
        script (str): 번역할 스크립트
        
    Returns:
        str: 번역된 텍스트
    """
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = """
            당신은 중국어-한국어 번역 전문가입니다. 
            당신에게는 최대 30분 분량의 중국어 뉴스에서 발췌한 스크립트가 주어질 것이고,
            당신의 역할은 그러한 긴 스크립트를 모두 빠짐없이, 문장 단위로 정확하게 한국어로 번역하고 원문의 간체 중국어 병음을 제공하는 것입니다.

            당신의 답변은 특정한 형태를 따라야 합니다. 
            예를 들어, 다음과 같은 간체 중국어 텍스트를 입력받았다고 해보겠습니다:

            各位观众，晚上好。晚上好。

            이러한 텍스트를 입력받았을 때, 당신의 답변은 다음과 같아야 합니다:

            各位观众，晚上好。
            Gèwèi guānzhòng, wǎnshàng hǎo.
            여러분 시청자 여러분, 안녕하세요.

            晚上好。
            Wǎnshàng hǎo.
            안녕하세요.

            위와 같이 답변을 제공할 때, 반드시 문장 단위로 줄바꿈을 하여 답변을 제공하세요. 여러 문장을 한꺼번에 묶지 마세요.
            """

        response = client.models.generate_content(
            model='models/gemini-2.5-flash',
            contents=types.Content(
                parts=[
                    types.Part(text=script),
                    types.Part(text=prompt)
                ]
            )
        )
        
        return response.text
        
    except Exception as e:
        print(f"번역 중 오류 발생: {e}")
        return None

if __name__ == "__main__":
    script = """
    那走马楼三国吴简中，数量最多的简牍是什么呢？作为临湘的官府文书，这里数量最多的，就是关于税收的简牍，大约有三万余枚。比方说，有一个非常具有代表性的简册，嘉禾吏民田家襎。它是由2194枚木简组成的。嘉禾是年号嘛，吏民是指这里的百姓，田家是种庄稼的人嘛。襎是一种文书制度了。木简的顶部啊，有一些很有意思的条纹。后来发现，这是"同文"字样。古人把它切成三片，每一片都写一模一样的内容，其实这就是凭证啊。就相当于我们现在三联单的形式。谁拿着这些凭证呢？就是具体负责这件事的官府机构，监管机构、农民本人。核验的时候，给它拼到一起，能够拼出那个"同"字来。那这就是一个真文书。那你说是拼起这个"同"的过程叫做什么呀？我们可以叫做合对不对？所以这个行为可以叫什么呀？叫合同嘛。嘉禾吏民田家襎，也就被视为中国迄今发现的最早的、形制最大的田租类实物合同券书。
    """
    translation = translate_script(script)
    print(translation)