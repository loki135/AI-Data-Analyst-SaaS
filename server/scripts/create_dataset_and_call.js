require('dotenv').config();
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
// use global fetch available in Node 18+
const fetch = global.fetch || (async () => { throw new Error('No fetch available') })();
const User = require('../models/User');
const Dataset = require('../models/Dataset');

const mongoUri = process.env.MONGO_URI || process.env.MONGO_URL || process.env.MONGO_CONN || process.env.MONGO_SRV_URI;
if (!mongoUri) {
  console.error('Missing MONGO_URI in .env');
  process.exit(1);
}

async function run() {
  await mongoose.connect(mongoUri);
  console.log('Connected to MongoDB');

  const user = await User.findOne({ email: 'test+lokesh@example.com' });
  if (!user) {
    throw new Error('Test user not found; run create_test_user.js first');
  }

  const ds = new Dataset({
    userId: user._id,
    filename: 'sample.csv',
    rowCount: 3,
    columns: [
      { name: 'age', type: 'numeric', nullCount: 0, uniqueCount: 3, min: 21, max: 45, mean: 33 },
      { name: 'city', type: 'categorical', nullCount: 0, uniqueCount: 2 },
    ],
    rows: [
      { age: 21, city: 'A' },
      { age: 45, city: 'B' },
      { age: 33, city: 'A' },
    ],
  });
  await ds.save();
  console.log('Created dataset:', ds._id.toString());

  const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '7d' });

  const res = await fetch('http://localhost:5000/api/ai/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ datasetId: ds._id.toString(), question: 'Give a short summary' }),
  });

  const text = await res.text();
  console.log('Response status:', res.status);
  console.log(text);

  await mongoose.disconnect();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
