import Image, ImageFont, ImageDraw

def make_wallpaper(raw, result, team_name, workspace_name, users): 
    
    Back  = Image.open(raw)
    draw  = ImageDraw.Draw(Back)

    fontB  = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf', 32)
    font   = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-L.ttf', 32)
    fontsB = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf', 24)
    fonts  = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-L.ttf', 24)

    x_shift = 750
    y_shift = 100
    x_tab   = 190
    y_tab   = 40
    y_tabs  = 32

    title_color = (160,160,160)
    text_color  = (160,160,160)

    draw.text((x_shift+0,   y_shift+0),        'team',       title_color,font=fontB)
    draw.text((x_shift+0,   y_shift+y_tab),    'workspace',  title_color,font=fontB)
    draw.text((x_shift+0,   y_shift+2.5*y_tab),'team members',    title_color,font=fontsB)

    draw.text((x_shift+x_tab, y_shift+0),      team_name,     text_color,font=font)
    draw.text((x_shift+x_tab, y_shift+y_tab),  workspace_name,text_color,font=font)
    i = 0
    for user in users:
        if i == 0:
            user += ' (lead)'
        draw.text((x_shift+x_tab, y_shift+2.5*y_tab+i*y_tabs), user,text_color,font=fonts)
        i = i + 1
    Back.save(result)

raw     	= '1.png'
result  	= 'res.png'
users   	= ['Moahammad Shoeybi','Yaser Khalighi','David Corson'] 
team_name	= 'Abaqual'
workspace_name	= 'my workspace 2'

make_wallpaper(raw, result, team_name, workspace_name, users)

