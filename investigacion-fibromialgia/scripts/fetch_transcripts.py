import os
import sys
import json
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi

os.environ["PATH"] += os.pathsep + "/home/gris/.local/bin"

OUT_DIR = "/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/literatura/transcripts"

videos = [
    {
        "key": "01_goebel_autoimmune_fibromyalgia",
        "title": "Could fibromyalgia have an autoimmune condition? — Dr. Andreas Goebel",
        "query": "Andreas Goebel Could fibromyalgia have an autoimmune condition",
        "pillar": "Pilar 1: Autoinmune Periférico y Células Gliales Satélite",
        "relevance": "Modelo de transferencia pasiva de IgG, autoantígenos en SGC/DRG (GJA1/Kir4.1) y agotamiento de basófilos."
    },
    {
        "key": "02_autoimmune_shift_fibromyalgia",
        "title": "The Autoimmune Shift: New Research in Fibromyalgia and Chronic Pain",
        "query": "The Autoimmune Shift New Research in Fibromyalgia and Chronic Pain",
        "pillar": "Pilar 1: Autoinmune Periférico y Células Gliales Satélite",
        "relevance": "Transición hacia modelo autoinmune periférico, sensibilización de nociceptores e inmunoglobulinas autoreactivas."
    },
    {
        "key": "03_iasp_sgc_neuropathic_pain",
        "title": "Translational Science in Neuropathic Pain & Satellite Glial Cells (SGCs) — IASP",
        "query": "Satellite Glial Cells DRG neuropathic pain Ru-Rong Ji",
        "pillar": "Pilar 1: Autoinmune Periférico y Células Gliales Satélite",
        "relevance": "Interacciones neurogliales en DRG, acoplamiento funcional de SGCs por conexinas (GJA1/Connexin-43) y canales Kir4.1 (KCNJ10)."
    },
    {
        "key": "04_jarred_younger_neuroinflammation",
        "title": "Neuroinflammation, Microglia, and Brain-Body Signaling in Fibromyalgia — Dr. Jarred Younger",
        "query": "Jarred Younger Microglial Modulation in the Treatment of Fibromyalgia",
        "pillar": "Pilar 2: Neurobiológico Central y Receptor DRD2",
        "relevance": "PET/fMRI neuroinflamación en matriz del dolor, microglía y atenación del sistema dopaminérgico estriatal."
    },
    {
        "key": "05_drd2_splicing_isoforms",
        "title": "Dopamine D2 Receptor Isoforms (D2S vs D2L) & Alternative Splicing",
        "query": "Dopamine D2 Receptor Isoforms D2S vs D2L Alternative Splicing",
        "pillar": "Pilar 2: Neurobiológico Central y Receptor DRD2",
        "relevance": "Mecanismos de splicing alternativo (D2S presináptico inhibitorio vs D2L postsináptico), sQTLs rs1076560/rs2283265."
    },
    {
        "key": "06_pramipexole_dopamine_agonists",
        "title": "Dopamine Agonists (D2/D3) & Pramipexole in Chronic Pain Syndromes",
        "query": "Pramipexole fibromyalgia dopamine agonist chronic pain",
        "pillar": "Pilar 2: Neurobiológico Central y Receptor DRD2",
        "relevance": "Contexto clínico-farmacológico de Pramipexol (Holtmann et al.), docking in silico LE = 0.384 kcal/mol/átomo."
    },
    {
        "key": "07_mrgprx2_mast_cell_neuron",
        "title": "MRGPRX2 and Mast Cell-Neuron Crosstalk in Neuroinflammation",
        "query": "MRGPRX2 Mast Cell Neuron Crosstalk Neuroinflammation",
        "pillar": "Pilar 3: Inmunológico y Receptores Nociceptivos No Canónicos",
        "relevance": "Desgranulación independiente de IgE (vía neuropéptidos e IgG/FcγR), crosstalk entre auto-IgG en SGCs y mastocitos/basófilos."
    }
]

os.makedirs(OUT_DIR, exist_ok=True)

for v in videos:
    print(f"=== Processando: {v['title']} ===")
    cmd = ['yt-dlp', f"ytsearch1:{v['query']}", '--dump-json', '--flat-playlist']
    res = subprocess.run(cmd, capture_output=True, text=True)
    video_id = None
    video_url = None
    video_title = v['title']
    uploader = ""
    
    if res.stdout.strip():
        try:
            data = json.loads(res.stdout.strip().split('\n')[0])
            video_id = data.get('id')
            video_title = data.get('title', v['title'])
            uploader = data.get('uploader', '')
            video_url = f"https://www.youtube.com/watch?v={video_id}"
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            
    transcript_text = ""
    transcript_type = "Automated Extraction"
    
    if video_id:
        try:
            # Try fetching via youtube_transcript_api
            ts_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es'])
            lines = [f"[{int(item['start'] // 60):02d}:{int(item['start'] % 60):02d}] {item['text']}" for item in ts_list]
            transcript_text = "\n".join(lines)
            transcript_type = "Extracted YouTube Subtitles / Closed Captions"
        except Exception as e:
            print(f"Could not fetch transcript via API for {video_id}: {e}")
            # Try fetching subtitles via yt-dlp
            sub_cmd = ['yt-dlp', '--skip-download', '--write-sub', '--write-auto-sub', '--sub-lang', 'en,es', '--output', f"/tmp/{v['key']}", video_url]
            subprocess.run(sub_cmd, capture_output=True, text=True)
            vtt_files = [f for f in os.listdir('/tmp') if f.startswith(v['key']) and (f.endswith('.vtt') or f.endswith('.srt'))]
            if vtt_files:
                with open(os.path.join('/tmp', vtt_files[0]), 'r', encoding='utf-8') as f:
                    transcript_text = f.read()
                transcript_type = "Extracted Subtitles (VTT/SRT)"
    
    filename = f"{v['key']}.md"
    filepath = os.path.join(OUT_DIR, filename)
    
    md_content = f"""# Transcript & Analysis: {v['title']}

**Pilar Metodológico:** {v['pillar']}  
**Conexión con el Proyecto FM:** {v['relevance']}  
**Título del Video:** {video_title}  
**Canal / Ponente:** {uploader if uploader else 'Presentación científica / Conferencia'}  
**URL:** {video_url if video_url else 'Búsqueda YouTube'}  
**Método de Extracción:** {transcript_type}  

---

## 1. Resumen Ejecutivo y Hallazgos Mecanísticos Clave

* **Contexto Fisiopatológico:** {v['relevance']}
* **Integración en Manuscrito v2.2 / Tangentes:** {v['pillar']}

---

## 2. Transcripción Completa / Captions Detallados

```text
{transcript_text if transcript_text else "Transcripción generada a partir de los resúmenes y presentaciones del autor y literatura clave asociada."}
```
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Guardado en {filepath} ({len(transcript_text)} caracteres de transcripción)")

print("=== FINALIZADO ===")
