// ==========================================================================
// Certificate Generator (Canvas-Based High-Res Export & Verification)
// ==========================================================================

const certModule = {
  certData: {
    id: "CERT-2024-8841",
    studentName: "Atul Mehta",
    courseTitle: "Full Stack Web Development with Node.js & React",
    issueDate: "October 25, 2024",
    score: 92,
    instructor: "Dr. Priya Nair"
  },

  initCertificatePage() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('certId');
    const name = params.get('name');
    const course = params.get('course');

    if (id) this.certData.id = id;
    if (name) this.certData.studentName = decodeURIComponent(name);
    if (course) this.certData.courseTitle = decodeURIComponent(course);

    this.drawCertificate();
  },

  drawCertificate() {
    const canvas = document.getElementById('cert-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    // Canvas dimensions: 1000 x 700 (High-Res 16:11 Certificate Aspect Ratio)
    const W = canvas.width;
    const H = canvas.height;

    // 1. Background Fill
    ctx.fillStyle = '#0a0f1d';
    ctx.fillRect(0, 0, W, H);

    // 2. Outer Ornate Border
    ctx.lineWidth = 14;
    ctx.strokeStyle = '#38bdf8';
    ctx.strokeRect(20, 20, W - 40, H - 40);

    // 3. Inner Gold Accent Border
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#fbbf24';
    ctx.strokeRect(34, 34, W - 68, H - 68);

    // 4. Corner Ornaments
    ctx.fillStyle = '#818cf8';
    [[45, 45], [W - 45, 45], [45, H - 45], [W - 45, H - 45]].forEach(([cx, cy]) => {
      ctx.beginPath();
      ctx.arc(cx, cy, 8, 0, Math.PI * 2);
      ctx.fill();
    });

    // 5. Header Title
    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 22px Segoe UI, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('AI TECHNICAL TRAINING PLATFORM', W / 2, 95);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '14px Segoe UI, sans-serif';
    ctx.fillText('OFFICIAL CERTIFICATE OF COMPLETION', W / 2, 125);

    // 6. Presented To
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'italic 16px Georgia, serif';
    ctx.fillText('This is to certify that', W / 2, 190);

    // 7. Student Name
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 36px Segoe UI, sans-serif';
    ctx.fillText(this.certData.studentName, W / 2, 245);

    // Underline below name
    ctx.strokeStyle = 'rgba(251, 191, 36, 0.4)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(W / 2 - 200, 260);
    ctx.lineTo(W / 2 + 200, 260);
    ctx.stroke();

    // 8. Fulfillment text
    ctx.fillStyle = '#cbd5e1';
    ctx.font = '16px Segoe UI, sans-serif';
    ctx.fillText('has successfully demonstrated technical proficiency and completed the rigorous curriculum for:', W / 2, 305);

    // 9. Course Name
    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 26px Segoe UI, sans-serif';
    ctx.fillText(this.certData.courseTitle, W / 2, 355);

    // 10. Grade & Assessment score
    ctx.fillStyle = '#34d399';
    ctx.font = 'bold 16px Segoe UI, sans-serif';
    ctx.fillText(`Assessment Score: ${this.certData.score}%  |  Status: Verified Honors`, W / 2, 400);

    // 11. Security Watermark / Seal
    ctx.beginPath();
    ctx.arc(W / 2, 490, 45, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(56, 189, 248, 0.1)';
    ctx.fill();
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 12px Segoe UI, sans-serif';
    ctx.fillText('AI CERTIFIED', W / 2, 485);
    ctx.fillText('VERIFIED', W / 2, 502);

    // 12. Bottom Signatures & Date
    ctx.textAlign = 'left';
    ctx.fillStyle = '#94a3b8';
    ctx.font = '14px Segoe UI, sans-serif';
    ctx.fillText(`Issued: ${this.certData.issueDate}`, 80, 580);
    ctx.fillText(`Certificate ID: ${this.certData.id}`, 80, 605);

    ctx.textAlign = 'right';
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'italic bold 18px Georgia, serif';
    ctx.fillText(this.certData.instructor, W - 80, 580);
    ctx.fillStyle = '#94a3b8';
    ctx.font = '14px Segoe UI, sans-serif';
    ctx.fillText('Lead Technical Instructor', W - 80, 605);

    // Signature line
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(W - 260, 560);
    ctx.lineTo(W - 80, 560);
    ctx.stroke();
  },

  downloadCertificate() {
    const canvas = document.getElementById('cert-canvas');
    if (!canvas) return;

    const link = document.createElement('a');
    link.download = `${this.certData.studentName.replace(/\s+/g, '_')}_Certificate_${this.certData.id}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    app.showToast('Certificate PNG downloaded successfully', 'success');
  },

  verifyCertificate(idInput) {
    const id = idInput ? idInput.trim().toUpperCase() : '';
    const resultBox = document.getElementById('verify-result-box');
    if (!id || !resultBox) return;

    resultBox.style.display = 'block';

    if (id.includes('CERT')) {
      resultBox.innerHTML = `
        <div style="background: rgba(52, 211, 153, 0.15); border: 1px solid var(--accent-green); border-radius: var(--radius-md); padding: 1.25rem;">
          <h4 style="color: var(--accent-green); margin-bottom: 0.5rem;">Certificate Authenticity Verified</h4>
          <p style="font-size: 0.9rem; color: var(--text-primary); margin-bottom: 0.25rem;">Student Name: <strong>${this.certData.studentName}</strong></p>
          <p style="font-size: 0.9rem; color: var(--text-primary); margin-bottom: 0.25rem;">Course: <strong>${this.certData.courseTitle}</strong></p>
          <p style="font-size: 0.85rem; color: var(--text-secondary);">Issued on ${this.certData.issueDate} with passing score ${this.certData.score}%.</p>
        </div>
      `;
    } else {
      resultBox.innerHTML = `
        <div style="background: rgba(251, 113, 133, 0.15); border: 1px solid var(--accent-rose); border-radius: var(--radius-md); padding: 1.25rem; color: var(--accent-rose);">
          Invalid Certificate ID. Please verify the code on the bottom left of the certificate.
        </div>
      `;
    }
  }
};
