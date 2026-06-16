const GEMINI_MODEL = process.env.GEMINI_MODEL || 'gemini-1.5';
const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${process.env.GEMINI_API_KEY}`;

async function callGemini(prompt) {
  const res = await fetch(GEMINI_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
  });
  if (!res.ok) {
    const errText = await res.text();
    let errMsg = `Gemini API error: ${errText}`;
    if (res.status === 404) {
      errMsg += `\nModel ${GEMINI_MODEL} not found for API version v1beta. Set GEMINI_MODEL to a supported model, or call ModelService.ListModels to see available models.`;
    }
    throw new Error(errMsg);
  }
  const data = await res.json();
  return data.candidates[0].content.parts[0].text;
}

async function generateSummary(columns, rowCount, filename) {
  const colDesc = columns
    .map((c) => `${c.name} (${c.type}${c.type === 'numeric' ? `, mean: ${c.mean}, min: ${c.min}, max: ${c.max}` : ''}, nulls: ${c.nullCount}, unique: ${c.uniqueCount})`)
    .join('; ');
  const prompt = `You are a data analyst. Analyze this CSV dataset and write a concise 3-4 sentence plain-English summary for a non-technical user.

Dataset: "${filename}"
Rows: ${rowCount}
Columns: ${colDesc}

Write only the summary, no headings or bullet points.`;
  return callGemini(prompt);
}

async function answerQuestion(question, columns, sampleRows) {
  const colNames = columns.map((c) => c.name).join(', ');
  const rowsStr = JSON.stringify(sampleRows.slice(0, 10), null, 2);
  const prompt = `You are a helpful data analyst. Answer the user's question about a CSV dataset based on the sample data provided.

Columns: ${colNames}
Sample rows (first 10):
${rowsStr}

User question: ${question}

Give a clear, concise, helpful answer. If you cannot determine the answer from the sample, say so.`;
  return callGemini(prompt);
}

async function suggestChartType(columns) {
  const colDesc = columns.map((c) => `${c.name} (${c.type})`).join(', ');
  const prompt = `You are a data visualization expert. Given these columns, suggest the best chart type.

Columns: ${colDesc}

Respond with ONLY valid JSON in this exact format, no markdown, no explanation:
{"type":"bar","x":"column_name","y":"column_name","reason":"one sentence reason"}

type must be one of: bar, line, pie`;
  const text = await callGemini(prompt);
  const clean = text.replace(/```json|```/g, '').trim();
  return JSON.parse(clean);
}

module.exports = { generateSummary, answerQuestion, suggestChartType };
