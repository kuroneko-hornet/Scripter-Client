# Scripter-Client
on the console, run:
```
python3 ScripterClient.py
```

# how to write json file "script info"
```
{
    script-1: {
        "text": "テスト1",
        "duration": [1.0, 2.5],
        (optional) "fontsize": 50, 
        (optional) "font": "ヒラギノ丸ゴ-ProN-W4",
        (optional) "color": "white",
        (optional) "pos": "pos=('center', 'bottom')"
    },
    script-2: {
        ...
    },
    ...
} 
```

# Requirement
```
brew install python3
brew install imagemagick
brew install python-tk
pip install moviepy
pip install wx
```