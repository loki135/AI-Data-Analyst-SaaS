const Dataset = require('../models/Dataset');

async function listDatasets(req, res, next) {
  try {
    const datasets = await Dataset.find({ userId: req.userId })
      .select('-rows')
      .sort({ createdAt: -1 });
    res.json(datasets);
  } catch (err) {
    next(err);
  }
}

async function getDataset(req, res, next) {
  try {
    const dataset = await Dataset.findOne({ _id: req.params.id, userId: req.userId });
    if (!dataset) return res.status(404).json({ message: 'Dataset not found' });
    res.json(dataset);
  } catch (err) {
    next(err);
  }
}

async function deleteDataset(req, res, next) {
  try {
    const dataset = await Dataset.findOneAndDelete({ _id: req.params.id, userId: req.userId });
    if (!dataset) return res.status(404).json({ message: 'Dataset not found' });
    res.json({ message: 'Dataset deleted' });
  } catch (err) {
    next(err);
  }
}

module.exports = { listDatasets, getDataset, deleteDataset };
