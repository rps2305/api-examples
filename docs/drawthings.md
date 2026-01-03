# Draw Things

## Overview
Draw Things is an on-device AI image generation app. The project maintains a wiki with model and usage guidance. If you are integrating via automation, consult the wiki for available interfaces or export formats.

## Python
```python
prompt = (
    "Prompt: a cozy cabin in a snowy forest, cinematic lighting\n"
    "Negative prompt: low quality, blurry\n"
    "Steps: 30\n"
    "Sampler: DPM++ 2M Karras\n"
)

with open("drawthings_prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

print("Saved drawthings_prompt.txt. Paste the contents into Draw Things.")
```

## PowerShell
```powershell
$prompt = @"
Prompt: a cozy cabin in a snowy forest, cinematic lighting
Negative prompt: low quality, blurry
Steps: 30
Sampler: DPM++ 2M Karras
"@

$prompt | Out-File -FilePath "drawthings_prompt.txt" -Encoding utf8
Write-Host "Saved drawthings_prompt.txt. Paste the contents into Draw Things."
```

## curl
```bash
cat > drawthings_prompt.txt <<'EOF'
Prompt: a cozy cabin in a snowy forest, cinematic lighting
Negative prompt: low quality, blurry
Steps: 30
Sampler: DPM++ 2M Karras
EOF

echo "Saved drawthings_prompt.txt. Paste the contents into Draw Things."
```

## Docs
- https://wiki.drawthings.ai/wiki/Main_Page
