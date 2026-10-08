import os
import zipfile

def build_pptx(filename, slide_data):
    """
    Pure Python OpenXML PPTX Presentation Generator.
    Builds a high-impact, modern dark-theme PowerPoint presentation with:
    - Custom slide dimensions (16:9 Widescreen: 9144000 x 5143500)
    - Card shape containers, accent color banners, and 2-column content layouts
    - Embedded Presenter Speaker Notes XML for presenter mode
    """
    num_slides = len(slide_data)
    
    # 1. Content Types
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
"""
    for i in range(1, num_slides + 1):
        content_types += f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
        content_types += f'  <Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>\n'
    content_types += '</Types>'

    # 2. Main Rels
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""

    # 3. Presentation Rels
    pres_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
"""
    for i in range(1, num_slides + 1):
        pres_rels += f'  <Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
    pres_rels += '</Relationships>'

    # 4. Presentation XML
    pres_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
"""
    for i in range(1, num_slides + 1):
        pres_xml += f'    <p:sldId id="{255 + i}" r:id="rId{i+1}"/>\n'
    pres_xml += """  </p:sldIdLst>
  <p:sldSz cx="9144000" cy="5143500"/>
  <p:notesSz cx="5143500" cy="9144000"/>
</p:presentation>"""

    # 5. Master XML
    master_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rId1"/>
  </p:sldLayoutIdLst>
</p:sldMaster>"""

    master_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""

    # 6. Layout XML
    layout_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
</p:sldLayout>"""

    layout_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""

    # Pack ZIP
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('ppt/_rels/presentation.xml.rels', pres_rels)
        z.writestr('ppt/presentation.xml', pres_xml)
        z.writestr('ppt/slideMasters/slideMaster1.xml', master_xml)
        z.writestr('ppt/slideMasters/_rels/slideMaster1.xml.rels', master_rels)
        z.writestr('ppt/slideLayouts/slideLayout1.xml', layout_xml)
        z.writestr('ppt/slideLayouts/_rels/slideLayout1.xml.rels', layout_rels)

        # Generate individual slide XMLs & Notes
        for idx, slide in enumerate(slide_data, start=1):
            slide_xml = generate_rich_slide_xml(idx, num_slides, slide)
            z.writestr(f'ppt/slides/slide{idx}.xml', slide_xml)
            
            slide_rel = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{idx}.xml"/>
</Relationships>"""
            z.writestr(f'ppt/slides/_rels/slide{idx}.xml.rels', slide_rel)

            # Generate speaker notes XML
            notes_xml = generate_notes_xml(slide.get('script', ''))
            z.writestr(f'ppt/notesSlides/notesSlide{idx}.xml', notes_xml)
            
            notes_rel = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide{idx}.xml"/>
</Relationships>"""
            z.writestr(f'ppt/notesSlides/_rels/notesSlide{idx}.xml.rels', notes_rel)

    print(f"Generated High-Impact PPTX Presentation: {filename} ({os.path.getsize(filename)} bytes, {num_slides} slides with Speaker Scripts)")

def generate_rich_slide_xml(slide_num, total_slides, slide):
    title = xml_escape(slide.get('title', ''))
    subtitle = xml_escape(slide.get('subtitle', ''))
    left_points = slide.get('left_points', slide.get('points', []))
    right_points = slide.get('right_points', [])
    badge = xml_escape(slide.get('badge', f"SLIDE {slide_num} / {total_slides}"))

    # Left Column XML
    left_xml = ""
    for p in left_points:
        safe_p = xml_escape(p)
        left_xml += f"""
        <a:p>
          <a:pPr spaceBefore="100" spaceAfter="100"/>
          <a:r>
            <a:rPr lang="en-US" sz="1500" b="1">
              <a:solidFill><a:srgbClr val="10B981"/></a:solidFill>
            </a:rPr>
            <a:t>• </a:t>
          </a:r>
          <a:r>
            <a:rPr lang="en-US" sz="1500">
              <a:solidFill><a:srgbClr val="F3F4F6"/></a:solidFill>
            </a:rPr>
            <a:t>{safe_p}</a:t>
          </a:r>
        </a:p>"""

    # Right Column XML (if 2-column slide)
    right_xml = ""
    if right_points:
        for p in right_points:
            safe_p = xml_escape(p)
            right_xml += f"""
            <a:p>
              <a:pPr spaceBefore="100" spaceAfter="100"/>
              <a:r>
                <a:rPr lang="en-US" sz="1500" b="1">
                  <a:solidFill><a:srgbClr val="06B6D4"/></a:solidFill>
                </a:rPr>
                <a:t>✓ </a:t>
              </a:r>
              <a:r>
                <a:rPr lang="en-US" sz="1500">
                  <a:solidFill><a:srgbClr val="F3F4F6"/></a:solidFill>
                </a:rPr>
                <a:t>{safe_p}</a:t>
              </a:r>
            </a:p>"""

    col_width = 3800000 if right_points else 7800000
    right_col_sp = ""
    if right_points:
        right_col_sp = f"""
      <!-- Right Card Container -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="5" name="Card Right"/><p:cSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="4700000" y="1400000"/><a:ext cx="3900000" cy="3400000"/></a:xfrm>
          <a:prstGeom prst="roundRect"><a:avLst><a:gd name="a" val="12000"/></a:avLst></a:prstGeom>
          <a:solidFill><a:srgbClr val="161B26"/></a:solidFill>
          <a:ln w="12700"><a:solidFill><a:srgbClr val="06B6D4"/></a:solidFill></a:ln>
        </p:spPr>
      </p:sp>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="6" name="Right Text"/><p:cSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="4800000" y="1500000"/><a:ext cx="3700000" cy="3200000"/></a:xfrm></p:spPr>
        <p:txBody><a:bodyPr/><a:lstStyle/>{right_xml}</p:txBody>
      </p:sp>"""

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgPr>
        <a:solidFill><a:srgbClr val="0D1117"/></a:solidFill>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      
      <!-- Header Banner Shape -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="10" name="Header Banner"/><p:cSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="500000" y="300000"/><a:ext cx="8144000" cy="850000"/></a:ext>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="161B26"/></a:solidFill>
          <a:ln w="9525"><a:solidFill><a:srgbClr val="10B981"/></a:solidFill></a:ln>
        </p:spPr>
      </p:sp>
      
      <!-- Slide Title & Subtitle -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Title 1"/><p:cSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="650000" y="360000"/><a:ext cx="6500000" cy="750000"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="2400" b="1">
                <a:solidFill><a:srgbClr val="10B981"/></a:solidFill>
              </a:rPr>
              <a:t>{title}</a:t>
            </a:r>
          </a:p>
          {'<a:p><a:r><a:rPr lang="en-US" sz="1100"><a:solidFill><a:srgbClr val="9CA3AF"/></a:solidFill></a:rPr><a:t>' + subtitle + '</a:t></a:r></a:p>' if subtitle else ''}
        </p:txBody>
      </p:sp>
      
      <!-- Badge Pill Shape -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="11" name="Badge"/><p:cSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="7200000" y="450000"/><a:ext cx="1300000" cy="350000"/></a:xfrm>
          <a:prstGeom prst="roundRect"><a:avLst><a:gd name="a" val="25000"/></a:avLst></a:prstGeom>
          <a:solidFill><a:srgbClr val="06B6D4"/></a:solidFill>
        </p:spPr>
        <p:txBody>
          <a:bodyPr lIns="0" rIns="0" tIns="0" bIns="0" anchor="ctr"/>
          <a:lstStyle/>
          <a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="1000" b="1"><a:solidFill><a:srgbClr val="000000"/></a:solidFill></a:rPr><a:t>{badge}</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>
      
      <!-- Left Card Container -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="Card Left"/><p:cSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="500000" y="1400000"/><a:ext cx="{3900000 if right_points else 8144000}" cy="3400000"/></a:xfrm>
          <a:prstGeom prst="roundRect"><a:avLst><a:gd name="a" val="12000"/></a:avLst></a:prstGeom>
          <a:solidFill><a:srgbClr val="161B26"/></a:solidFill>
          <a:ln w="12700"><a:solidFill><a:srgbClr val="10B981"/></a:solidFill></a:ln>
        </p:spPr>
      </p:sp>

      <!-- Left Text -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="4" name="Left Text"/><p:cSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="600000" y="1500000"/><a:ext cx="{3700000 if right_points else 7944000}" cy="3200000"/></a:xfrm></p:spPr>
        <p:txBody><a:bodyPr/><a:lstStyle/>{left_xml}</p:txBody>
      </p:sp>
      
      {right_col_sp}
    </p:spTree>
  </p:cSld>
</p:sld>"""

def generate_notes_xml(script_text):
    safe_script = xml_escape(script_text)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Notes Text"/><p:cSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="685800" y="1143000"/><a:ext cx="3771900" cy="6858000"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1200" b="1">
                <a:solidFill><a:srgbClr val="000000"/></a:solidFill>
              </a:rPr>
              <a:t>SPEAKER SCRIPT: {safe_script}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:notes>"""

def xml_escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;').replace('₹', 'INR ')
