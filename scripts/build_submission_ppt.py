from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls
from pathlib import Path

OUT = Path('/mnt/data/INT396_Worksite_Project_Submission.pptx')
ROOT = Path(__file__).resolve().parents[1]

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

# Worksite visual system
FOREST = '20352D'
FOREST2 = '2D493E'
INK = '202A27'
MUTED = '68736D'
PAPER = 'F2F0E9'
WHITE = 'FFFFFF'
RUST = 'B85C38'
GOLD = 'D2A15F'
LINE = 'D8DCD4'
PALE = 'E7E9E1'
PALE_RUST = 'F3E7DF'
PALE_GREEN = 'E4ECE6'
BLUE = '5D7F86'

FONT = 'Aptos'
HEAD = 'Georgia'


def rgb(h):
    return RGBColor.from_string(h)


def set_bg(slide, color=PAPER):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(color)


def add_text(slide, x, y, w, h, text, size=14, color=INK, bold=False,
             font=FONT, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP,
             margin=0.03, italic=False, fit=True):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_after = Pt(0)
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = rgb(color)
    if fit:
        try:
            tf.fit_text(font_family=font, max_size=size)
        except Exception:
            pass
    return box


def add_rich_paragraphs(slide, x, y, w, h, lines, size=13, color=INK,
                        bullet=False, gap=7, font=FONT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    for i, item in enumerate(lines):
        if isinstance(item, tuple):
            lead, body = item
        else:
            lead, body = '', item
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        p.level = 0
        if bullet:
            p.text = ''
            pPr = p._p.get_or_add_pPr()
            pPr.insert(0, parse_xml(f'<a:buChar {nsdecls("a")} char="•"/>'))
        if lead:
            r = p.add_run(); r.text = lead
            r.font.name = font; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = rgb(color)
        r = p.add_run(); r.text = body
        r.font.name = font; r.font.size = Pt(size); r.font.color.rgb = rgb(color)
    return box


def add_shape(slide, x, y, w, h, fill=WHITE, line=LINE, radius=True, line_width=0.8):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.fill.solid(); shape.fill.fore_color.rgb = rgb(fill)
    shape.line.color.rgb = rgb(line)
    shape.line.width = Pt(line_width)
    if radius:
        try: shape.adjustments[0] = 0.08
        except Exception: pass
    return shape


def add_line(slide, x1, y1, x2, y2, color=LINE, width=1.0, dash=None):
    shp = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    shp.line.color.rgb = rgb(color)
    shp.line.width = Pt(width)
    if dash:
        shp.line.dash_style = dash
    return shp


def add_pill(slide, x, y, w, text, fill=PALE_GREEN, color=FOREST, size=9):
    add_shape(slide, x, y, w, 0.32, fill=fill, line=fill, radius=True, line_width=0.2)
    add_text(slide, x+0.05, y+0.025, w-0.1, 0.25, text, size=size, color=color, bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)


def header(slide, num, section, title, subtitle=''):
    set_bg(slide)
    add_text(slide, 0.62, 0.30, 7.0, 0.25, f'INT396  /  SIH26165     •     {section.upper()}', 9, RUST, True)
    add_text(slide, 0.62, 0.66, 12.0, 0.56, title, 27, FOREST, True, font=HEAD)
    if subtitle:
        add_text(slide, 0.66, 1.26, 12.0, 0.43, subtitle, 11, MUTED)
    add_line(slide, 0.65, 1.78, 12.68, 1.78, LINE, 0.8)
    add_line(slide, 0.65, 7.08, 12.68, 7.08, LINE, 0.6)
    add_text(slide, 0.66, 7.13, 5.5, 0.18, 'WORKSITE  /  INCIDENT INTELLIGENCE', 8, MUTED, True)
    add_text(slide, 12.0, 7.11, 0.65, 0.2, f'{num:02d} / 14', 8, MUTED, True, align=PP_ALIGN.RIGHT)


def card(slide, x, y, w, h, title, body=None, accent=RUST, fill=WHITE, title_size=15, body_size=11):
    add_shape(slide, x, y, w, h, fill=fill, line=LINE)
    add_shape(slide, x, y, 0.06, h, fill=accent, line=accent, radius=False, line_width=0)
    add_text(slide, x+0.22, y+0.16, w-0.42, 0.35, title, title_size, FOREST, True, font=HEAD)
    if body:
        if isinstance(body, list):
            add_rich_paragraphs(slide, x+0.2, y+0.64, w-0.4, h-0.78, body, body_size, INK, gap=5)
        else:
            add_text(slide, x+0.22, y+0.64, w-0.43, h-0.78, body, body_size, INK)


def add_link(run, url):
    run.hyperlink.address = url

# Slide 1: Cover
s = prs.slides.add_slide(blank); set_bg(s, FOREST)
# abstract concentric/connected marks
for i, (x,y,d,c) in enumerate([(10.1,1.1,1.7,FOREST2),(11.25,2.2,0.9,RUST),(9.45,3.2,0.55,GOLD),(11.0,4.1,1.55,FOREST2),(9.25,5.2,0.35,GOLD)]):
    sh=s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d)); sh.fill.solid(); sh.fill.fore_color.rgb=rgb(c); sh.line.color.rgb=rgb(c)
add_line(s,10.95,1.95,11.65,2.55,'7C8D82',1.1)
add_line(s,10.1,3.75,11.25,2.9,'7C8D82',1.1)
add_line(s,10.05,3.75,11.6,4.65,'7C8D82',1.1)
add_pill(s,0.78,0.75,2.3,'INT396  •  UNSUPERVISED LEARNING',fill=FOREST2,color='E4EAE3',size=8)
add_text(s,0.82,1.45,8.65,2.05,'Safety-Incident Anomaly\nPattern Detection Using\nIsolation Forest and LOF',27,'F5F2E9',True,font=HEAD)
add_text(s,0.86,3.62,7.7,0.54,'From incident reports to reviewable evidence',20,GOLD,True,font=HEAD)
add_text(s,0.86,4.32,7.9,0.75,'An unsupervised study and human-led workflow for spotting unusual incident patterns and comparing historical cases.',13,'D7E0D9')
add_line(s,0.85,5.34,7.95,5.34,'687D70',1)
add_text(s,0.88,5.55,5.6,0.28,'WORKSITE  /  INCIDENT INTELLIGENCE',10,'E8EDE7',True)
add_text(s,0.88,5.92,8.65,0.25,'Dhruv Pal  •  Roll No. RK3P24RDA26  •  Registration ID 12408224',9.2,'D7E0D9')
add_text(s,0.88,6.22,8.65,0.25,'Section K3P24RD  •  Individual  •  LPU  •  SIH26165  •  CO2 / CO4 / CO5',9.2,'D7E0D9')
add_text(s,10.0,6.65,2.5,0.24,'15 NOVEMBER 2026',9,'D7E0D9',True,align=PP_ALIGN.RIGHT)

# Slide 2: Problem
s=prs.slides.add_slide(blank); header(s,2,'Problem','The problem is hidden in the incident record','Severe-injury reports contain both structured classifications and narrative descriptions. Turning that information into useful review evidence takes time.')
card(s,0.72,2.12,3.82,2.0,'Fragmented evidence',[
    ('Structured fields: ','industry, event, source, injury and body part.'),
    ('Narrative fields: ','task context, equipment, conditions and event sequence.'),
],accent=RUST)
card(s,4.77,2.12,3.82,2.0,'Manual review burden',[
    ('Volume: ','large report collections are difficult to compare case by case.'),
    ('Inconsistency: ','similar events may be described with different words and detail.'),
],accent=GOLD)
card(s,8.82,2.12,3.82,2.0,'Decision gap',[
    ('Discovery: ','recurring configurations and unusual reports can be overlooked.'),
    ('Follow-up: ','review findings need evidence, ownership and documentation.'),
],accent=BLUE)
add_shape(s,0.72,4.55,11.92,1.62,fill=FOREST,line=FOREST)
add_text(s,1.0,4.82,2.2,0.35,'PROJECT RESPONSE',9,GOLD,True)
add_text(s,1.0,5.2,10.9,0.7,'Move from a narrative report to a structured review: group similar patterns, flag unusual representations, retrieve historical examples and guide a human investigation.',18,'F7F3E9',True,font=HEAD)
add_text(s,0.76,6.42,11.6,0.3,'The tool supports review of reported severe injuries. It does not predict accidents or represent all workplace hazards.',10,MUTED,italic=True)

# Slide 3: Objectives
s=prs.slides.add_slide(blank); header(s,3,'Objectives','Three objectives, mapped to course outcomes','The implementation follows the submitted INT396 objectives while connecting anomaly analysis to an incident-review workflow.')
objectives=[
 ('01','Prepare the data','Audit the OSHA sample; handle missing values; encode categories; create narrative and date features; reduce and scale.'),
 ('02','Apply IF and LOF','Compare both detectors on the same sample across multiple estimator, neighbourhood and contamination settings.'),
 ('03','Visualise and group','Use PCA to inspect detection patterns and K-Means to describe recurring incident groups.'),
 ('04','Evaluate consistency','Compare flags and scores across settings; inspect held-out injury-outcome descriptors without feature leakage.'),
 ('05','Interpret responsibly','Explain threshold-driven flags, false-positive implications, reporting bias, data limits and human oversight.'),
]
for i,(n,t,b) in enumerate(objectives):
    col=i%2; row=i//2; x=0.75+col*6.1; y=2.05+row*1.28
    if i==4: x=3.8; y=4.61
    add_shape(s,x,y,5.78,1.02,fill=WHITE,line=LINE)
    add_text(s,x+0.18,y+0.18,0.5,0.35,n,15,RUST,True,font=HEAD)
    add_text(s,x+0.78,y+0.13,4.7,0.28,t,14,FOREST,True,font=HEAD)
    add_text(s,x+0.78,y+0.48,4.73,0.44,b,10.2,INK)
add_text(s,0.9,5.82,11.55,0.43,'CO2: preprocessing and unsupervised methods    •    CO4: PCA and visual comparison    •    CO5: evaluation, bias and ethics',9.2,FOREST,True,align=PP_ALIGN.CENTER)

# Slide 4: Data
s=prs.slides.add_slide(blank); header(s,4,'Data','Dataset: OSHA Severe Injury Reports','The supplied local extract spans January 2015 to November 2025. Its jurisdiction and reporting rules define what the model can and cannot represent.')
metrics=[('105,996','records in supplied extract'),('28','columns'),('2015–2025','event-date coverage'),('0','exact duplicate rows')]
for i,(val,lab) in enumerate(metrics):
    x=0.75+i*3.02
    add_shape(s,x,2.05,2.76,1.14,fill=WHITE,line=LINE)
    add_text(s,x+0.18,2.25,2.38,0.4,val,24,FOREST,True,font=HEAD,align=PP_ALIGN.CENTER)
    add_text(s,x+0.16,2.72,2.42,0.22,lab,9,MUTED,True,align=PP_ALIGN.CENTER)
card(s,0.75,3.55,5.78,2.18,'What OSHA reporting covers',[
    'Amputation injuries',
    'Inpatient hospitalisations',
    'Loss of an eye',
    'Federal OSHA jurisdiction reports, beginning 1 January 2015.'
],accent=RUST,body_size=11)
card(s,6.78,3.55,5.78,2.18,'Important coverage limits',[
    'Excludes incidents under OSHA-approved State Plans.',
    'Not a census of all recordable injuries, unsafe acts or near misses.',
    'Reporting and selection bias are possible.',
    'The model bundle excludes names, addresses, IDs and raw narratives.'
],accent=BLUE,body_size=10.4)
add_text(s,0.8,6.15,11.8,0.45,'Audit note: 105,996 unique non-null UPA values; five repeated distinct ID values affected ten rows. The raw CSV is excluded from the deployable ZIP.',9,MUTED,italic=True)

# Slide 5: Research context
s=prs.slides.add_slide(blank); header(s,5,'Research context','What prior work tells us','Text analytics, NLP and clustering have already been applied to occupational safety narratives. The project therefore makes no claim of a new clustering or anomaly-detection algorithm.')
card(s,0.75,2.03,5.75,1.22,'Narrative analytics', 'Safety reports support text classification, extraction, semantic search and topic modelling. Practical usefulness still requires validation.',accent=RUST,body_size=10.7)
card(s,6.78,2.03,5.75,1.22,'Anomaly detection already exists', 'Song and Suh (2019) applied text mining with LOF to accident narratives; Smetana et al. (2024) clustered OSHA severe-injury narratives.',accent=GOLD,body_size=10.7)
add_text(s,0.8,3.43,11.5,0.3,'SELECTED RELATED WORK',9,RUST,True)
refs=[
 ('Ricketts et al. (2023)','Scoping review of NLP applications to safety occurrence reports','10.3390/safety9020022'),
 ('Song & Suh (2019)','Narrative accident-text anomaly detection using LOF','10.1016/j.jlp.2018.08.010'),
 ('Smetana et al. (2024)','Highway construction safety analysis using large language models','10.3390/app14041352'),
 ('Shayboun et al. (2025)','Review of ML for construction accident-report analysis','10.36680/j.itcon.2025.019'),
 ('Macêdo et al. (2023)','Identifying low-quality patterns in accident reports','10.1080/10803548.2022.2111847'),
]
for i,(a,b,d) in enumerate(refs):
    y=3.78+i*0.47
    add_line(s,0.8,y+0.46,12.5,y+0.46,LINE,0.5)
    add_text(s,0.85,y,2.4,0.25,a,10.3,FOREST,True)
    add_text(s,3.18,y,6.55,0.3,b,9.7,INK)
    tx=add_text(s,9.95,y,2.48,0.3,'DOI  '+d,8.6,BLUE,True,align=PP_ALIGN.RIGHT)
    p=tx.text_frame.paragraphs[0]
    if p.runs: add_link(p.runs[0],'https://doi.org/'+d)
add_shape(s,0.78,6.18,11.72,0.48,fill=PALE_GREEN,line=PALE_GREEN)
add_text(s,0.95,6.27,11.4,0.25,'Contribution: reproducible IF/LOF comparison, pattern context, historical retrieval and structured human follow-up. No algorithm novelty claim.',8.8,FOREST,True)

# Slide 6: Workflow
s=prs.slides.add_slide(blank); header(s,6,'Solution','A report becomes a reviewable case','The operational workflow is designed around the person reviewing the incident, not around a graph-first dashboard.')
steps=[
 ('01','CAPTURE','Structured fields\n+ factual narrative'),
 ('02','REPRESENT','One-hot fields\n+ TF-IDF text\n+ 24D SVD'),
 ('03','GROUP','K-Means\npattern group'),
 ('04','SCREEN','Isolation Forest\nunusual pattern'),
 ('05','COMPARE','Five nearest\nhistorical reports'),
 ('06','REVIEW','Checklist, owner,\ndue date and export'),
]
for i,(n,t,b) in enumerate(steps):
    x=0.6+i*2.12
    add_shape(s,x,2.45,1.82,2.18,fill=WHITE,line=LINE)
    add_text(s,x+0.14,2.66,0.48,0.3,n,15,RUST,True,font=HEAD)
    add_text(s,x+0.14,3.1,1.5,0.32,t,10,FOREST,True)
    add_text(s,x+0.14,3.62,1.52,0.72,b,10,INK)
    if i<5:
        add_text(s,x+1.83,3.1,0.29,0.25,'›',22,RUST,True,align=PP_ALIGN.CENTER)
add_shape(s,0.8,5.18,11.75,0.98,fill=FOREST,line=FOREST)
add_text(s,1.08,5.38,2.3,0.25,'OUTPUT',9,GOLD,True)
add_text(s,1.08,5.69,10.9,0.26,'An incident review record with model context and human-entered follow-up. Decisions remain with the qualified reviewer.',12,'F5F2E9',True)
add_text(s,0.82,6.5,11.6,0.2,'No generative-AI text is used. The checklist is rule-based and must be checked against site-specific procedures.',9,MUTED,italic=True)

# Slide 7: Architecture
s=prs.slides.add_slide(blank); header(s,7,'Architecture','Frontend and model services are separated','The user interface calls reusable Python services. The operational model is a standalone serialized artifact required for inference.')
# layered boxes
add_shape(s,0.85,2.1,3.35,3.75,fill=WHITE,line=LINE)
add_pill(s,1.1,2.35,1.3,'FRONTEND',fill=PALE_RUST,color=RUST)
add_text(s,1.1,2.85,2.8,0.45,'Streamlit application',17,FOREST,True,font=HEAD)
add_rich_paragraphs(s,1.1,3.48,2.75,1.85,[
 ('Pages: ','intake, project brief, data, methods, experiments, explorer, governance.'),
 ('Actions: ','validation, screening, review, JSON export.'),
 ('State: ','current session only.')
],10.5,INK,gap=8)
add_text(s,4.38,3.6,0.5,0.35,'→',24,RUST,True,align=PP_ALIGN.CENTER)
add_shape(s,4.95,2.1,3.35,3.75,fill=WHITE,line=LINE)
add_pill(s,5.2,2.35,1.4,'BACKEND',fill=PALE_GREEN,color=FOREST)
add_text(s,5.2,2.85,2.8,0.45,'Python services',17,FOREST,True,font=HEAD)
add_rich_paragraphs(s,5.2,3.48,2.75,1.85,[
 ('Features: ','structured encoding, TF-IDF and TruncatedSVD.'),
 ('Inference: ','K-Means, Isolation Forest and nearest neighbours.'),
 ('Review: ','rule-based prompts and safe JSON serialisation.')
],10.5,INK,gap=8)
add_text(s,8.48,3.6,0.5,0.35,'→',24,RUST,True,align=PP_ALIGN.CENTER)
add_shape(s,9.05,2.1,3.35,3.75,fill=FOREST,line=FOREST)
add_pill(s,9.3,2.35,1.45,'MODEL BUNDLE',fill=FOREST2,color='E9EFE9')
add_text(s,9.3,2.85,2.8,0.45,'Fitted artifact',17,'F5F2E9',True,font=HEAD)
add_rich_paragraphs(s,9.3,3.48,2.75,1.85,[
 ('Reference: ','5,000 sampled OSHA reports.'),
 ('Representation: ','24 dimensions.'),
 ('Contains: ','transformers, detector, clusters and non-identifying comparison fields.')
],10.3,'E7ECE7',gap=8)
add_text(s,0.9,6.25,11.7,0.36,'Raw OSHA CSV is not required to run the deployed application; it is required to rebuild the model and reproduce the complete research pipeline.',9.5,MUTED,italic=True)

# Slide 8: Methods
s=prs.slides.add_slide(blank); header(s,8,'Methodology','A compact representation for mixed incident data','The same fitted feature space is used for grouping, anomaly screening and nearest-neighbour retrieval.')
card(s,0.75,2.05,3.82,1.66,'Preprocessing',[
 'Missing categorical values: Unknown.',
 'One-hot categories + date-cycle features.',
 'TF-IDF unigrams/bigrams, up to 2,500 terms.'
],accent=RUST,body_size=9.8)
card(s,4.77,2.05,3.82,1.66,'Feature space and tests',[
 'TruncatedSVD to 24 components + StandardScaler.',
 'IF: 100/200 trees; 1%/3% contamination.',
 'LOF: k=15/25; 1%/3% contamination.'
],accent=GOLD,body_size=9.6)
card(s,8.79,2.05,3.82,1.66,'Patterns and projections',[
 'K-Means k=8 for descriptive groups.',
 'PCA 3-component exploratory projection.',
 'Five nearest neighbours for historical context.'
],accent=BLUE,body_size=9.8)
add_shape(s,0.78,4.15,11.82,1.52,fill=PALE_RUST,line=PALE_RUST)
add_text(s,1.05,4.42,2.0,0.28,'INTERPRETATION',9,RUST,True)
add_text(s,1.05,4.8,10.95,0.58,'Anomaly percentile = relative position against the fitted reference scores. It is not a probability of injury, a calibrated risk score or proof of a control failure.',15,FOREST,True,font=HEAD)
add_text(s,0.82,6.05,11.6,0.4,'LOF remains part of the experimental comparison. PCA is used for research inspection and visualisation, not as a deployed decision rule.',9.5,MUTED,italic=True)

# Slide 9: clustering metrics
s=prs.slides.add_slide(blank); header(s,9,'Evaluation','K-Means cluster-count evaluation','A deterministic 5,000-record sample was represented in 24 dimensions. Three initialisation seeds were compared for each candidate k.')
# table
rows=[['k','Silhouette¹','Davies–Bouldin','Calinski–Harabasz','Mean pairwise ARI²'],
      ['4','0.0679','2.8638','243.77','0.6777'],
      ['6','0.1062','2.4009','253.01','0.5861'],
      ['8','0.1367','2.2188','277.90','0.5291'],
      ['10','0.1547','2.1740','282.13','0.5027']]
tbl=s.shapes.add_table(len(rows),len(rows[0]), Inches(0.82), Inches(2.1), Inches(11.7), Inches(2.45)).table
widths=[1.0,2.1,2.5,2.5,3.6]
for i,w in enumerate(widths): tbl.columns[i].width= Inches(w)
for ri,row in enumerate(rows):
    for ci,val in enumerate(row):
        cell=tbl.cell(ri,ci); cell.text=val
        cell.margin_left=Inches(0.12); cell.margin_right=Inches(0.08)
        cell.margin_top=Inches(0.06); cell.margin_bottom=Inches(0.04)
        cell.fill.solid(); cell.fill.fore_color.rgb=rgb(FOREST if ri==0 else (PALE_GREEN if row[0]=='8' else WHITE))
        for p in cell.text_frame.paragraphs:
            p.alignment=PP_ALIGN.CENTER if ci==0 else PP_ALIGN.LEFT
            for r in p.runs:
                r.font.name=FONT; r.font.size=Pt(10 if ri else 9.5); r.font.bold=(ri==0 or row[0]=='8'); r.font.color.rgb=rgb('FFFFFF' if ri==0 else INK)
add_shape(s,0.82,4.88,5.55,1.2,fill=PALE_GREEN,line=PALE_GREEN)
add_text(s,1.06,5.08,4.9,0.28,'WHY k = 8?',10,FOREST,True)
add_text(s,1.06,5.45,4.9,0.44,'An exploratory compromise: better separation than k=4/6 without fragmenting as much as k=10.',10,INK)
add_shape(s,6.62,4.88,5.9,1.2,fill=PALE_RUST,line=PALE_RUST)
add_text(s,6.86,5.08,5.2,0.28,'WHAT THE SCORES MEAN',10,RUST,True)
add_text(s,6.86,5.45,5.2,0.44,'Separation is modest; mean ARI 0.5291 indicates sensitivity to initialisation. These are not hazard labels.',10,INK)
add_text(s,0.86,6.42,11.5,0.26,'¹ Silhouette calculated on a 2,000-row evaluation sample. ² Mean pairwise adjusted Rand index across seeds 13, 42 and 77.',8.8,MUTED,italic=True)

# Slide 10: profiles
s=prs.slides.add_slide(blank); header(s,10,'Pattern groups','Examples from the eight exploratory groups','Cluster profiles report frequent fields in each group. They are descriptive summaries, not causal explanations or a ranking of risk.')
profiles=[
 ('GROUP 04  /  250 RECORDS','Caught in running machinery during maintenance or cleaning','Dominant injury: Amputations  •  Body: Fingers'),
 ('GROUP 05  /  330 RECORDS','Caught in running machinery during regular operation','Dominant injury: Amputations  •  Body: Fingers'),
 ('GROUP 08  /  100 RECORDS','Exposure to environmental heat','Dominant source: Heat / environment  •  Injury: Effects of heat and light'),
 ('GROUP 06  /  808 RECORDS','Other fall to lower level, unspecified','Dominant injury: Fractures  •  Body: Hips'),
 ('GROUP 07  /  230 RECORDS','Compressed or pinched by shifting objects or equipment','Dominant source: Powered forklift  •  Injury: Amputations'),
 ('GROUP 01  /  251 RECORDS','Other fall to lower level, less than six feet','Dominant source: Other constructed surface  •  Injury: Fractures'),
]
for i,(tag,title,desc) in enumerate(profiles):
    c=i%2; r=i//2; x=0.78+c*6.03; y=2.0+r*1.32
    add_shape(s,x,y,5.7,1.08,fill=WHITE,line=LINE)
    add_text(s,x+0.2,y+0.12,5.25,0.2,tag,8.3,RUST,True)
    add_text(s,x+0.2,y+0.37,5.25,0.29,title,11.4,FOREST,True,font=HEAD)
    add_text(s,x+0.2,y+0.73,5.25,0.22,desc,8.2,MUTED)
add_text(s,0.82,6.18,11.7,0.48,'These profiles are from the k=8 partition of the fixed sample. Cluster IDs may change under different samples or model settings; group membership must not be interpreted as a causal finding.',9.2,MUTED,italic=True)

# Slide 11: IF/LOF
s=prs.slides.add_slide(blank); header(s,11,'Anomaly experiments','IF and LOF results depend on method and settings','Six configurations were compared on the same deterministic 5,000-record sample. The selected 3% configurations each flag 150 observations, with low overlap.')
# mini result cards
cards=[('IF • 100 TREES • 1%','50 / 5,000','1% flagged'),('IF • 200 TREES • 3%','150 / 5,000','3% flagged'),('LOF • k=15 • 3%','150 / 5,000','3% flagged')]
for i,(tag,val,desc) in enumerate(cards):
    x=0.82+i*4.02
    add_shape(s,x,2.08,3.7,1.16,fill=WHITE,line=LINE)
    add_text(s,x+0.18,2.25,3.3,0.2,tag,8.5,RUST,True)
    add_text(s,x+0.18,2.53,1.9,0.37,val,20,FOREST,True,font=HEAD)
    add_text(s,x+2.0,2.62,1.45,0.23,desc,9,MUTED,True,align=PP_ALIGN.RIGHT)
add_shape(s,0.82,3.65,5.4,1.77,fill=FOREST,line=FOREST)
add_text(s,1.08,3.9,4.85,0.24,'SELECTED IF / LOF AGREEMENT AT 3%',9,GOLD,True)
add_text(s,1.08,4.28,4.85,0.62,'19 of 150 shared flags',20,'F7F3E9',True,font=HEAD)
add_text(s,1.08,4.95,4.85,0.25,'Jaccard 0.068  •  ARI 0.094  •  Spearman 0.139',8.8,'E4EAE4')
card(s,6.55,3.65,5.95,1.77,'Pairwise parameter stability',[
    'Mean within-IF Jaccard: 0.429 across three pairs.',
    'Mean within-LOF Jaccard: 0.426 across three pairs.',
    'Mean cross-method Jaccard: 0.059 across nine pairs.'
],accent=RUST,body_size=9.5)
add_text(s,0.86,6.0,11.5,0.42,'15 pairwise configuration comparisons are saved in the project. Agreement is consistency evidence, not a measure of correctness or accuracy.',9.1,MUTED,italic=True)

# Slide 12: product UX
s=prs.slides.add_slide(blank); header(s,12,'Implementation','A task-focused product, not a graph-first dashboard','The primary screen asks the reviewer to describe an event and then guides them through evidence, comparison and follow-up.')
# faux app wireframe (labeled as layout schematic)
add_shape(s,0.85,2.05,7.65,3.85,fill=WHITE,line=LINE,radius=False)
add_shape(s,0.85,2.05,7.65,0.48,fill=FOREST,line=FOREST,radius=False)
add_text(s,1.1,2.16,3.1,0.2,'WORKSITE  /  INCIDENT REVIEW',9,'F6F2E9',True)
add_text(s,1.1,2.76,6.8,0.35,'New incident review',18,FOREST,True,font=HEAD)
# form rows
for i,(lab,val) in enumerate([('EVENT CATEGORY','Caught in equipment'),('SOURCE / EQUIPMENT','Conveyor transfer point'),('INDUSTRY CODE','Optional NAICS input')]):
    y=3.35+i*0.62
    add_text(s,1.1,y,1.85,0.18,lab,7.5,RUST,True)
    add_shape(s,1.1,y+0.19,6.85,0.34,fill=PAPER,line=LINE,radius=False)
    add_text(s,1.23,y+0.25,6.55,0.18,val,8.8,MUTED)
add_shape(s,1.1,5.3,6.85,0.4,fill=RUST,line=RUST,radius=False)
add_text(s,1.2,5.39,6.65,0.18,'SCREEN INCIDENT AND CREATE REVIEW',8,'FFFFFF',True,align=PP_ALIGN.CENTER)
card(s,8.85,2.05,3.6,1.1,'Pattern group','K-Means group + frequent category descriptors.',accent=GOLD,body_size=9.3)
card(s,8.85,3.32,3.6,1.1,'Historical context','Five nearest reports, with non-identifying fields only.',accent=BLUE,body_size=9.3)
card(s,8.85,4.59,3.6,1.1,'Human follow-up','Checklist, owner role, due date, notes and JSON export.',accent=RUST,body_size=9.3)
add_text(s,0.9,6.2,11.6,0.38,'Layout schematic, not a captured browser screenshot. Verify the actual browser workflow after dependency installation and before submitting.',9,MUTED,italic=True)

# Slide 13: verification and limitations
s=prs.slides.add_slide(blank); header(s,13,'Verification','Implementation checks and held-out outcome proxies','The updated package includes a reproducible 5,000-record run, ten automated tests and an additional descriptive check using outcome fields excluded from model inputs.')
add_shape(s,0.8,2.08,5.55,2.0,fill=PALE_GREEN,line=PALE_GREEN)
add_text(s,1.08,2.35,4.9,0.25,'VERIFIED IN THIS BUILD',9,FOREST,True)
add_text(s,1.08,2.8,1.9,0.55,'10 / 10',28,FOREST,True,font=HEAD)
add_text(s,3.0,2.89,2.6,0.35,'automated tests passed',11,INK,True)
add_text(s,1.08,3.47,4.9,0.36,'Python compilation, model loading and fictional-case inference passed. The held-out outcome check is descriptive only.',9.0,INK)
card(s,6.65,2.08,5.85,2.0,'Held-out outcome proxy check',[
    'IF flags: 3.52% with reported hospitalisation vs 0.75% without.',
    'IF flags: 0.85% with reported amputation vs 3.75% without.',
    'Only one eye-loss record in the sample; not interpretable.',
    'Outcome fields were excluded from features and used post hoc.'
],accent=RUST,body_size=9.2)
add_shape(s,0.82,4.48,11.68,1.37,fill=FOREST,line=FOREST)
add_text(s,1.1,4.72,2.0,0.23,'INTERPRETATION',9,GOLD,True)
add_text(s,1.1,5.1,10.95,0.47,'These outcomes are not anomaly labels. No true false-positive rate or predictive accuracy can be calculated. The 3% contamination setting is a model threshold, not real-world anomaly prevalence.',11,'F7F3E9',True,font=HEAD)
add_text(s,0.85,6.15,11.55,0.33,'No prospective safety-professional trial or browser end-to-end test in this build; case records are session-only. Do not enter personal or confidential data.',8.9,MUTED,italic=True)

# Slide 14: project links
s=prs.slides.add_slide(blank); set_bg(s,FOREST)
add_text(s,0.72,0.45,5.5,0.25,'INT396  /  SIH26165     •     SUBMISSION',9,GOLD,True)
add_text(s,0.72,0.9,7.3,0.7,'Project Links',31,'F5F2E9',True,font=HEAD)
add_text(s,0.75,1.62,10.7,0.36,'Replace the two marked fields with your live URLs after pushing and deploying.',11,'D7E0D9')
# link cards
link_data=[
 ('01','GITHUB REPOSITORY','PASTE YOUR PUBLIC REPOSITORY URL HERE',''),
 ('02','LIVE DEPLOYMENT','PASTE YOUR STREAMLIT APP URL HERE',''),
 ('03','DATASET SOURCE','OSHA Severe Injury Reports','https://www.osha.gov/severeinjury'),
 ('04','PROJECT DOCUMENTATION','README, methodology, model card and validation notes',''),
]
for i,(n,title,desc,url) in enumerate(link_data):
    col=i%2; row=i//2; x=0.78+col*6.03; y=2.28+row*1.52
    add_shape(s,x,y,5.68,1.2,fill=FOREST2,line='496155')
    add_text(s,x+0.18,y+0.16,0.45,0.27,n,12,GOLD,True,font=HEAD)
    add_text(s,x+0.74,y+0.14,4.65,0.25,title,9,'E6ECE7',True)
    t=add_text(s,x+0.74,y+0.5,4.65,0.47,desc,10,'F7F3E9',True)
    if url and t.text_frame.paragraphs[0].runs:
        add_link(t.text_frame.paragraphs[0].runs[0],url)
add_line(s,0.82,5.72,12.48,5.72,'687D70',0.8)
add_text(s,0.85,5.98,11.4,0.4,'PPT submission: 15 November 2026  •  Research paper / patent draft: 24 November 2026',11,'F2F0E9',True)
add_text(s,0.85,6.55,11.2,0.26,'Upload the same final PPT individually through each group member’s UMS account.',9,'D7E0D9')

# Presentation properties
prs.core_properties.title = 'Safety-Incident Anomaly Pattern Detection Using Isolation Forest and LOF'
prs.core_properties.subject = 'INT396 Unsupervised Learning, Individual project, SIH26165, CO2 CO4 CO5'
prs.core_properties.author = 'Dhruv Pal'
prs.core_properties.keywords = 'Workplace safety, OSHA, K-Means, Isolation Forest, LOF, anomaly detection'
prs.core_properties.comments = 'Prepared from the implemented project, course mapping and verified experiment outputs. Project Links slide requires live GitHub and deployment URLs.'

prs.save(OUT)
print(OUT, OUT.stat().st_size)
