"""Static, resolution-independent diagrams for the portfolio."""
from math import sin, exp, pi
from pathlib import Path


def path(points):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points)


def lines(points, color, width=1, opacity=1):
    return f'<path d="{path(points)}" fill="none" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>'


def diagram(folder: Path):
    # Parallel projection keeps the pipeline readable at any viewport size.
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 365">', '''
    <defs><radialGradient id="halo"><stop stop-color="#18bfa5" stop-opacity=".16"/>
    <stop offset="1" stop-color="#18bfa5" stop-opacity="0"/></radialGradient>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r=".85" fill="#6d9397" opacity=".42"/></pattern></defs>
    <rect width="560" height="365" fill="url(#dots)"/>
    <ellipse cx="270" cy="174" rx="236" ry="165" fill="url(#halo)"/>''']
    for level, color in [(2, "#467b83"), (1, "#42a99e"), (0, "#72ebd1")]:
        def project(u, v):
            envelope = (1-u*u) * (1-v*v)
            peak = exp(-((u+.1)**2*2.4+(v-.02)**2*1.9))
            wave = (64*peak + 24*sin(u*3.3-v*3.7)*envelope) * [1,.36,.04][level]
            return 247+107*u-97*v, 152+40*u+38*v+level*48-wave

        # Closed silhouette gently occludes each layer underneath.
        edge = [project(-1+i/20,-1) for i in range(41)]
        edge += [project(1,-1+i/20) for i in range(41)]
        edge += [project(1-i/20,1) for i in range(41)]
        edge += [project(-1,1-i/20) for i in range(41)]
        parts.append(f'<path d="{path(edge)}Z" fill="#102528" fill-opacity=".82"/>')
        for i in range(33):
            t = -1+i/16
            grid = [-1+j/14 for j in range(29)] if level < 2 else [-1,0,1]
            parts.append(lines([project(t,v) for v in grid], color, .77, .9))
            parts.append(lines([project(u,t) for u in grid], color, .77, .74))
        parts.append(lines(edge+[edge[0]],color,1.1))
    for x, y, tx, ty, title in [(330,131,428,86,"INPUT"),(368,184,433,172,"ORCHESTRATE"),(329,255,429,267,"EVALUATE")]:
        parts.append(lines([(x,y),(tx-18,ty),(tx-3,ty)],"#79a29e",.85))
        parts.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="#9bf7df"/><text x="{tx+3}" y="{ty+4}" font-family="monospace" font-size="11.5" letter-spacing="1" fill="#c1d9d5">{title}</text>')
    parts.append('</svg>')
    (folder/'agent-workflow.svg').write_text(''.join(parts),encoding='utf8')


def covers(folder: Path):
    # These are conceptual signal and data-flow illustrations, not measurements.
    waves = []
    for i in range(37):
        pts = []
        for x in range(0,641,5):
            u = x/640
            envelope = sin(pi*u)**1.7
            y = 138 + (i-18)*2.7 + envelope*(40*sin(10*u+i*.105)+33*sin(18*u-i*.14))
            pts.append((x,y))
        waves.append(lines(pts,"#ffa58d",.95,.76))
    network = []
    for i in range(11):
        y = 50+i*18
        target = 87+(i%4)*31
        network.append(f'<path d="M-4 {y} H118 C177 {y} 152 {target} 220 {target} H310 C365 {target} 363 138 425 138 H655" stroke="#88b5ff" fill="none" stroke-width="1.3" opacity=".8"/>')
        network.append(f'<circle cx="{95+i*1.6}" cy="{y}" r="3.2" fill="#b9d1ff"/>')
    for x,y in [(221,87),(265,118),(230,149),(300,180),(424,138),(530,138)]:
        network.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#182d50" stroke="#c2d9ff" stroke-width="2"/>')
    for name,bg,fg,body in [('litmus','#452c2b','#b88f83',waves),('crypto-risk-agent','#192d4a','#89a7c5',network)]:
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 270"><defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{fg}" opacity=".19"/></pattern></defs><rect width="640" height="270" fill="{bg}"/><rect width="640" height="270" fill="url(#grid)"/>'
        (folder/f'{name}.svg').write_text(svg+''.join(body)+'</svg>',encoding='utf8')

