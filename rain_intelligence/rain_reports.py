"""
Professional client-facing PDF generator for RAIN Intelligence.

The generated PDF exists only in memory.
It is not saved to Google Sheets or permanent application storage.
"""

import datetime
import io
import os
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


RAIN_NAVY = "#17324D"
RAIN_GOLD = "#C4A24D"
RAIN_TEXT = "#222222"
RAIN_MUTED = "#555555"
RAIN_LIGHT = "#F7F5EF"
RAIN_BORDER = "#D9D9D9"


def _register_rain_fonts():
    """
    Register Unicode-compatible fonts when available.
    """

    regular_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]

    bold_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]

    regular_path = next(
        (
            path
            for path in regular_candidates
            if os.path.exists(path)
        ),
        None,
    )

    bold_path = next(
        (
            path
            for path in bold_candidates
            if os.path.exists(path)
        ),
        None,
    )

    if regular_path and bold_path:
        try:
            pdfmetrics.registerFont(
                TTFont(
                    "RainRegular",
                    regular_path,
                )
            )

            pdfmetrics.registerFont(
                TTFont(
                    "RainBold",
                    bold_path,
                )
            )

            return "RainRegular", "RainBold"

        except Exception:
            pass

    return "Helvetica", "Helvetica-Bold"


def _clean_text(value):
    """
    Prepare ordinary text for ReportLab Paragraph.
    """

    if value is None:
        return ""

    return escape(str(value).strip()).replace(
        "\n",
        "<br/>",
    )


def _safe_list(value):
    """
    Ensure a value is returned as a clean list.
    """

    if not value:
        return []

    if isinstance(value, list):
        return [
            item
            for item in value
            if str(item).strip()
        ]

    return [value]


def _page_header_footer(pdf_canvas, document):
    """
    Add branded headers, footers, and page numbers.

    The cover page remains clean.
    """

    pdf_canvas.saveState()

    page_width, page_height = letter
    page_number = pdf_canvas.getPageNumber()

    regular_font = getattr(
        document,
        "rain_regular_font",
        "Helvetica",
    )

    bold_font = getattr(
        document,
        "rain_bold_font",
        "Helvetica-Bold",
    )

    if page_number > 1:
        pdf_canvas.setStrokeColor(
            colors.HexColor(RAIN_GOLD)
        )

        pdf_canvas.setLineWidth(0.8)

        pdf_canvas.line(
            0.72 * inch,
            page_height - 0.62 * inch,
            page_width - 0.72 * inch,
            page_height - 0.62 * inch,
        )

        pdf_canvas.setFillColor(
            colors.HexColor(RAIN_NAVY)
        )

        pdf_canvas.setFont(
            bold_font,
            8.5,
        )

        pdf_canvas.drawString(
            0.72 * inch,
            page_height - 0.47 * inch,
            "RAIN INTELLIGENCE",
        )

        pdf_canvas.setFont(
            regular_font,
            8,
        )

        pdf_canvas.drawRightString(
            page_width - 0.72 * inch,
            page_height - 0.47 * inch,
            "STRATEGIC GAME PLAN",
        )

        pdf_canvas.setStrokeColor(
            colors.HexColor(RAIN_BORDER)
        )

        pdf_canvas.setLineWidth(0.5)

        pdf_canvas.line(
            0.72 * inch,
            0.58 * inch,
            page_width - 0.72 * inch,
            0.58 * inch,
        )

        pdf_canvas.setFillColor(
            colors.HexColor(RAIN_MUTED)
        )

        pdf_canvas.setFont(
            regular_font,
            7.5,
        )

        pdf_canvas.drawString(
            0.72 * inch,
            0.38 * inch,
            "Find Your Way Network Marketing Consultants",
        )

        pdf_canvas.drawRightString(
            page_width - 0.72 * inch,
            0.38 * inch,
            f"Page {page_number}",
        )

    pdf_canvas.restoreState()


def build_rain_game_plan_pdf(
    game_plan,
    consultation_date=None,
):
    """
    Build the polished client-facing RAIN Strategic Game Plan.

    Returns an in-memory BytesIO PDF buffer.
    """

    if not isinstance(game_plan, dict):
        raise ValueError(
            "The RAIN game plan must be a dictionary."
        )

    pdf_buffer = io.BytesIO()

    regular_font, bold_font = _register_rain_fonts()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        rightMargin=0.72 * inch,
        leftMargin=0.72 * inch,
        topMargin=0.82 * inch,
        bottomMargin=0.78 * inch,
        title=game_plan.get(
            "report_title",
            "RAIN Strategic Game Plan",
        ),
        author=(
            "RAIN Intelligence and Find Your Way "
            "Network Marketing Consultants"
        ),
        subject="Client Strategic Game Plan",
        pageCompression=1,
    )

    document.rain_regular_font = regular_font
    document.rain_bold_font = bold_font

    styles = getSampleStyleSheet()

    cover_brand = ParagraphStyle(
        name="RainCoverBrand",
        parent=styles["Normal"],
        fontName=bold_font,
        fontSize=13,
        leading=17,
        alignment=TA_CENTER,
        textColor=colors.HexColor(RAIN_GOLD),
        spaceAfter=18,
    )

    cover_title = ParagraphStyle(
        name="RainCoverTitle",
        parent=styles["Title"],
        fontName=bold_font,
        fontSize=25,
        leading=31,
        alignment=TA_CENTER,
        textColor=colors.HexColor(RAIN_NAVY),
        spaceAfter=14,
    )

    cover_subtitle = ParagraphStyle(
        name="RainCoverSubtitle",
        parent=styles["Normal"],
        fontName=regular_font,
        fontSize=13,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor(RAIN_MUTED),
        spaceAfter=28,
    )

    cover_details = ParagraphStyle(
        name="RainCoverDetails",
        parent=styles["Normal"],
        fontName=regular_font,
        fontSize=10.5,
        leading=17,
        alignment=TA_CENTER,
        textColor=colors.HexColor(RAIN_MUTED),
    )

    report_title = ParagraphStyle(
        name="RainReportTitle",
        parent=styles["Title"],
        fontName=bold_font,
        fontSize=20,
        leading=26,
        alignment=TA_LEFT,
        textColor=colors.HexColor(RAIN_NAVY),
        spaceAfter=16,
    )

    section_heading = ParagraphStyle(
        name="RainSectionHeading",
        parent=styles["Heading1"],
        fontName=bold_font,
        fontSize=15,
        leading=20,
        textColor=colors.HexColor(RAIN_NAVY),
        spaceBefore=15,
        spaceAfter=9,
        keepWithNext=True,
    )

    body = ParagraphStyle(
        name="RainBody",
        parent=styles["BodyText"],
        fontName=regular_font,
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor(RAIN_TEXT),
        alignment=TA_LEFT,
        spaceAfter=9,
        allowWidows=0,
        allowOrphans=0,
    )

    bullet = ParagraphStyle(
        name="RainBullet",
        parent=body,
        leftIndent=18,
        firstLineIndent=-9,
        bulletIndent=6,
        spaceBefore=1,
        spaceAfter=5,
    )

    priority = ParagraphStyle(
        name="RainPriority",
        parent=body,
        leftIndent=12,
        rightIndent=12,
        borderColor=colors.HexColor(RAIN_GOLD),
        borderWidth=0.8,
        borderPadding=9,
        backColor=colors.HexColor(RAIN_LIGHT),
        spaceBefore=5,
        spaceAfter=10,
    )

    step_heading = ParagraphStyle(
        name="RainStepHeading",
        parent=body,
        fontName=bold_font,
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor(RAIN_NAVY),
        spaceBefore=8,
        spaceAfter=6,
        keepWithNext=True,
    )

    small_text = ParagraphStyle(
        name="RainSmallText",
        parent=body,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor(RAIN_MUTED),
    )

    story = []

    # =====================================================
    # COVER PAGE
    # =====================================================

    story.append(
        Spacer(
            1,
            1.05 * inch,
        )
    )

    story.append(
        Paragraph(
            "RAIN INTELLIGENCE",
            cover_brand,
        )
    )

    story.append(
        Paragraph(
            _clean_text(
                game_plan.get(
                    "report_title",
                    "RAIN Strategic Game Plan",
                )
            ),
            cover_title,
        )
    )

    story.append(
        Paragraph(
            "Strategic direction and practical execution plan",
            cover_subtitle,
        )
    )

    client_name = game_plan.get(
        "client_name",
        "",
    )

    business_name = game_plan.get(
        "business_name",
        "",
    )

    cover_lines = []

    if client_name:
        cover_lines.append(
            f"<b>Prepared for</b><br/>{_clean_text(client_name)}"
        )

    if business_name:
        cover_lines.append(
            f"<b>Business or organization</b><br/>{_clean_text(business_name)}"
        )

    if consultation_date:
        cover_lines.append(
            f"<b>Consultation date</b><br/>{_clean_text(consultation_date)}"
        )

    if not cover_lines:
        cover_lines.append(
            "<b>Prepared through</b><br/>"
            "Find Your Way Network Marketing Consultants"
        )

    story.append(
        Paragraph(
            "<br/><br/>".join(cover_lines),
            cover_details,
        )
    )

    story.append(
        Spacer(
            1,
            1.15 * inch,
        )
    )

    story.append(
        Paragraph(
            "Prepared by Find Your Way Network Marketing Consultants",
            cover_details,
        )
    )

    story.append(PageBreak())

    # =====================================================
    # BODY HELPERS
    # =====================================================

    story.append(
        Paragraph(
            "Strategic Game Plan",
            report_title,
        )
    )

    def add_section(title, text):
        if not str(text or "").strip():
            return

        story.append(
            Paragraph(
                _clean_text(title),
                section_heading,
            )
        )

        story.append(
            Spacer(
                1,
                0.04 * inch,
            )
        )

        story.append(
            Paragraph(
                _clean_text(text),
                body,
            )
        )

    def add_list_section(
        title,
        items,
        empty_message=None,
    ):
        clean_items = _safe_list(items)

        if not clean_items and not empty_message:
            return

        story.append(
            Paragraph(
                _clean_text(title),
                section_heading,
            )
        )

        story.append(
            Spacer(
                1,
                0.04 * inch,
            )
        )

        if not clean_items:
            story.append(
                Paragraph(
                    _clean_text(empty_message),
                    body,
                )
            )

            return

        for item in clean_items:
            story.append(
                Paragraph(
                    _clean_text(item),
                    bullet,
                    bulletText="•",
                )
            )

    # =====================================================
    # MAIN SECTIONS
    # =====================================================

    add_section(
        "1. Strategic Snapshot",
        game_plan.get("strategic_snapshot"),
    )

    add_section(
        "2. Current Position",
        game_plan.get("current_position"),
    )

    add_section(
        "3. Desired Outcome",
        game_plan.get("desired_outcome"),
    )

    add_list_section(
        "4. Core Challenges",
        game_plan.get("core_challenges"),
    )

    add_list_section(
        "5. Strengths and Existing Assets",
        game_plan.get("strengths_and_assets"),
    )

    add_section(
        "6. Primary Opportunity",
        game_plan.get("primary_opportunity"),
    )

    add_section(
        "7. Recommended Strategic Direction",
        game_plan.get("strategic_direction"),
    )

    priorities = _safe_list(
        game_plan.get("immediate_priorities")
    )

    if priorities:
        story.append(
            Paragraph(
                "8. Immediate Priorities",
                section_heading,
            )
        )

        story.append(
            Spacer(
                1,
                0.04 * inch,
            )
        )

        for number, item in enumerate(
            priorities,
            start=1,
        ):
            story.append(
                Paragraph(
                    f"<b>Priority {number}</b><br/>{_clean_text(item)}",
                    priority,
                )
            )

    steps = _safe_list(
        game_plan.get("step_by_step_game_plan")
    )

    if steps:
        story.append(
            Paragraph(
                "9. Step-by-Step Game Plan",
                section_heading,
            )
        )

        story.append(
            Spacer(
                1,
                0.04 * inch,
            )
        )

        for index, step in enumerate(
            steps,
            start=1,
        ):
            step_content = []

            if not isinstance(step, dict):
                step_content.append(
                    Paragraph(
                        f"<b>Step {index}</b>",
                        step_heading,
                    )
                )

                step_content.append(
                    Paragraph(
                        _clean_text(step),
                        body,
                    )
                )

                story.append(
                    KeepTogether(step_content)
                )

                continue

            step_number = step.get(
                "step",
                index,
            )

            action = step.get(
                "action",
                "",
            )

            purpose = step.get(
                "purpose",
                "",
            )

            success_indicator = step.get(
                "success_indicator",
                "",
            )

            step_content.append(
                Paragraph(
                    f"Step {step_number}: {_clean_text(action)}",
                    step_heading,
                )
            )

            if purpose:
                step_content.append(
                    Paragraph(
                        f"<b>Purpose:</b> {_clean_text(purpose)}",
                        body,
                    )
                )

            if success_indicator:
                step_content.append(
                    Paragraph(
                        "<b>Success indicator:</b> "
                        f"{_clean_text(success_indicator)}",
                        body,
                    )
                )

            story.append(
                KeepTogether(step_content)
            )

    timeline_sections = [
        (
            "10. First 30 Days",
            game_plan.get("first_30_days"),
        ),
        (
            "11. Days 31–60",
            game_plan.get("days_31_to_60"),
        ),
        (
            "12. Days 61–90",
            game_plan.get("days_61_to_90"),
        ),
    ]

    for title, items in timeline_sections:
        add_list_section(
            title,
            items,
        )

    add_list_section(
        "13. Recommended Find Your Way Support",
        game_plan.get("recommended_fyw_support"),
        empty_message=(
            "No paid Find Your Way service is recommended at this time. "
            "The client should complete the current game-plan priorities "
            "before considering additional support."
        ),
    )

    add_list_section(
        "14. Risks and Things to Avoid",
        game_plan.get("risks_and_things_to_avoid"),
    )

    add_section(
        "15. Final Strategic Guidance",
        game_plan.get("final_strategic_guidance"),
    )

    story.append(
        Spacer(
            1,
            0.2 * inch,
        )
    )

    story.append(
        Paragraph(
            "This strategic game plan is advisory and is based on the "
            "information available during the consultation. Legal, tax, "
            "financial, licensing, medical, and other regulated matters "
            "should be verified with an appropriately qualified professional.",
            small_text,
        )
    )

    document.build(
        story,
        onFirstPage=_page_header_footer,
        onLaterPages=_page_header_footer,
    )

    pdf_buffer.seek(0)

    return pdf_buffer