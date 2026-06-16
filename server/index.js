require('dotenv').config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const errorHandler = require('./middleware/errorHandler');

const app = express();

app.use(cors({
  origin: process.env.CLIENT_URL || 'http://localhost:5173',
  credentials: true,
}));
app.use(express.json({ limit: '10mb' }));

// Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/upload', require('./routes/upload'));
app.use('/api/analysis', require('./routes/analysis'));
app.use('/api/ai', require('./routes/ai'));

app.get('/api/health', (req, res) => res.json({ status: 'ok' }));

app.use(errorHandler);

const mongoUri = process.env.MONGO_URI || process.env.MONGO_URL || process.env.MONGO_CONN || process.env.MONGO_SRV_URI;

if (!mongoUri) {
  console.error('Missing MongoDB URI. Set `MONGO_URI` (or MONGO_URL/MONGO_CONN/MONGO_SRV_URI) in your .env file.');
  process.exit(1);
}

mongoose
  .connect(mongoUri)
  .then(() => {
    console.log('MongoDB connected');
    const PORT = process.env.PORT || 5000;
    app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
  })
  .catch((err) => {
    console.error('MongoDB connection error:', err);
    if (err && err.syscall === 'querySrv') {
      console.error('\nIt looks like the connection string uses the SRV format (mongodb+srv://) and DNS SRV lookups failed.');
      console.error('Possible fixes:');
      console.error('- Ensure this machine has internet/DNS access and outbound DNS on port 53 is not blocked.');
      console.error('- In Atlas, copy the "Standard connection string" (non-SRV) and set it as `MONGO_URI` in your .env.');
      console.error('- Or run a local MongoDB and set `MONGO_URI=mongodb://localhost:27017/your_db` in your .env for local development.');
    }
    process.exit(1);
  });
