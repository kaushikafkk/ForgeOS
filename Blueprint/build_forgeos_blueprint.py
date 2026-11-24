from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(r"C:\Users\kaush\Documents\Codex\ForgeOS\Blueprint")
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "ForgeOS Product and Engineering Blueprint.docx"

BLACK = "000000"
SLATE = "16212B"
SLATE_2 = "22303C"
TEAL = "16A394"
TEAL_PALE = "EAF8F6"
AMBER = "E99A20"
PURPLE = "7756B5"
GRAY = "65717C"
LIGHT = "F4F7F8"
BORDER = "D9D9D9"
WHITE = "FFFFFF"


def set_font(run, name: str = "Aptos", size: float | None = None, bold: bool | None = None,
             color: str | None = None, italic: bool | None = None) -> None:
    run.font.name = name
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color: str = BORDER, size: str = "5") -> None:
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = f"w:{edge}"
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def prevent_row_split(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    cant_split.set(qn("w:val"), "true")
    tr_pr.append(cant_split)


def set_cell_width(cell, inches: float) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.find(qn("w:tcW"))
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(int(inches * 1440)))
    tc_w.set(qn("w:type"), "dxa")


def add_page_number(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Page ")
    set_font(run, size=9, color=GRAY)
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char1)
    run._r.append(instr)
    run._r.append(fld_char2)


def add_hyperlink(paragraph, text: str, url: str, color: str = TEAL) -> None:
    part = paragraph.part
    rel_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), rel_id)
    new_run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    c = OxmlElement("w:color")
    c.set(qn("w:val"), color)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    r_pr.append(c)
    r_pr.append(u)
    new_run.append(r_pr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def add_paragraph(doc: Document, text: str = "", *, bold_lead: str | None = None,
                  style: str | None = None, space_after: float = 6, keep_with_next: bool = False):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.12
    p.paragraph_format.keep_with_next = keep_with_next
    if bold_lead and text.startswith(bold_lead):
        lead = p.add_run(bold_lead)
        set_font(lead, bold=True)
        rest = p.add_run(text[len(bold_lead):])
        set_font(rest)
    elif text:
        run = p.add_run(text)
        set_font(run)
    return p


def add_bullets(doc: Document, items: Iterable[str], level: int = 0) -> None:
    for item in items:
        p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.12
        p.paragraph_format.keep_together = True
        set_font(p.add_run(item))


def add_numbered(doc: Document, items: Iterable[str]) -> None:
    for number, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.12
        p.paragraph_format.keep_together = True
        set_font(p.add_run(f"{number}.  "), bold=True)
        set_font(p.add_run(item))


def add_code(doc: Document, lines: str) -> None:
    for line_number, line in enumerate(lines.strip("\n").splitlines()):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.24)
        p.paragraph_format.right_indent = Inches(0.18)
        if line_number == 0:
            p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        set_font(p.add_run(line), name="Cascadia Mono", size=8.8, color=SLATE)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(2)


def add_table(doc: Document, headers: Sequence[str], rows: Sequence[Sequence[str]],
              widths: Sequence[float] | None = None, font_size: float = 9.0):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    header = table.rows[0]
    set_repeat_table_header(header)
    prevent_row_split(header)
    for i, (cell, text) in enumerate(zip(header.cells, headers)):
        set_cell_shading(cell, SLATE)
        set_cell_margins(cell, 115, 120, 115, 120)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        set_font(p.add_run(text), size=9.0, bold=True, color=WHITE)
        if widths:
            set_cell_width(cell, widths[i])
    for row_idx, row_values in enumerate(rows):
        row = table.add_row()
        prevent_row_split(row)
        for i, (cell, value) in enumerate(zip(row.cells, row_values)):
            set_cell_margins(cell, 105, 120, 105, 120)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if row_idx % 2 == 1:
                set_cell_shading(cell, LIGHT)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            set_font(p.add_run(str(value)), size=font_size, color=BLACK)
            if widths:
                set_cell_width(cell, widths[i])
    after = doc.add_paragraph()
    after.paragraph_format.space_after = Pt(4)
    return table


def add_figure(doc: Document, image: Path, caption: str, width: float = 6.85) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    inline_shape = run.add_picture(str(image), width=Inches(width))
    doc_pr = inline_shape._inline.docPr
    doc_pr.set("descr", caption)
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_after = Pt(9)
    set_font(cp.add_run(caption), size=8.6, italic=True, color=GRAY)


def heading(doc: Document, text: str, level: int = 1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(11 if level == 1 else 9)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    set_font(run, size=17 if level == 1 else 12.5, bold=True, color=BLACK)
    if level > 1:
        gap = p.add_run()
        gap.add_break()
        set_font(gap, size=4)
    return p


def major_section(doc: Document, title: str, intro: str | None = None) -> None:
    if len(doc.paragraphs) > 0:
        doc.add_page_break()
    heading(doc, title, 1)
    if intro:
        add_paragraph(doc, intro, space_after=8)


def configure_document(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.72)
    section.bottom_margin = Inches(0.68)
    section.left_margin = Inches(0.78)
    section.right_margin = Inches(0.78)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.3)

    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(BLACK)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.12

    for style_name, size in (("Title", 28), ("Subtitle", 13), ("Heading 1", 17), ("Heading 2", 12.5), ("Heading 3", 10.8)):
        style = doc.styles[style_name]
        style.font.name = "Aptos Display" if style_name != "Normal" else "Aptos"
        style._element.rPr.rFonts.set(qn("w:ascii"), style.font.name)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), style.font.name)
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(BLACK)
        style.font.bold = style_name != "Subtitle"

    footer = section.footer
    p = footer.paragraphs[0]
    p.clear()
    run = p.add_run("ForgeOS Product and Engineering Blueprint    ")
    set_font(run, size=8.5, color=GRAY)
    add_page_number(p)

    doc.core_properties.title = "ForgeOS Product and Engineering Blueprint"
    doc.core_properties.subject = "Product architecture interface security and delivery plan"
    doc.core_properties.author = "ForgeOS Project"
    doc.core_properties.keywords = "ForgeOS Linux distribution architecture interface security roadmap"


def build_document() -> Document:
    doc = Document()
    configure_document(doc)

    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(14)
    title.paragraph_format.space_after = Pt(6)
    set_font(title.add_run("ForgeOS Product and Engineering Blueprint"), name="Aptos Display", size=28, bold=True, color=BLACK)

    subtitle = doc.add_paragraph(style="Subtitle")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.paragraph_format.space_after = Pt(10)
    set_font(subtitle.add_run("Interface System Architecture Security Delivery and Release Plan"), name="Aptos", size=13, color=BLACK)

    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.paragraph_format.space_after = Pt(12)
    set_font(meta.add_run("Planning baseline 0.1    24 November 2026"), size=9.5, color=GRAY)

    add_figure(doc, ASSETS / "forgeos-desktop.png", "Figure 1  ForgeOS desktop concept with Forge Shell and Forge Hub", width=6.75)

    opening = doc.add_paragraph()
    opening.paragraph_format.space_before = Pt(3)
    opening.paragraph_format.space_after = Pt(0)
    opening.paragraph_format.line_spacing = 1.14
    set_font(opening.add_run(
        "ForgeOS should ship as a Debian based developer distribution with a reproducible build, "
        "rootless project workspaces, recoverable system updates, and equal command line and graphical control. "
        "The first release should concentrate on one x86 64 desktop image that boots, installs, updates, rolls back, "
        "and creates isolated development environments reliably in QEMU and on a small tested hardware set."
    ), size=10.5)

    doc.add_page_break()
    heading(doc, "Contents", 1)
    contents = [
        "Executive Summary",
        "Product Definition",
        "Users and Experience Principles",
        "Interface Architecture",
        "System Architecture",
        "Core Services and Contracts",
        "Base Platform and Build System",
        "Installation and Storage",
        "Updates Rollback and Recovery",
        "Developer Workspaces",
        "Security and Privacy",
        "Operations Diagnostics and Performance",
        "Testing and Quality Assurance",
        "Repository Release Engineering and Governance",
        "Roadmap Risks and Release Gates",
        "Portfolio Demonstration Plan",
        "Appendices and Technical References",
    ]
    for index, item in enumerate(contents, 1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3.5)
        set_font(p.add_run(f"{index:02d}  "), name="Cascadia Mono", size=9.5, bold=True, color=TEAL)
        set_font(p.add_run(item), size=10.5)

    major_section(doc, "Executive Summary")
    add_paragraph(doc,
        "ForgeOS is a portfolio grade Linux distribution for backend and systems developers. Its product value comes from "
        "recoverability, isolated development workspaces, reproducible releases, and a coherent interface that explains system "
        "state without hiding the underlying Linux model. The project will reuse proven upstream components and concentrate custom "
        "engineering on the areas that define the experience.")
    add_paragraph(doc,
        "The baseline uses Debian Stable packages, the upstream Linux kernel, systemd, KDE Plasma on Wayland, NetworkManager, "
        "PipeWire, Flatpak, Podman, Btrfs, and LUKS2. ForgeOS adds signed build configuration, the forge command line interface, "
        "a per user workspace agent, a privileged system service, the Forge Hub graphical control surface, update orchestration, "
        "snapshot management, diagnostics, installer configuration, and automated virtual machine testing.")
    add_paragraph(doc,
        "Version 0.1 will use package based updates protected by Btrfs snapshots. A later image based release may move to A and B "
        "system partitions with dm verity integrity checking and systemd sysupdate. This sequence produces a usable first release "
        "without blocking on a more complex immutable image pipeline.")

    heading(doc, "Baseline Decisions", 2)
    add_table(doc,
        ["Area", "Decision", "Reason"],
        [
            ["Distribution base", "Debian Stable", "Stable repository and official live image tooling"],
            ["Desktop", "KDE Plasma on Wayland", "Mature accessibility and configurable shell components"],
            ["System filesystem", "Btrfs inside optional LUKS2", "Subvolumes and rollback friendly snapshots"],
            ["Workspaces", "Rootless Podman", "User namespaces and daemonless container lifecycle"],
            ["Custom services", "Go services with D Bus and Polkit", "Clear privilege boundary and strong concurrency support"],
            ["Updates", "APT transaction plus pre update snapshot", "Practical first release with an upgrade path to image updates"],
            ["Target", "UEFI x86 64", "Small support surface for the first public release"],
        ],
        widths=[1.28, 2.25, 3.35], font_size=8.9)

    heading(doc, "Release Outcome", 2)
    add_bullets(doc, [
        "A signed hybrid ISO that boots in UEFI QEMU and on the documented reference hardware.",
        "A live desktop and guided installer with optional disk encryption and a recovery partition.",
        "A working forge CLI and Forge Hub that create, inspect, stop, export, and remove project workspaces.",
        "An update workflow that creates a snapshot, applies packages, verifies health, and offers rollback.",
        "Automated tests that install, boot, exercise core services, inject failures, and publish release evidence.",
        "Public documentation covering architecture, threat model, support matrix, known limitations, and contributor workflow.",
    ])

    major_section(doc, "Product Definition")
    heading(doc, "Product Purpose", 2)
    add_paragraph(doc,
        "ForgeOS is a local first development workstation. It reduces the time needed to prepare reproducible project environments "
        "and reduces the cost of recovering from a bad package update or configuration change. It remains a normal Linux system: "
        "administrators can inspect units, logs, filesystems, containers, package metadata, and policy decisions with standard tools.")

    heading(doc, "Product Promise", 2)
    add_paragraph(doc,
        "A user can install ForgeOS, create an isolated backend workspace, develop and test a service, update the operating system, "
        "and return to a known working system state without rebuilding the machine. Every high impact graphical action has a documented "
        "forge command and every privileged action passes through an explicit authorization boundary.")

    heading(doc, "Version One Scope", 2)
    add_bullets(doc, [
        "One x86 64 UEFI desktop image with a live session and graphical installation path.",
        "English language interface with architecture prepared for localization.",
        "KDE Plasma session with the Pulse Bar, Orbit Dock, Flow Deck, Forge Hub, and Forge Recovery experience.",
        "Rootless Podman workspaces for Go, Rust, Node, Python, Java, PostgreSQL, Redis, and generic Compose projects.",
        "Btrfs snapshots for system rollback and separate guidance for real backups.",
        "Stable, beta, and development release channels backed by signed metadata.",
        "QEMU based continuous integration plus a documented reference hardware test set.",
    ])

    heading(doc, "Explicit Non Goals", 2)
    add_bullets(doc, [
        "A new kernel, init system, package manager, container runtime, or desktop compositor.",
        "A distribution package repository that rebuilds the entire Debian archive.",
        "Legacy BIOS, ARM, server, mobile, gaming, and enterprise fleet support in version 0.1.",
        "Guaranteed compatibility with every proprietary GPU or vendor firmware combination.",
        "Automatic collection of usage telemetry, project files, command history, or workspace contents.",
        "Snapshots presented as backups. A snapshot shares storage with its source and does not protect against disk loss.",
    ])

    heading(doc, "Success Measures", 2)
    add_table(doc,
        ["Measure", "Version One Target", "Evidence"],
        [
            ["Clean installation", "At least 95 percent across 20 repeated QEMU runs", "CI installation history"],
            ["Cold boot", "Under 25 seconds on reference NVMe hardware", "Boot chart and journal timestamps"],
            ["Idle memory", "Under 1.8 GiB after settling", "Repeatable system metrics"],
            ["Workspace creation", "Under 30 seconds from warm image cache", "CLI benchmark suite"],
            ["Rollback", "Restore working system within 5 minutes", "Power failure and bad update scenarios"],
            ["Accessibility", "Keyboard complete core flows at 200 percent scale", "Manual and automated review"],
            ["Reproducibility", "Two controlled builders produce matching manifests", "Build comparison report"],
        ], widths=[1.35, 2.5, 3.03], font_size=8.8)

    major_section(doc, "Users and Experience Principles")
    heading(doc, "Primary Users", 2)
    add_table(doc,
        ["User", "Main Need", "ForgeOS Response"],
        [
            ["Backend developer", "Repeatable databases queues and services", "Versioned workspace templates with rootless containers"],
            ["Systems learner", "Understand how the system works", "Visible logs commands and architecture documentation"],
            ["Open source contributor", "Switch between project toolchains", "Independent workspaces and per project resources"],
            ["Maintainer", "Build test sign and recover releases", "Reproducible ISO pipeline and recovery evidence"],
        ], widths=[1.35, 2.35, 3.18], font_size=8.9)

    heading(doc, "Experience Principles", 2)
    add_bullets(doc, [
        "Recoverability is visible. Update and configuration screens show the snapshot that protects the operation.",
        "The interface explains Linux state. It names services, filesystems, containers, logs, and packages rather than inventing vague labels.",
        "Graphical and command line paths stay equivalent. The GUI displays the corresponding forge command for repeatable operations.",
        "Privilege is requested at the last responsible moment. Browsing status never requires authentication.",
        "The system works offline after required packages and images have been downloaded.",
        "Color reinforces meaning but never carries meaning alone. Icons, labels, and status text remain present.",
        "Destructive actions describe affected data, preserve user files by default, and require specific confirmation.",
    ])

    heading(doc, "Core User Journeys", 2)
    add_numbered(doc, [
        "Install ForgeOS from the live image, choose encryption, create an account, review storage changes, and boot the installed system.",
        "Open Flow Deck, create a backend workspace, enter the shell, run services, inspect ports, and switch between Code Test and Ship modes.",
        "Receive an update, inspect its size and restart requirements, create a snapshot, apply the update, and review the health result.",
        "Recover from a failed update by selecting a verified snapshot, reading the restore plan, and restarting into the restored system.",
        "Export a diagnostics bundle, preview every included file, redact optional data, and share it only through an explicit user action.",
    ])

    major_section(doc, "Interface Architecture")
    add_paragraph(doc,
        "The shell uses a stable spatial model. System context stays at the top, applications remain on the left, focused work occupies "
        "the center, and system control opens from the right. This reduces movement between unrelated surfaces and keeps the development "
        "workspace visible while the user checks health, snapshots, or updates.")

    add_figure(doc, ASSETS / "forgeos-desktop.png", "Figure 2  Main desktop with Forge Shell and the Forge Hub control surface")

    heading(doc, "Desktop Components", 2)
    add_table(doc,
        ["Component", "Purpose", "Primary Interaction"],
        [
            ["Pulse Bar", "Shows active workspace and essential system status", "Click status groups or use Super Space"],
            ["Orbit Dock", "Provides stable access to frequent tools", "Click icon or use Super plus number"],
            ["Flow Deck", "Searches apps files commands and workspaces", "Press Super or Ctrl K"],
            ["Forge Hub", "Controls health updates snapshots and workspaces", "Open from Pulse Bar or forge hub"],
            ["Forge Shell", "Presents workspace aware terminal context", "Open from workspace card or forge enter"],
            ["Forge Recovery", "Verifies and restores system state", "Open from settings or recovery boot entry"],
            ["Notification Stream", "Reports completed and actionable operations", "Open with Super N"],
        ], widths=[1.35, 3.1, 2.43], font_size=8.8)

    heading(doc, "Flow Deck", 2)
    add_paragraph(doc,
        "Flow Deck is the main switcher and command surface. Results are grouped by apps, files, commands, settings, and workspaces. "
        "Privileged commands display a shield and plain language explanation. Search remains local unless the user enables an online provider.")
    add_figure(doc, ASSETS / "forgeos-flow-deck.png", "Figure 3  Flow Deck workspace overview and command surface")

    heading(doc, "Workspace Modes", 2)
    add_table(doc,
        ["Mode", "Behavior", "Guardrails"],
        [
            ["Code", "Starts development services and exposes configured local ports", "Secrets stay in the keyring and resource caps remain active"],
            ["Test", "Creates a clean ephemeral test layer and enables detailed logs", "Test data is isolated and discarded unless exported"],
            ["Ship", "Locks dependency versions and runs release checks", "Requires a clean repository and blocks unsigned output by default"],
        ], widths=[0.9, 3.3, 2.68], font_size=8.9)

    heading(doc, "Visual System", 2)
    add_table(doc,
        ["Token", "Value", "Use"],
        [
            ["Graphite", "0B0F14", "Desktop and application background"],
            ["Slate", "151C24", "Primary surfaces"],
            ["Teal", "2DD4BF", "Healthy active and successful state"],
            ["Amber", "F5A524", "Update attention and reversible risk"],
            ["Purple", "7756B5", "Snapshots recovery and historical state"],
            ["Corner radius", "14 px", "Application panels and cards"],
            ["Spacing unit", "4 px", "All layout increments"],
            ["UI type", "Aptos or Noto Sans", "Interface labels and prose"],
            ["Code type", "Cascadia Mono or JetBrains Mono", "Commands logs and paths"],
        ], widths=[1.25, 1.5, 4.13], font_size=8.9)

    heading(doc, "Interaction Standards", 2)
    add_bullets(doc, [
        "Every action responds within 100 milliseconds with focus, progress, or an explicit queued state.",
        "Operations longer than two seconds show current phase, completed work, and a safe cancellation rule.",
        "Error messages identify the failed component, preserve the original log identifier, and give one next action.",
        "The Escape key closes transient surfaces. It never silently cancels a disk or update transaction.",
        "Confirmation text states what changes, what is preserved, whether restart is required, and how to recover.",
        "The interface remembers layout per workspace but stores settings in documented user configuration files.",
    ])

    heading(doc, "Accessibility", 2)
    add_bullets(doc, [
        "Complete keyboard access with visible focus and no pointer only operation.",
        "Screen reader names for every icon control status and progress indicator.",
        "Usable layouts at 125 150 and 200 percent scaling on common laptop resolutions.",
        "Reduced motion mode that removes wallpaper movement and uses opacity rather than spatial animation.",
        "Minimum body text contrast of 4.5 to 1 and large text contrast of 3 to 1.",
        "Status shown with text and icon in addition to color.",
        "Installer and recovery flows tested without audio and without fine motor assumptions.",
    ])

    major_section(doc, "System Architecture")
    add_paragraph(doc,
        "ForgeOS separates ordinary user operations from privileged system changes. The desktop, CLI, and workspace agent operate without "
        "root privileges. A small system service accepts a versioned set of privileged operations over D Bus and applies Polkit policy. "
        "Direct arbitrary command execution is not part of the service contract.")

    heading(doc, "Platform Layers", 2)
    add_table(doc,
        ["Layer", "Selected Components", "ForgeOS Responsibility"],
        [
            ["Firmware and boot", "UEFI shim GRUB initramfs", "Signed configuration recovery entry and boot health"],
            ["Kernel and devices", "Upstream Debian kernel udev fwupd", "Supported configuration and hardware evidence"],
            ["System services", "systemd NetworkManager PipeWire", "Units policies health checks and diagnostics"],
            ["Storage", "LUKS2 Btrfs zram", "Subvolume layout snapshots and restore orchestration"],
            ["Application layer", "APT Flatpak Podman", "Curated defaults permissions and workspace templates"],
            ["Forge control", "forged forge agent forge CLI", "Stable APIs authorization and state model"],
            ["Desktop", "KDE Plasma Forge Hub Flow Deck", "User experience and GUI CLI parity"],
            ["Delivery", "live build CI signed repository", "Reproducible images tests manifests and releases"],
        ], widths=[1.18, 2.55, 3.15], font_size=8.7)

    heading(doc, "Boot Lifecycle", 2)
    add_numbered(doc, [
        "UEFI validates the configured boot path and starts the bootloader.",
        "The bootloader selects the normal system, a previous snapshot, or the recovery environment.",
        "The initramfs unlocks the LUKS2 container, mounts Btrfs subvolumes, and validates required root state.",
        "systemd starts foundational services and records a boot attempt identifier.",
        "The display manager starts the Wayland session after storage and network prerequisites reach their defined state.",
        "forge agent starts inside the user session, reconciles workspaces, and publishes non sensitive state to Forge Hub.",
        "The boot health service marks the boot successful after the desktop, storage, and update checks pass.",
    ])

    heading(doc, "Control and Data Planes", 2)
    add_table(doc,
        ["Plane", "Contains", "Rule"],
        [
            ["System control", "Updates snapshots boot repair package and storage operations", "Only forged performs privileged mutations"],
            ["User control", "Workspace lifecycle settings notifications and local search", "Runs as the signed in user"],
            ["Project data", "Source code volumes databases caches and artifacts", "Never enters system telemetry by default"],
            ["Release data", "Manifests checksums package metadata and signatures", "Must be authenticated before use"],
            ["Diagnostic data", "Selected logs hardware summary and service state", "Preview and explicit export required"],
        ], widths=[1.22, 2.75, 2.91], font_size=8.8)

    heading(doc, "Trust Boundaries", 2)
    add_bullets(doc, [
        "The graphical shell and forge CLI are unprivileged clients. Compromise of either must not grant unrestricted root execution.",
        "Workspace containers are untrusted project execution. Rootless namespaces and resource controls limit their reach.",
        "Package mirrors and container registries are untrusted transport. Signatures digests and policy decide acceptance.",
        "The installer is trusted with storage changes and therefore uses a separate process with explicit review and confirmation.",
        "Recovery operations are trusted but must state whether user data system data or both will change.",
    ])

    major_section(doc, "Core Services and Contracts")
    heading(doc, "Service Inventory", 2)
    add_table(doc,
        ["Component", "Privilege", "Responsibility", "Failure Behavior"],
        [
            ["forge", "User", "CLI and scriptable entry point", "Returns stable exit codes and structured JSON"],
            ["forge agent", "User", "Workspace lifecycle and local state", "Reconciles state after restart"],
            ["forged", "Root", "Approved system mutations", "Rejects unknown operations and logs authorization"],
            ["Forge Hub", "User", "Graphical system and workspace control", "Remains useful in read only degraded mode"],
            ["forge update", "Root unit", "Update download stage apply and verify", "Keeps previous snapshot bootable"],
            ["forge snapshot", "Root unit", "Snapshot create prune verify restore", "Never deletes last known good snapshot"],
            ["forge diagnostics", "Split", "Local health and export bundle", "Exports nothing without confirmation"],
            ["forge firstboot", "Root then user", "Machine identity account defaults and initial state", "Resumable and idempotent"],
        ], widths=[1.05, 0.75, 2.72, 2.36], font_size=8.3)

    heading(doc, "Privileged API Rules", 2)
    add_bullets(doc, [
        "Expose named operations such as CreateSnapshot ApplyUpdate RestoreSnapshot and RepairBoot rather than a shell command API.",
        "Version requests and responses from the first release and reject unsupported versions explicitly.",
        "Validate paths device identifiers channel names and snapshot identifiers against service owned state.",
        "Use Polkit actions with separate rules for read status stage update apply update restore and repair.",
        "Return an operation identifier immediately and publish progress events with phase percentage and recoverability state.",
        "Make mutating requests idempotent through operation keys so UI retries cannot duplicate work.",
        "Write an audit event containing the caller action target result and journal correlation identifier.",
    ])

    heading(doc, "State Model", 2)
    add_code(doc, """
Operation
  id              globally unique identifier
  kind            update snapshot restore repair install
  state           queued running waiting completed failed cancelled
  phase           component specific stable phase name
  progress        optional percentage and completed units
  recoverability  safe to cancel restart required rollback available
  started_at      monotonic and wall clock timestamps
  result          typed result or typed error
""")

    heading(doc, "Configuration Locations", 2)
    add_table(doc,
        ["Path", "Owner", "Purpose"],
        [
            ["/etc/forgeos", "Root", "Machine policy channels and system defaults"],
            ["/var/lib/forgeos", "Root", "Update snapshot and operation state"],
            ["/var/log/journal", "systemd journal", "Structured system logs"],
            ["~/.config/forgeos", "User", "Interface preferences and workspace defaults"],
            ["~/.local/share/forgeos", "User", "Workspace metadata and cached indexes"],
            ["~/Forge", "User", "Default source and project directory"],
        ], widths=[2.1, 1.3, 3.48], font_size=8.9)

    major_section(doc, "Base Platform and Build System")
    heading(doc, "Base Selection", 2)
    add_paragraph(doc,
        "Debian Stable is the version 0.1 base. ForgeOS consumes Debian packages without rebuilding the complete archive and publishes only "
        "the small set of custom packages it owns. Debian live build produces the live filesystem, kernel, initramfs, bootloader, installer "
        "payload, checksums, and hybrid ISO from repository configuration.")

    heading(doc, "Platform Components", 2)
    add_table(doc,
        ["Capability", "Component", "Policy"],
        [
            ["Kernel", "Debian supported upstream kernel", "No custom fork in version 0.1"],
            ["Init and services", "systemd", "Harden custom units and use timers for maintenance"],
            ["Desktop", "KDE Plasma Wayland", "Minimal overrides packaged separately"],
            ["Networking", "NetworkManager and nftables", "Firewall on with explicit workspace port exposure"],
            ["Audio and video", "PipeWire", "Use portal mediated application access"],
            ["System packages", "APT and dpkg", "Signed ForgeOS repository layered on Debian"],
            ["Desktop applications", "Flatpak", "Curated remotes and visible permissions"],
            ["Workspaces", "Podman rootless", "No root daemon and no privileged default containers"],
            ["Firmware", "fwupd where supported", "Separate firmware operation and restart messaging"],
        ], widths=[1.4, 2.35, 3.13], font_size=8.7)

    heading(doc, "Build Inputs", 2)
    add_bullets(doc, [
        "Pinned Debian suite architecture mirrors and package lists.",
        "ForgeOS package source and deterministic package build instructions.",
        "Filesystem overlays for branding defaults policies and service units.",
        "Installer configuration and partition recipes.",
        "Bootloader theme recovery entry and kernel command line policy.",
        "Signed release metadata channel metadata checksums SBOM and provenance.",
        "Test scenarios that boot the exact image produced by the build job.",
    ])

    heading(doc, "Build Pipeline", 2)
    add_numbered(doc, [
        "Validate configuration schema package lists and license metadata.",
        "Build custom Debian packages in an isolated builder and generate source packages.",
        "Create a temporary signed repository containing the custom packages.",
        "Run live build with the pinned configuration and clean package cache.",
        "Generate ISO disk image package manifest SBOM and cryptographic checksums.",
        "Boot the ISO in QEMU and run smoke installation workspace update and recovery tests.",
        "Sign release artifacts only after required tests complete.",
        "Publish artifacts release notes known limitations and support matrix together.",
    ])

    heading(doc, "Package Strategy", 2)
    add_paragraph(doc,
        "ForgeOS will not create a new package manager. Custom software is delivered as Debian packages with declared dependencies, service "
        "units, migration scripts, and uninstall behavior. Desktop styling remains separate from core services so users can replace the shell "
        "without breaking update or recovery functions. Configuration migrations must be idempotent and reversible when the data model permits.")

    major_section(doc, "Installation and Storage")
    add_paragraph(doc,
        "The installer offers a safe guided path and an advanced manual path. The guided path requires a complete review before writing the "
        "partition table. Device identity uses model serial capacity and stable device path rather than a short name such as sda alone.")
    add_figure(doc, ASSETS / "forgeos-installer.png", "Figure 4  Guided storage and encryption step in the ForgeOS installer")

    heading(doc, "Guided Installation Flow", 2)
    add_numbered(doc, [
        "Choose language region keyboard accessibility preferences and network.",
        "Select the target disk and choose erase disk use free space or manual partitioning.",
        "Choose encryption and enter a passphrase that is confirmed locally and never logged.",
        "Create the user account and optionally enable automatic login for an unencrypted test machine only.",
        "Review the exact disk device partition changes data loss restart behavior and recovery layout.",
        "Apply partitioning install packages write boot entries and verify the installed system before offering restart.",
    ])

    heading(doc, "Recommended Disk Layout", 2)
    add_table(doc,
        ["Element", "Format", "Typical Size", "Purpose"],
        [
            ["EFI system partition", "FAT32", "1 GiB", "UEFI boot files and signed loader"],
            ["Encrypted system container", "LUKS2", "Remaining disk less recovery", "System user data swap and snapshots"],
            ["System filesystem", "Btrfs", "Inside LUKS2", "Subvolumes packages workspaces and snapshots"],
            ["Recovery partition", "Read only image", "8 GiB", "Offline repair reinstall and restore tools"],
            ["Memory swap", "zram", "Dynamic", "Compressed memory pressure relief"],
            ["Hibernate swap", "Optional file", "Hardware dependent", "Enabled only when validated for encryption and resume"],
        ], widths=[1.55, 1.25, 1.25, 2.83], font_size=8.6)

    heading(doc, "Btrfs Subvolumes", 2)
    add_table(doc,
        ["Subvolume", "Mount", "Snapshot Rule"],
        [
            ["@root", "/", "Included in system snapshots"],
            ["@home", "/home", "Excluded from system rollback by default"],
            ["@var", "/var", "Selective persistent directories separated where needed"],
            ["@log", "/var/log", "Persists across rollback for diagnostics"],
            ["@containers", "/var/lib/containers and user container storage", "Managed independently to avoid large system snapshots"],
            ["@snapshots", "/.snapshots", "Read only snapshots with retention policy"],
        ], widths=[1.35, 2.3, 3.23], font_size=8.8)

    heading(doc, "Storage Safety Rules", 2)
    add_bullets(doc, [
        "The installer never writes until the final review screen names the selected disk and changes.",
        "Manual partitioning validates an EFI partition a supported root filesystem and sufficient recovery space.",
        "System rollback does not roll back user home by default. The restore plan states every affected subvolume.",
        "A snapshot is not described as a backup because it shares the same storage device and extents.",
        "The recovery environment can export user files before repair or reinstall.",
        "Low disk space blocks snapshot creating updates before the transaction begins.",
    ])

    major_section(doc, "Updates Rollback and Recovery")
    add_paragraph(doc,
        "The update system treats download, staging, snapshot creation, package application, restart, boot verification, and cleanup as separate "
        "phases. The previous known good snapshot remains available until the new system passes health checks and the retention policy permits pruning.")

    heading(doc, "Version One Update Transaction", 2)
    add_numbered(doc, [
        "Refresh signed channel metadata and calculate package disk and restart impact.",
        "Download packages without modifying the running system and verify signatures and hashes.",
        "Check free space power state inhibited services and workspace activity.",
        "Create a read only pre update snapshot and register a temporary boot entry.",
        "Apply packages with a transaction identifier and capture structured output.",
        "Run post update checks for package consistency services storage and boot files.",
        "Restart when required and mark the boot successful only after health checks pass.",
        "Retain the previous snapshot through the defined safety period and prune older snapshots by policy.",
    ])

    add_figure(doc, ASSETS / "forgeos-recovery.png", "Figure 5  Forge Recovery snapshot verification and restore plan")

    heading(doc, "Recovery Capabilities", 2)
    add_table(doc,
        ["Capability", "Normal Desktop", "Recovery Environment"],
        [
            ["Inspect snapshots", "Yes", "Yes"],
            ["Verify snapshot metadata", "Yes", "Yes"],
            ["Restore system snapshot", "Schedules restart", "Direct offline restore"],
            ["Repair bootloader", "Status only", "Yes"],
            ["Check filesystem", "Read only checks", "Offline repair where supported"],
            ["Export user files", "Yes", "Yes"],
            ["Reinstall system", "Launches recovery", "Yes with preservation options"],
            ["Export diagnostics", "Yes", "Yes"],
        ], widths=[2.5, 1.85, 2.53], font_size=8.8)

    heading(doc, "Future Image Based Updates", 2)
    add_paragraph(doc,
        "Version 0.2 may introduce A and B read only system images. systemd sysupdate can stage the inactive image, and dm verity can verify "
        "blocks on demand through a signed root hash. A boot attempt counter would return to the previous slot if the new image does not reach "
        "the healthy state. This design requires signed manifests, partition planning, migration policy, and careful separation of persistent data.")

    heading(doc, "Snapshot Retention", 2)
    add_bullets(doc, [
        "Always retain the last known good boot and the snapshot immediately before the latest update.",
        "Keep daily snapshots for seven days and weekly snapshots for four weeks when disk capacity permits.",
        "Never prune a snapshot referenced by an active boot entry or incomplete operation.",
        "Calculate exclusive referenced space before presenting reclaimed space estimates.",
        "Offer export to separate storage for backup but label exported snapshots and backups accurately.",
    ])

    major_section(doc, "Developer Workspaces")
    add_paragraph(doc,
        "A workspace is a versioned project environment described by a manifest. The source directory remains owned by the user. Runtime services "
        "run through rootless Podman with dedicated networks volumes secrets and resource limits. Workspace state can be recreated from its manifest "
        "and lock file without requiring the original containers.")

    heading(doc, "Workspace Manifest", 2)
    add_code(doc, """
apiVersion: forgeos.dev/v1
kind: Workspace
metadata:
  name: payments
spec:
  stack: go-postgres
  mode: code
  services:
    api:
      source: .
      ports: [8080]
      resources: { cpu: 2, memory: 2GiB }
    database:
      image: postgres:16
      volume: payments-db
  secrets: [database-url]
  healthchecks: [api, database]
""")

    heading(doc, "Workspace Lifecycle", 2)
    add_table(doc,
        ["State", "Meaning", "Allowed Actions"],
        [
            ["Defined", "Manifest is valid but runtime does not exist", "Create validate delete manifest"],
            ["Provisioning", "Images volumes and networks are being prepared", "Inspect logs cancel if safe"],
            ["Stopped", "Runtime exists with no running services", "Start export clone remove"],
            ["Running", "Required services are healthy", "Enter logs test ship stop"],
            ["Degraded", "One or more required health checks failed", "Inspect restart repair export"],
            ["Testing", "Ephemeral clean test layer is active", "View progress logs cancel"],
            ["Shipping", "Release checks and artifact build are active", "View evidence cancel before signing"],
        ], widths=[1.18, 3.0, 2.7], font_size=8.7)

    heading(doc, "Isolation Model", 2)
    add_bullets(doc, [
        "Run containers as the signed in user with user namespaces and subordinate UID and GID ranges.",
        "Create a separate network per workspace and publish only ports declared in the manifest.",
        "Mount source directories with the minimum required permissions and prefer read only mounts for test fixtures.",
        "Store named secrets in the desktop keyring and inject them at runtime without writing them into manifests or logs.",
        "Apply CPU memory process and disk limits through cgroups where supported.",
        "Block privileged containers host PID host devices and unrestricted host networking unless an advanced policy explicitly allows them.",
        "Record image digests in the lock file so rebuilds use the intended artifacts.",
    ])

    heading(doc, "Template System", 2)
    add_table(doc,
        ["Template", "Services", "First Release Goal"],
        [
            ["go-postgres", "Go API PostgreSQL migration runner", "Reference backend workflow"],
            ["node-redis", "Node service Redis test runner", "JavaScript service workflow"],
            ["python-worker", "Python worker queue PostgreSQL", "Background processing workflow"],
            ["rust-service", "Rust API PostgreSQL", "Systems backend workflow"],
            ["java-postgres", "Java service PostgreSQL", "Enterprise backend workflow"],
            ["compose-import", "Existing Compose file", "Compatibility path with validation"],
        ], widths=[1.5, 3.0, 2.38], font_size=8.8)

    heading(doc, "Command Surface", 2)
    add_code(doc, """
forge create payments --stack go-postgres
forge start payments
forge enter payments
forge mode payments test
forge mode payments ship
forge status payments --json
forge logs payments api --follow
forge ports payments
forge export payments --output payments.forgebundle
forge stop payments
forge remove payments --keep-data
""")

    major_section(doc, "Security and Privacy")
    heading(doc, "Security Objectives", 2)
    add_bullets(doc, [
        "Prevent unsigned or unexpected release content from becoming trusted system state.",
        "Limit compromise of a desktop application workspace or user account from becoming unrestricted root access.",
        "Protect user data at rest when encryption is selected and avoid leaking secrets through logs or diagnostics.",
        "Keep a recoverable known good system state after interrupted or malicious updates.",
        "Make every privileged change attributable to a local caller and operation identifier.",
    ])

    heading(doc, "Threat Model", 2)
    add_table(doc,
        ["Threat", "Asset", "Primary Mitigation", "Residual Risk"],
        [
            ["Malicious update mirror", "System integrity", "Signed metadata packages hashes and channel policy", "Signing key compromise"],
            ["Compromised workspace", "Host and user data", "Rootless containers namespaces limited mounts and resources", "Kernel vulnerability"],
            ["Stolen laptop", "User data", "Optional default guided LUKS2 encryption", "Weak passphrase or unlocked session"],
            ["Privileged API abuse", "Root control", "Typed operations input validation Polkit and audit", "Service implementation flaw"],
            ["Diagnostic data leak", "Project and personal data", "Local generation preview redaction and explicit export", "User chooses unsafe contents"],
            ["Interrupted update", "Bootability", "Pre update snapshot boot entry and health verification", "Disk failure during write"],
            ["Installer error", "Existing disk data", "Stable device identity review and destructive confirmation", "Incorrect user selection"],
        ], widths=[1.3, 1.25, 2.9, 1.43], font_size=8.15)

    heading(doc, "Privilege and Authorization", 2)
    add_bullets(doc, [
        "forged runs with the minimum Linux capabilities required for each operation and uses systemd hardening directives.",
        "Polkit actions separate staging applying restoring repairing and changing channel operations.",
        "Read only status is available without authentication unless it exposes sensitive data.",
        "Authorization dialogs name the operation and target. They never request a password before the user initiates a privileged action.",
        "The service rejects caller supplied executable paths shell fragments environment overrides and arbitrary unit names.",
    ])

    heading(doc, "Boot and Supply Chain", 2)
    add_bullets(doc, [
        "Use signed boot components and document Secure Boot status. Production key management is a later release requirement.",
        "Generate an SBOM for the ISO and custom packages and publish it beside the release.",
        "Build custom packages from reviewed source commits in isolated workers.",
        "Pin container images by digest in release templates and show image origin in Forge Hub.",
        "Keep signing keys outside the ordinary build job and require protected release approval.",
        "Publish checksums signatures source packages and reproducible build instructions.",
    ])

    heading(doc, "Privacy", 2)
    add_bullets(doc, [
        "No usage telemetry or cloud account is required for installation and daily operation.",
        "Crash reporting is off by default. Enabling it shows the destination fields retention and disable path.",
        "Local search indexes paths and metadata only within configured locations and can be disabled or rebuilt.",
        "Diagnostics exclude home files source content secrets environment values shell history and container data by default.",
        "The user previews and edits a diagnostics manifest before an archive is created or transmitted.",
        "Update requests reveal only the information required to select the correct architecture channel and version.",
    ])

    major_section(doc, "Operations Diagnostics and Performance")
    heading(doc, "Observability Model", 2)
    add_paragraph(doc,
        "ForgeOS uses the systemd journal as the primary structured log store and emits stable message identifiers for custom services. Operation "
        "records link GUI progress CLI output journal entries and diagnostics. Metrics remain local unless the user configures an exporter.")

    add_table(doc,
        ["Signal", "Examples", "Retention"],
        [
            ["System logs", "Unit start failure update phase authorization result", "Size capped journal with persistent error history"],
            ["Operation records", "Snapshot update restore install", "Retained with related snapshots and release evidence"],
            ["Health state", "Storage boot workspace update", "Current state plus recent transitions"],
            ["Performance metrics", "Boot time memory disk pressure workspace startup", "Local rolling history configurable by user"],
            ["Diagnostic bundle", "Selected logs manifests hardware and versions", "Created on demand and user managed"],
        ], widths=[1.35, 3.3, 2.23], font_size=8.8)

    heading(doc, "Diagnostic Workflow", 2)
    add_numbered(doc, [
        "Select the failing area and reproduce or select an existing operation identifier.",
        "Collect a local draft containing the minimum relevant service and system records.",
        "Scan for configured secret patterns usernames home paths network identifiers and environment values.",
        "Show a file by file manifest with inclusion reason size and redaction status.",
        "Let the user remove entries or open text entries before archive creation.",
        "Create the archive locally and leave sharing to a separate explicit action.",
    ])

    heading(doc, "Performance Budgets", 2)
    add_table(doc,
        ["Area", "Budget", "Measurement"],
        [
            ["Desktop cold boot", "Less than 25 seconds on reference NVMe hardware", "Firmware excluded journal and boot chart"],
            ["Desktop idle memory", "Less than 1.8 GiB", "Five minute settled median"],
            ["Flow Deck open", "Visible in less than 150 milliseconds", "Input to first frame"],
            ["Forge Hub status", "Fresh state in less than 500 milliseconds", "Local service response"],
            ["Warm workspace create", "Less than 30 seconds", "Images already cached"],
            ["Workspace start", "Less than 10 seconds for reference stack", "Start to healthy"],
            ["Snapshot creation", "Less than 5 seconds in normal case", "Metadata operation only"],
            ["Recovery open", "Less than 8 seconds from desktop", "Launch to usable interface"],
        ], widths=[1.45, 3.2, 2.23], font_size=8.7)

    heading(doc, "Hardware Support", 2)
    add_table(doc,
        ["Class", "Version One Position", "Evidence Required"],
        [
            ["UEFI x86 64 laptops", "Primary target", "Install suspend audio network and display tests"],
            ["Intel and AMD integrated graphics", "Primary graphics target", "Wayland session and multi monitor tests"],
            ["NVIDIA graphics", "Best effort documented path", "Open and proprietary driver matrix"],
            ["Wi Fi and Bluetooth", "Supported through Debian firmware policy", "Reference adapter results"],
            ["High DPI displays", "Required", "125 150 and 200 percent scaling review"],
            ["Legacy BIOS", "Not supported in version 0.1", "No release blocker"],
            ["ARM64", "Future investigation", "Separate boot and driver plan"],
        ], widths=[1.7, 2.6, 2.58], font_size=8.8)

    major_section(doc, "Testing and Quality Assurance")
    heading(doc, "Test Layers", 2)
    add_table(doc,
        ["Layer", "Scope", "Release Role"],
        [
            ["Unit", "Parsers state transitions policy and manifest validation", "Every change"],
            ["Component", "D Bus contracts workspace engine snapshot and update helpers", "Every change"],
            ["Integration", "Service interactions package install and permissions", "Every change"],
            ["QEMU boot", "Live boot installed boot recovery and rollback", "Every release candidate"],
            ["Installer", "Guided encryption manual partition and interrupted install", "Every release candidate"],
            ["Fault injection", "Power loss disk full corrupt metadata failed service and network loss", "Nightly and release"],
            ["Interface", "Keyboard scaling contrast localization and screen reader labels", "Milestone and release"],
            ["Hardware", "Reference laptops docks monitors graphics and suspend", "Release candidate"],
            ["Security", "Static analysis dependency audit service sandbox and threat cases", "Every release"],
        ], widths=[1.22, 3.65, 2.01], font_size=8.5)

    heading(doc, "Critical Scenarios", 2)
    add_bullets(doc, [
        "Power loss while packages are being applied leaves the previous snapshot bootable.",
        "Disk full before and during staging fails safely without deleting the last known good state.",
        "Repeated update and snapshot requests with the same operation key do not duplicate work.",
        "A failed user service does not prevent Forge Recovery from opening.",
        "A compromised workspace cannot access another workspace secret or privileged system socket.",
        "Installer selection remains bound to the same physical disk after device enumeration changes.",
        "Rollback preserves home data and clearly reports any excluded persistent directories.",
        "A diagnostics export contains no default shell history source file or secret environment value.",
    ])

    heading(doc, "Continuous Integration", 2)
    add_table(doc,
        ["Trigger", "Jobs", "Artifact"],
        [
            ["Pull request", "Lint unit component package build interface schema", "Test report and packages"],
            ["Main branch", "Clean ISO build QEMU smoke and manifest comparison", "Development ISO"],
            ["Nightly", "Install update rollback fault injection and security scans", "Nightly evidence bundle"],
            ["Release candidate", "Full QEMU matrix accessibility and reference hardware", "Signed candidate artifacts"],
            ["Release", "Independent verification signing and publication", "ISO checksums SBOM source and notes"],
        ], widths=[1.4, 3.6, 1.88], font_size=8.8)

    heading(doc, "Quality Gates", 2)
    add_bullets(doc, [
        "No unresolved critical or high severity security issue in a custom ForgeOS component.",
        "No data loss issue in installer update rollback or workspace volume tests.",
        "All required QEMU installation boot update and recovery scenarios pass from a clean environment.",
        "The known limitations document matches the actual hardware and feature support matrix.",
        "Every release artifact has a checksum signature manifest SBOM source reference and build identifier.",
        "Keyboard only completion succeeds for installation workspace creation update and recovery.",
    ])

    major_section(doc, "Repository Release Engineering and Governance")
    heading(doc, "Repository Structure", 2)
    add_code(doc, """
forgeos/
  build/                 live build orchestration and image metadata
  config/                package lists hooks overlays and policies
  packages/              source for ForgeOS Debian packages
  cmd/forge/             command line client
  services/forged/       privileged system service
  services/forge-agent/  per user workspace service
  desktop/               Forge Hub Flow Deck themes and integration
  installer/             installer modules and storage recipes
  recovery/              recovery image and tools
  templates/             versioned workspace templates
  tests/unit/            fast component tests
  tests/qemu/            boot install update and recovery automation
  docs/                  architecture threat model support and decisions
  release/               channel metadata signing and publication tooling
""")

    heading(doc, "Branch and Change Policy", 2)
    add_bullets(doc, [
        "The main branch remains releasable and protected by required tests and review.",
        "Feature branches are short lived. Large architectural work begins with a design record.",
        "Changes to installer storage update signing or privilege contracts require security and recovery review.",
        "Generated artifacts are not committed unless they are required test fixtures. Releases publish immutable artifacts separately.",
        "Every custom package owns a changelog migration notes license data and maintainer entry.",
    ])

    heading(doc, "Versioning and Channels", 2)
    add_table(doc,
        ["Channel", "Audience", "Update Policy"],
        [
            ["Stable", "Daily users and portfolio reviewers", "Signed tested releases with conservative package movement"],
            ["Beta", "Testers and contributors", "Release candidates with explicit rollback and issue reporting"],
            ["Development", "Maintainers", "Frequent builds no stability promise and separate signing policy"],
        ], widths=[1.1, 2.55, 3.23], font_size=8.9)

    heading(doc, "Release Contents", 2)
    add_bullets(doc, [
        "Hybrid installation ISO and optional raw disk image.",
        "SHA 256 checksums and detached signatures.",
        "Package manifest source commit build identifier and reproducibility notes.",
        "SPDX or CycloneDX software bill of materials.",
        "Release notes upgrade notes known limitations and support matrix.",
        "Architecture threat model and recovery documentation for the released design.",
    ])

    heading(doc, "Project Roles", 2)
    add_table(doc,
        ["Role", "Accountability"],
        [
            ["Product and UX owner", "Scope interface behavior documentation and release narrative"],
            ["Platform maintainer", "Base packages image build boot and hardware support"],
            ["Services maintainer", "forge CLI agents D Bus contracts updates and diagnostics"],
            ["Security reviewer", "Threat model privilege supply chain installer and release signing"],
            ["Quality owner", "Test matrix evidence accessibility and release gates"],
            ["Release manager", "Version channel notes artifacts signatures and rollback plan"],
        ], widths=[2.0, 4.88], font_size=8.9)

    major_section(doc, "Roadmap Risks and Release Gates")
    heading(doc, "Sixteen Week Plan", 2)
    add_table(doc,
        ["Weeks", "Milestone", "Exit Condition"],
        [
            ["1 to 2", "Foundation", "Repository decisions package builder and console ISO boot in UEFI QEMU"],
            ["3 to 4", "Live Desktop", "KDE Wayland session networking audio branding Flow Deck shell prototype"],
            ["5 to 7", "Workspace Core", "forge CLI agent rootless Podman manifests templates and health"],
            ["8 to 9", "System Control", "forged Polkit Forge Hub operations diagnostics and audit"],
            ["10 to 11", "Installer", "Guided encrypted installation installed boot and first boot flow"],
            ["12 to 13", "Update and Recovery", "Snapshot protected update rollback recovery boot and repair"],
            ["14 to 15", "Quality", "Fault injection accessibility security and reference hardware evidence"],
            ["16", "Release", "Signed 0.1 artifacts documentation screenshots demo and public release"],
        ], widths=[0.95, 1.75, 4.18], font_size=8.7)

    heading(doc, "Risk Register", 2)
    add_table(doc,
        ["Risk", "Impact", "Mitigation", "Trigger"],
        [
            ["Scope expansion", "Release never stabilizes", "Freeze version one non goals and require design records", "New subsystem enters critical path"],
            ["Installer data loss", "Severe user harm", "QEMU destructive tests stable device identity and review screen", "Any ambiguous disk selection"],
            ["Snapshot confusion", "False backup confidence", "Separate backup language and preserve home by default", "UI calls snapshot a backup"],
            ["Desktop customization fragility", "Upstream updates break shell", "Package small modular extensions and test upstream updates", "Private patch count grows"],
            ["NVIDIA incompatibility", "Poor hardware experience", "Best effort path and explicit matrix", "Unverified driver update"],
            ["Signing key exposure", "Supply chain compromise", "Offline or protected signing release approval and rotation plan", "Key appears in build environment"],
            ["Root service vulnerability", "Privilege escalation", "Typed API fuzzing sandboxing and narrow capabilities", "Arbitrary execution path added"],
            ["Small test pool", "Hardware defects escape", "Publish support matrix and recruit testers after beta", "Unsupported issue volume rises"],
        ], widths=[1.25, 1.35, 3.1, 1.18], font_size=7.9)

    heading(doc, "Release Gates", 2)
    add_table(doc,
        ["Gate", "Required Evidence"],
        [
            ["Architecture", "Approved decisions for privilege storage update workspace and diagnostics boundaries"],
            ["Boot", "Live installed normal snapshot and recovery entries boot successfully"],
            ["Data safety", "Installer rollback disk full and power interruption scenarios pass"],
            ["Security", "Threat model updated custom services hardened release artifacts signed"],
            ["Accessibility", "Core journeys complete with keyboard and required scaling"],
            ["Performance", "Published targets measured on documented reference hardware"],
            ["Documentation", "Install recovery support known limitations and contributor guides complete"],
            ["Portfolio", "Five minute demonstration can be reproduced from released artifacts"],
        ], widths=[1.45, 5.43], font_size=8.9)

    heading(doc, "Post Release Direction", 2)
    add_bullets(doc, [
        "Version 0.2 image based A and B updates with dm verity and systemd sysupdate.",
        "Version 0.3 ARM64 image and expanded hardware lab if the x86 64 architecture remains stable.",
        "Shared template registry with signed manifests and reproducible template tests.",
        "Optional remote workspace targets after the local workspace security model is mature.",
        "Localization infrastructure and community translation workflow.",
    ])

    major_section(doc, "Portfolio Demonstration Plan")
    heading(doc, "Five Minute Demonstration", 2)
    add_numbered(doc, [
        "Boot the released ISO in QEMU and show the live desktop build identifier.",
        "Open Flow Deck and create the payments Go and PostgreSQL workspace.",
        "Enter Forge Shell start the services and show health ports logs and resource controls.",
        "Switch to Test mode and demonstrate the clean ephemeral test layer.",
        "Stage a simulated update and show the automatically created pre update snapshot.",
        "Inject a failed health check and restore the previous snapshot through Forge Recovery.",
        "Open the public repository and show CI evidence package manifests architecture and threat model.",
    ])

    heading(doc, "Resume Evidence", 2)
    add_bullets(doc, [
        "Reproducible Linux image generation and automated UEFI virtual machine testing.",
        "A privilege separated Go service architecture using D Bus Polkit systemd and typed operations.",
        "Rootless container workspace orchestration with manifests health checks resources and secrets.",
        "Snapshot protected updates recovery boot and tested rollback under injected failures.",
        "A documented threat model signed release pipeline SBOM and measurable release gates.",
        "A coherent accessible interface backed by equivalent command line operations.",
    ])

    heading(doc, "Recommended Repository Evidence", 2)
    add_table(doc,
        ["Evidence", "Why It Matters"],
        [
            ["Architecture decision records", "Shows tradeoffs and disciplined system design"],
            ["Threat model", "Shows security boundaries before implementation"],
            ["QEMU test recordings", "Proves boot installation update and rollback behavior"],
            ["Performance dashboard", "Shows measured rather than claimed system targets"],
            ["Release manifest and SBOM", "Shows professional supply chain practice"],
            ["Failure injection results", "Shows correctness under realistic system faults"],
            ["Interface reference pack", "Connects product intent with implemented screens"],
        ], widths=[2.35, 4.53], font_size=8.9)

    major_section(doc, "Appendices and Technical References")
    heading(doc, "Screen Inventory", 2)
    add_table(doc,
        ["Surface", "Version One State", "Key Screens"],
        [
            ["Desktop shell", "Required", "Pulse Bar Orbit Dock notifications session power"],
            ["Flow Deck", "Required", "Search workspace overview recent work command preview"],
            ["Forge Hub", "Required", "Overview workspaces updates snapshots diagnostics settings"],
            ["Forge Shell", "Required", "Workspace shell status logs ports environment"],
            ["Installer", "Required", "Welcome keyboard storage account review progress complete"],
            ["Recovery", "Required", "Snapshots updates boot repair diagnostics reinstall"],
            ["First boot", "Required", "Welcome privacy workspace defaults release channel tour"],
            ["Settings", "Required", "Appearance accessibility privacy updates containers hardware"],
        ], widths=[1.35, 1.35, 4.18], font_size=8.7)

    heading(doc, "Error Taxonomy", 2)
    add_table(doc,
        ["Class", "Meaning", "Interface Response"],
        [
            ["Validation", "User input or manifest cannot be accepted", "Keep input show exact field and correction"],
            ["Authorization", "Caller lacks permission or cancels authentication", "Preserve operation and explain required action"],
            ["Transient", "Network mirror or service may recover", "Offer bounded retry and preserve progress"],
            ["Resource", "Disk memory process or power requirement is not met", "Block safely and show required capacity"],
            ["Integrity", "Signature hash filesystem or state verification failed", "Stop mutation protect known good state and open recovery"],
            ["Unsupported", "Hardware configuration or schema is outside support", "Name limitation and safe alternative"],
            ["Internal", "Unexpected ForgeOS component failure", "Show operation identifier and diagnostics path"],
        ], widths=[1.25, 2.85, 2.78], font_size=8.7)

    heading(doc, "Technical References", 2)
    refs = [
        ("Debian Live Manual", "https://live-team.pages.debian.net/live-manual/html/live-manual.en.html", "Live image build boot and persistence concepts"),
        ("Debian live build manual", "https://manpages.debian.org/trixie/live-build/live-build.7.en.html", "Build stages and configuration commands"),
        ("Linux From Scratch 13.1", "https://linuxfromscratch.org/lfs/downloads/stable-systemd/LFS-BOOK-13.1-NOCHUNKS.html", "Learning reference for Linux system composition"),
        ("systemd sysupdate", "https://www.freedesktop.org/software/systemd/man/latest/systemd-sysupdate.service.html", "Future image update mechanism"),
        ("Podman documentation", "https://docs.podman.io/en/stable/markdown/podman.1.html", "Rootless container model"),
        ("Btrfs subvolume documentation", "https://btrfs.readthedocs.io/en/latest/btrfs-subvolume.html", "Subvolumes snapshots and limitations"),
        ("Linux dm verity documentation", "https://www.kernel.org/doc/html/latest/admin-guide/device-mapper/verity.html", "Future read only image integrity"),
    ]
    for title_text, url, note in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        add_hyperlink(p, title_text, url)
        set_font(p.add_run(f"  {note}"), size=9.3, color=GRAY)

    heading(doc, "Decision Record Backlog", 2)
    add_bullets(doc, [
        "ADR 001 Debian Stable as the first distribution base.",
        "ADR 002 KDE Plasma Wayland shell and extension boundary.",
        "ADR 003 Btrfs subvolume and snapshot layout.",
        "ADR 004 D Bus and Polkit privileged operation model.",
        "ADR 005 Rootless Podman workspace architecture.",
        "ADR 006 Package based update transaction and rollback.",
        "ADR 007 Installer encryption and recovery partition design.",
        "ADR 008 Release signing key custody and rotation.",
        "ADR 009 Diagnostics data model and privacy defaults.",
        "ADR 010 Criteria for moving to A and B image updates.",
    ])

    heading(doc, "Immediate Next Actions", 2)
    add_numbered(doc, [
        "Create the ForgeOS repository with the documented top level directories and contribution rules.",
        "Write ADR 001 through ADR 005 before implementing privileged or storage components.",
        "Set up a Linux build virtual machine and produce the smallest UEFI Debian live image.",
        "Add a QEMU smoke test that waits for a known systemd target and collects the journal.",
        "Prototype the forge manifest parser and workspace state machine without a graphical dependency.",
        "Implement a read only forged status API before adding any privileged mutation.",
        "Turn the four interface references in this blueprint into clickable prototypes and accessibility flows.",
        "Publish milestone zero with build instructions boot evidence and the first architecture decisions.",
    ])

    return doc


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    document = build_document()
    document.save(OUTPUT)
    print(OUTPUT)

