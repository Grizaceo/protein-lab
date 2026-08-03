import os
from youtube_transcript_api import YouTubeTranscriptApi

try:
    ts = YouTubeTranscriptApi.get_transcript('NrMJsED-JyQ', languages=['en', 'fr', 'es'])
    lines = [f"[{int(item['start'] // 60):02d}:{int(item['start'] % 60):02d}] {item['text']}" for item in ts]
    text = "\n".join(lines)
    print("Fetched", len(text), "chars")
    path = '/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/literatura/transcripts/01_goebel_autoimmune_fibromyalgia.md'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace transcript block
    new_block = f"```text\n{text}\n```"
    if "```text\n\n```" in content:
        content = content.replace("```text\n\n```", new_block)
    else:
        content += f"\n\n## 2. Transcripción Completa\n{new_block}"
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated 01_goebel_autoimmune_fibromyalgia.md successfully!")
except Exception as e:
    print("Error:", e)
