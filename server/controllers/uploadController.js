const Dataset = require('../models/Dataset');
const { parseCSVBuffer } = require('../utils/csvUtils');
const { computeStats } = require('../utils/statsUtils');
const { generateSummary } = require('../utils/geminiUtils');

async function uploadCSV(req, res, next) {
  try {
    if (!req.file) return res.status(400).json({ message: 'No file uploaded' });

    const rows = await parseCSVBuffer(req.file.buffer);
    if (rows.length === 0)
      return res.status(400).json({ message: 'CSV file is empty or malformed' });

    const columns = computeStats(rows);

    let aiSummary = '';
    try {
      aiSummary = await generateSummary(columns, rows.length, req.file.originalname);
    } catch (geminiErr) {
      console.error('Gemini summary failed:', geminiErr.message);
      aiSummary = 'AI summary unavailable. Please check your Gemini API key.';
    }

    const dataset = await Dataset.create({
      userId: req.userId,
      filename: req.file.originalname,
      rowCount: rows.length,
      columns,
      rows,
      aiSummary,
    });

    res.status(201).json({
      id: dataset._id,
      filename: dataset.filename,
      rowCount: dataset.rowCount,
      columns: dataset.columns,
      aiSummary: dataset.aiSummary,
    });
  } catch (err) {
    next(err);
  }
}

module.exports = { uploadCSV };
