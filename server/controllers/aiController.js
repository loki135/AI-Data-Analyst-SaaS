const Dataset = require('../models/Dataset');
const { answerQuestion, suggestChartType } = require('../utils/geminiUtils');

async function askQuestion(req, res, next) {
  try {
    const { datasetId, question } = req.body;
    if (!datasetId || !question)
      return res.status(400).json({ message: 'datasetId and question are required' });

    const dataset = await Dataset.findOne({ _id: datasetId, userId: req.userId });
    if (!dataset) return res.status(404).json({ message: 'Dataset not found' });

    const answer = await answerQuestion(question, dataset.columns, dataset.rows);
    res.json({ answer });
  } catch (err) {
    next(err);
  }
}

async function suggestChart(req, res, next) {
  try {
    const { datasetId } = req.body;
    if (!datasetId) return res.status(400).json({ message: 'datasetId is required' });

    const dataset = await Dataset.findOne({ _id: datasetId, userId: req.userId }).select('columns');
    if (!dataset) return res.status(404).json({ message: 'Dataset not found' });

    const suggestion = await suggestChartType(dataset.columns);
    res.json(suggestion);
  } catch (err) {
    next(err);
  }
}

module.exports = { askQuestion, suggestChart };
