const mongoose = require('mongoose');

const columnSchema = new mongoose.Schema(
  {
    name: String,
    type: { type: String, enum: ['numeric', 'date', 'categorical'] },
    nullCount: Number,
    uniqueCount: Number,
    min: mongoose.Schema.Types.Mixed,
    max: mongoose.Schema.Types.Mixed,
    mean: Number,
  },
  { _id: false }
);

const datasetSchema = new mongoose.Schema(
  {
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, index: true },
    filename: { type: String, required: true },
    rowCount: { type: Number, required: true },
    columns: [columnSchema],
    rows: { type: mongoose.Schema.Types.Mixed, default: [] },
    aiSummary: { type: String, default: '' },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Dataset', datasetSchema);
