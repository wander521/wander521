"""Build repository-owned badges using official Simple Icons geometry."""
import html
from pathlib import Path
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1] / 'assets'
target = root / 'badges'
target.mkdir(exist_ok=True)

def badge(slug,label,status,color,wide=False):
    size=32 if wide else 28
    left=max(92,int(len(label)*7.7+44))
    right=103 if status=='Coming soon' else max(58,int(len(status)*7.2+20))
    width=left+right
    geometry=''
    icon=root/'icons'/(slug+'.svg')
    if icon.exists():
        element=ET.fromstring(icon.read_text())
        for node in element.iter():
            if node.tag.split('}')[-1]=='path':
                geometry+=f'<path d="{html.escape(node.attrib["d"],quote=True)}"/>'
    else:
        geometry='<path d="M4 4h16v16H4z M8 9h8 M8 13h8 M8 17h5" fill="none" stroke="white" stroke-width="2"/>'
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{size}" viewBox="0 0 {width} {size}" role="img" aria-label="{html.escape(label)}: {html.escape(status)}"><title>{html.escape(label)} · {html.escape(status)}</title><path fill="#30363d" d="M0 0h{left}v{size}H0z"/><path fill="{color}" d="M{left} 0h{right}v{size}H{left}z"/><g fill="white" transform="translate(10 {(size-16)/2}) scale(.6667)">{geometry}</g><g fill="white" font-family="Arial,sans-serif" font-size="13"><text x="34" y="{size/2+4.5}">{html.escape(label)}</text><text x="{left+right/2}" y="{size/2+4.5}" text-anchor="middle" font-weight="600">{html.escape(status)}</text></g></svg>'''
    (target/(slug+'.svg')).write_text(svg)

for args in [('telegram','Telegram','Coming soon','#087eac',True),('discord','Discord','Coming soon','#5865f2',True),('blog','Blog','Coming soon','#b51242',True),('csdn','CSDN','Soon','#bd351a'),('juejin','Juejin','Soon','#155fc9'),('zhihu','Zhihu','Soon','#155fc9'),('bilibili','Bilibili','Soon','#087eac'),('infoq','InfoQ','Soon','#155fc9'),('jianshu','Jianshu','Soon','#b84735'),('segmentfault','SegmentFault','Soon','#08754a'),('gitee','Gitee','Soon','#b21920'),('python','Python','Build','#245a86'),('fastapi','FastAPI','APIs','#007f73'),('ros','ROS 2','Robotics','#243746'),('android','Android','Devices','#08754a'),('mysql','MySQL','Data','#245a86'),('redis','Redis','State','#b21920'),('openjdk','Java','Systems','#b84735')]:
    badge(*args)
print('Built 18 local badges')
