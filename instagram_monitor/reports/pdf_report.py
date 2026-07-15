"""PDF report generator."""

from pathlib import Path
from datetime import datetime
from typing import List, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.enums import TA_CENTER
from loguru import logger

from instagram_monitor.core.settings import settings
from instagram_monitor.database import Account, DailyStatistics


class PDFReportGenerator:
    """Generate professional PDF reports."""

    def __init__(self):
        """Initialize PDF report generator."""
        self.reports_dir = settings.REPORTS_DIR
        self.reports_dir.mkdir(exist_ok=True)

    def generate_report(
        self,
        accounts: List[Account],
        statistics: Optional[List[DailyStatistics]] = None,
        filename: Optional[str] = None,
    ) -> Path:
        """Generate PDF report."""
        if not filename:
            filename = f"instagram_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        report_path = self.reports_dir / filename

        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                str(report_path),
                pagesize=letter,
                rightMargin=0.5 * inch,
                leftMargin=0.5 * inch,
                topMargin=0.5 * inch,
                bottomMargin=0.5 * inch,
            )

            # Container for PDF elements
            elements = []

            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#667eea"),
                spaceAfter=30,
                alignment=TA_CENTER,
            )

            # Title
            title = Paragraph("📊 OTT Instagram Monitor Report", title_style)
            elements.append(title)

            # Date
            date_para = Paragraph(
                f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                styles["Normal"],
            )
            elements.append(date_para)
            elements.append(Spacer(1, 0.3 * inch))

            # Summary section
            total_followers = sum(a.followers or 0 for a in accounts)
            total_posts = sum(a.posts_count or 0 for a in accounts)

            summary_data = [
                ["Metric", "Value"],
                ["Total Accounts", str(len(accounts))],
                ["Total Followers", f"{total_followers:,}"],
                ["Total Posts", f"{total_posts:,}"],
                ["Average Followers", f"{total_followers // len(accounts) if accounts else 0:,}"],
            ]

            summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
            summary_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667eea")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f5f5f5")),
                        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ]
                )
            )
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3 * inch))

            # Accounts table
            heading = Paragraph("<b>Top Accounts by Followers</b>", styles["Heading2"])
            elements.append(heading)
            elements.append(Spacer(1, 0.2 * inch))

            top_accounts = sorted(
                accounts, key=lambda x: x.followers or 0, reverse=True
            )[:10]

            accounts_data = [["Username", "Followers", "Posts", "Verified"]]
            for account in top_accounts:
                accounts_data.append(
                    [
                        account.username,
                        f"{account.followers or 0:,}",
                        str(account.posts_count or 0),
                        "✓" if account.verified else "✗",
                    ]
                )

            accounts_table = Table(accounts_data)
            accounts_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667eea")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f9f9f9")),
                        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ]
                )
            )
            elements.append(accounts_table)

            # Build PDF
            doc.build(elements)
            logger.info(f"PDF report saved to {report_path}")
            return report_path

        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            raise
