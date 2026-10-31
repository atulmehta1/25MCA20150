import io
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(stock_symbol, model_name, metrics, forecast_data, tech_signals, risk_info):
    """
    Generates an executive PDF report containing model metrics, price forecast,
    technical indicator signals, and risk assessment.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )
    
    story = []
    
    # Header Banner
    story.append(Paragraph("Stock Market Prediction & AI Intelligence Report", title_style))
    story.append(Paragraph(
        f"<b>Asset:</b> {stock_symbol} &nbsp;|&nbsp; "
        f"<b>Model:</b> {model_name} &nbsp;|&nbsp; "
        f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=15))
    
    # Executive Summary Box
    recommendation = tech_signals.get('recommendation', 'HOLD')
    confidence = tech_signals.get('confidence', 60)
    risk_level = risk_info.get('risk_level', 'Medium')
    latest_price = tech_signals.get('latest_price', 0.0)
    
    rec_color = colors.HexColor('#16A34A') if 'BUY' in recommendation else (colors.HexColor('#DC2626') if 'SELL' in recommendation else colors.HexColor('#D97706'))
    
    exec_summary_data = [
        [
            Paragraph("<b>Overall AI Signal</b>", body_style),
            Paragraph(f"<b><font color='{rec_color.hexval()}'>{recommendation}</font></b> ({confidence}% Confidence)", body_style),
            Paragraph("<b>Latest Market Price</b>", body_style),
            Paragraph(f"<b>${latest_price:.2f}</b>", body_style)
        ],
        [
            Paragraph("<b>Risk Classification</b>", body_style),
            Paragraph(f"<b>{risk_level} Risk</b>", body_style),
            Paragraph("<b>Annualized Volatility</b>", body_style),
            Paragraph(f"{risk_info.get('ann_volatility', 20.0)}%", body_style)
        ]
    ]
    
    t_summary = Table(exec_summary_data, colWidths=[130, 140, 130, 130])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 15))
    
    # Section 1: Model Evaluation Metrics
    story.append(Paragraph("1. Machine Learning Performance Metrics", section_heading))
    
    metrics_rows = [["Metric", "Value", "Standard Interpretation"]]
    if 'rmse' in metrics:
        metrics_rows.append(["RMSE (Root Mean Squared Error)", f"{metrics['rmse']:.4f}", "Lower is better; measures prediction spread"])
        metrics_rows.append(["MAE (Mean Absolute Error)", f"{metrics['mae']:.4f}", "Average magnitude of price errors in USD"])
        metrics_rows.append(["R² Score (Coefficient of Determination)", f"{metrics['r2']:.4f}", "Variance explained (1.0 = perfect model)"])
        metrics_rows.append(["MAPE (Mean Absolute % Error)", f"{metrics.get('mape', 0.0):.2f}%", "Percentage difference from actual price"])
    else:
        metrics_rows.append(["Accuracy", f"{metrics.get('accuracy', 0.0):.2f}%", "Percentage of correct direction calls"])
        metrics_rows.append(["Precision", f"{metrics.get('precision', 0.0):.2f}%", "Ratio of true positive signals"])
        metrics_rows.append(["Recall", f"{metrics.get('recall', 0.0):.2f}%", "Sensitivity to upward market moves"])
        metrics_rows.append(["F1-Score", f"{metrics.get('f1_score', 0.0):.2f}%", "Harmonic balance of precision and recall"])
        
    t_metrics = Table(metrics_rows, colWidths=[180, 100, 250])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F1F5F9')])
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 15))
    
    # Section 2: Technical Indicators Matrix
    story.append(Paragraph("2. Technical Indicators Matrix", section_heading))
    tech_rows = [["Indicator", "Observed Value", "Signal / Condition"]]
    signals = tech_signals.get('signals', [])
    for s in signals:
        tech_rows.append([s['indicator'], str(s['value']), s['status']])
        
    t_tech = Table(tech_rows, colWidths=[150, 160, 220])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 15))
    
    # Section 3: Future Forecast
    if forecast_data and 'future_dates' in forecast_data:
        story.append(Paragraph("3. Multi-Day Price Forecast", section_heading))
        fc_rows = [["Forecast Date", "Predicted Price ($)", "Implied Shift from Current"]]
        base_p = latest_price or 100.0
        for dt, p in zip(forecast_data['future_dates'], forecast_data['future_predictions']):
            diff_pct = ((p - base_p) / base_p) * 100
            diff_str = f"+{diff_pct:.2f}%" if diff_pct >= 0 else f"{diff_pct:.2f}%"
            fc_rows.append([dt, f"${p:.2f}", diff_str])
            
        t_fc = Table(fc_rows, colWidths=[160, 160, 210])
        t_fc.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284C7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F9FF')])
        ]))
        story.append(t_fc)
        story.append(Spacer(1, 15))
        
    # Disclaimer
    story.append(Paragraph(
        "<b>Disclaimer:</b> This report is generated by algorithmic machine learning models and quantitative indicators "
        "for educational and analytical purposes only. It does not constitute formal financial, investment, or legal advice. "
        "Past performance is not indicative of future returns.",
        ParagraphStyle('Disclaimer', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor('#94A3B8'))
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_csv_report(stock_symbol, model_name, metrics, forecast_data):
    """Generates CSV string of forecast and metrics."""
    rows = []
    if forecast_data and 'future_dates' in forecast_data:
        for dt, p in zip(forecast_data['future_dates'], forecast_data['future_predictions']):
            rows.append({
                'Symbol': stock_symbol,
                'Model': model_name,
                'Date': dt,
                'Predicted_Price': p,
                'RMSE': metrics.get('rmse', ''),
                'MAE': metrics.get('mae', ''),
                'R2_Score': metrics.get('r2', '')
            })
    df_out = pd.DataFrame(rows)
    return df_out.to_csv(index=False)
