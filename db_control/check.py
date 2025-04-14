import base64

# ↓ここに実際の base64 の音声データを貼り付けてください（短縮しています）
base64_data = """
SUQzBAAAAAAAI1RTU0MAAAAAAAA//tQxAADBzYAAf7///7///8aAwAAAAAAAAAA...
"""  # ↑実際の長い文字列に置き換えてください（前後のスペースや改行は削除）

# base64 → バイトデコード
try:
    audio_bytes = base64.b64decode(base64_data)
except Exception as e:
    print("base64デコードに失敗:", e)
    exit()

# MP3ファイルとして保存
output_path = "test_output.mp3"
with open(output_path, "wb") as f:
    f.write(audio_bytes)

print(f"ファイルを保存しました: {output_path}")
print("このファイルを音楽プレイヤーで開いて再生できるか確認してください。")
