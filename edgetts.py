import asyncio
import edge_tts
import os
from pathlib import Path
from typing import Optional

async def generate_audio_with_subtitles(
    input_file: str = "ttsinput.txt",
    voice: str = "zh-CN-XiaoxiaoNeural",
    output_audio: str = "chinese_output.mp3",
    output_srt: str = "chinese_output.srt",
    encoding: str = "utf-8",
    subtitle_max_line_length: Optional[int] = None,
) -> None:
    """
    生成带字幕的语音文件
    
    :param input_file: 输入文本文件路径
    :param voice: 语音模型名称（支持多种中文语音，详见下方说明）
    :param output_audio: 输出音频文件路径
    :param output_srt: 输出字幕文件路径
    :param encoding: 文件编码格式
    :param subtitle_max_line_length: 字幕每行最大长度
    
    中文语音模型示例：
    zh-CN-XiaoxiaoNeural               Female    News, Novel            Warm
    zh-CN-XiaoyiNeural                 Female    Cartoon, Novel         Lively，活泼

    zh-CN-liaoning-XiaobeiNeural       Female    Dialect，方言          Humorous，幽默
    zh-CN-shaanxi-XiaoniNeural         Female    Dialect，方言          Bright，明亮

    zh-CN-YunjianNeural                Male      Sports, Novel          Passion，激情
    zh-CN-YunxiNeural                  Male      Novel                  Lively, Sunshine，活泼，阳光
    zh-CN-YunxiaNeural                 Male      Cartoon, Novel         Cute，可爱
    zh-CN-YunyangNeural                Male      News                   Professional, Reliable，专业，可靠
    """
    try:
        # 确保输出目录存在
        Path(output_audio).parent.mkdir(parents=True, exist_ok=True)
        Path(output_srt).parent.mkdir(parents=True, exist_ok=True)

        # 读取输入文件
        with open(input_file, "r", encoding=encoding) as f:
            text = f.read().strip()

        if not text:
            raise ValueError("输入文件内容为空")

        # 初始化语音合成器
        communicate = edge_tts.Communicate(text, voice)
        submaker = edge_tts.SubMaker()

        # 流式处理音频和字幕
        with open(output_audio, "wb") as audio_file:  # 同步写入
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.feed(chunk)

        # 处理字幕格式
        srt_content = submaker.get_srt()
        if subtitle_max_line_length:
            srt_content = split_long_lines(srt_content, subtitle_max_line_length)

        # 写入字幕文件
        with open(output_srt, "w", encoding=encoding) as srt_file:  # 同步写入
            srt_file.write(srt_content)

        print(f"生成成功：\n音频文件 -> {output_audio}\n字幕文件 -> {output_srt}")

    except Exception as e:
        print(f"处理过程中发生错误：{str(e)}")
        # 清理可能生成的空文件
        for path in [output_audio, output_srt]:
            if os.path.exists(path) and os.path.getsize(path) == 0:
                os.remove(path)

def split_long_lines(srt_content: str, max_length: int) -> str:
    """拆分长字幕行"""
    lines = []
    for line in srt_content.split("\n"):
        if len(line) > max_length and " --> " not in line and not line.isdigit():
            line = "\n".join([line[i:i+max_length] for i in range(0, len(line), max_length)])
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    asyncio.run(generate_audio_with_subtitles(
        input_file="ttsinput.txt",
        output_audio="output/chinese_audio.mp3",
        # output_srt="subtitles/chinese_subs.srt",
        output_srt="output/chinese_subs.srt",
        subtitle_max_line_length=35
    ))