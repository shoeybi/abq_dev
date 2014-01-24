from PIL import Image
from PIL import ImageFont, ImageDraw

#---------------------------------------------------------------
# make a wallpaper
#---------------------------------------------------------------
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

#---------------------------------------------------------------
# make a thumbnail
#---------------------------------------------------------------
def make_thumb(raw, result, status):
    thumb  = Image.open(raw)
    if status in ['TR', 'PA', 'ST', 'SU']:
        white = Image.new(thumb.mode,thumb.size,color=(256,256,256))
        thumb = Image.blend(white,thumb,0.5)
        
        draw  = ImageDraw.Draw(thumb)
        fontH = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf', 225)
        color = (0,0,0)
        
        y_pos = 250
        
        if status == 'TR' :
            text 	= 'Terminated'
            x_pos 	= 10

        if status == 'PA' :
            text 	= 'Paused'
            x_pos 	= 220

        if status == 'ST' :
            text 	= 'Stopping'
            x_pos 	= 160

        if status == 'SU' :
            text 	= 'Starting up'
            x_pos 	= 30
        
    
    	draw.text((x_pos,y_pos),text,color,font=fontH)
        
    thumb.save(result)
 

